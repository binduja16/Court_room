from fastapi import FastAPI, UploadFile, Request
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import json, os, re
from io import BytesIO

from extract import extract_text
from simplify import simplify_text
from facts import extract_facts
from draft import generate_draft
from safety import check_safety
from report_generator import generate_pdf

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load IPC Sections
with open("ipc_sections.json") as f:
    ipc_data = json.load(f)

# Load IPC Synonyms (NEW)
with open("ipc_synonyms.json") as f:
    ipc_synonyms = json.load(f)


# --- Detect IPC sections ---
def detect_ipc(text: str):
    found = []
    text_lower = text.lower()

    for sec, info in ipc_data.items():
        # Info can be dict or string
        if isinstance(info, dict):
            desc = info["description"]
            law = info.get("law", "IPC")
        else:
            desc = info
            law = "IPC"

        # --- 1. Match "Section <number>" ---
        pattern = rf"\bsection\s*{sec}\b"
        if re.search(pattern, text_lower, re.IGNORECASE):
            found.append({"section": sec, "description": desc, "law": law})
            continue

        # --- 2. Full description match ---
        if desc.lower() in text_lower:
            found.append({"section": sec, "description": desc, "law": law})
            continue

        # --- 3. Synonyms from external JSON ---
        if sec in ipc_synonyms:
            for word in ipc_synonyms[sec]:
                if re.search(rf"\b{word.lower()}\b", text_lower):
                    found.append({"section": sec, "description": desc, "law": law})
                    break

    # Remove duplicates
    unique = {f"{s['section']}": s for s in found}
    return list(unique.values())


# --- Clean extracted facts ---
def clean_facts(facts):
    cleaned = {}
    for key, val in facts.items():
        if isinstance(val, list):
            cleaned[key] = list({v.strip() for v in val if v.strip()})  # deduplicate
        else:
            cleaned[key] = val
    return cleaned


# --- Remove generic parties ---
# --- Remove generic / junk parties ---
def clean_parties(facts):
    ignore_list = [
        'Incident Summary', 'First Information', 'Offense Sections',
        'Action Taken', 'Police Station', 'Bengaluru City',
        'Station House', 'Loan Recovery', 'Home Loan',
        'Authorized Signatory', 'Account No',
        'Sections Applied'   # NEW – removes junk field
    ]
    cleaned = [p for p in facts.get('Parties', []) if p not in ignore_list and p.strip()]
    facts['Parties'] = cleaned
    return facts



@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/process/")
async def process_file(request: Request, file: UploadFile):
    # Read uploaded file
    file_bytes = await file.read()
    try:
        extracted = extract_text(BytesIO(file_bytes))
    except Exception as e:
        return {"error": f"File could not be processed: {str(e)}"}

    # Summarize and extract facts
    summary = simplify_text(extracted)
    facts = extract_facts(extracted)
    facts = clean_facts(facts)
    facts = clean_parties(facts)

    # Generate draft petition
    draft = generate_draft(
        facts.get("Parties", []),
        facts.get("Amounts", []),
        facts.get("Dates", []),
        summary
    )

    # Detect IPC sections
    ipc_list = detect_ipc(extracted)

    # Load and fix resources
    with open("resources.json") as f:
        resources_dict = json.load(f)
    resources = []
    for k, v in resources_dict.items():
        resources.append({
            "Authority": v.get("authority", k),
            "Helpline": v.get("helpline", "N/A")
        })

    # Generate PDF report
    report_file = generate_pdf(summary, facts, draft, ipc_list, resources)

    return templates.TemplateResponse("result.html", {
        "request": request,
        "summary": summary,
        "facts": facts,
        "draft": draft,
        "ipc_list": ipc_list,
        "resources": resources,
        "report_file": report_file
    })


@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(".", filename)
    return FileResponse(file_path, media_type="application/pdf", filename=filename)
