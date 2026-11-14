import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def create_dental_ai_document(output_path):
    doc = Document()

    # Set Margins
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Color Palette
    HEX_PRIMARY = "1E3A8A"      # Deep Navy
    HEX_SECONDARY = "0D9488"    # Teal
    HEX_DARK = "0F172A"         # Slate Dark
    HEX_MUTED = "475569"        # Slate Muted
    HEX_BG_LIGHT = "F8FAFC"     # Light Slate Background
    HEX_BORDER = "CBD5E1"       # Border Gray
    HEX_ACCENT_BG = "F0FDFA"    # Light Teal BG

    COLOR_PRIMARY = RGBColor(30, 58, 138)
    COLOR_SECONDARY = RGBColor(13, 148, 136)
    COLOR_DARK = RGBColor(15, 23, 42)
    COLOR_MUTED = RGBColor(71, 85, 105)

    # Set default style font
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(10.5)
    normal_style.font.color.rgb = COLOR_DARK

    def set_cell_background(cell, fill_hex):
        tcPr = cell._tc.get_or_add_tcPr()
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
        tcPr.append(shd)

    def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
        tcPr.append(tcMar)

    def add_callout(text, title="NOTE", bg_hex=HEX_ACCENT_BG, border_hex=HEX_SECONDARY):
        table = doc.add_table(rows=1, cols=1)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False
        table.columns[0].width = Inches(6.5)
        
        cell = table.cell(0, 0)
        set_cell_background(cell, bg_hex)
        set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
        
        tcPr = cell._tc.get_or_add_tcPr()
        borders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:top w:val="none"/><w:left w:val="single" w:sz="24" w:space="0" w:color="{border_hex}"/><w:bottom w:val="none"/><w:right w:val="none"/></w:tcBorders>')
        tcPr.append(borders)
        
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(4)
        run_title = p.add_run(f"📌 {title}: ")
        run_title.bold = True
        run_title.font.color.rgb = COLOR_SECONDARY if border_hex == HEX_SECONDARY else RGBColor(185, 28, 28)
        
        run_text = p.add_run(text)
        run_text.font.size = Pt(10)
        run_text.font.color.rgb = COLOR_DARK
        doc.add_paragraph().paragraph_format.space_after = Pt(4)

    def add_custom_heading_1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(16)
        run.bold = True
        run.font.color.rgb = COLOR_PRIMARY
        return p

    def add_custom_heading_2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(13)
        run.bold = True
        run.font.color.rgb = COLOR_SECONDARY
        return p

    def add_custom_heading_3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(11)
        run.bold = True
        run.font.color.rgb = COLOR_DARK
        return p

    def style_table(table, col_widths, headers, data):
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False
        
        # Header Row
        hdr_row = table.rows[0]
        for idx, header_text in enumerate(headers):
            cell = hdr_row.cells[idx]
            cell.width = Inches(col_widths[idx])
            set_cell_background(cell, HEX_PRIMARY)
            set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            run = p.add_run(header_text)
            run.bold = True
            run.font.color.rgb = RGBColor(255, 255, 255)
            run.font.size = Pt(9.5)
            
        # Data Rows
        for r_idx, row_data in enumerate(data):
            row = table.rows[r_idx + 1]
            bg_color = HEX_BG_LIGHT if r_idx % 2 == 1 else "FFFFFF"
            for c_idx, cell_value in enumerate(row_data):
                cell = row.cells[c_idx]
                cell.width = Inches(col_widths[c_idx])
                set_cell_background(cell, bg_color)
                set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
                
                # Apply light border
                tcPr = cell._tc.get_or_add_tcPr()
                borders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:top w:val="single" w:sz="4" w:space="0" w:color="{HEX_BORDER}"/><w:left w:val="single" w:sz="4" w:space="0" w:color="{HEX_BORDER}"/><w:bottom w:val="single" w:sz="4" w:space="0" w:color="{HEX_BORDER}"/><w:right w:val="single" w:sz="4" w:space="0" w:color="{HEX_BORDER}"/></w:tcBorders>')
                tcPr.append(borders)
                
                p = cell.paragraphs[0]
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                p.paragraph_format.space_before = Pt(0)
                p.paragraph_format.space_after = Pt(0)
                run = p.add_run(cell_value)
                run.font.size = Pt(9.5)
                run.font.color.rgb = COLOR_DARK

    # -------------------------------------------------------------
    # DOCUMENT COVER & HEADER
    # -------------------------------------------------------------
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(24)
    title_p.paragraph_format.space_after = Pt(4)
    r_title = title_p.add_run("AI Dental Receptionist & Automated Consultation Scheduling Agent")
    r_title.bold = True
    r_title.font.size = Pt(22)
    r_title.font.color.rgb = COLOR_PRIMARY

    sub_p = doc.add_paragraph()
    sub_p.paragraph_format.space_after = Pt(14)
    r_sub = sub_p.add_run("Market Landscape, Technical Architecture, PMS Integrations, Workflow State Machine & Implementation Blueprint")
    r_sub.font.size = Pt(13)
    r_sub.font.color.rgb = COLOR_SECONDARY

    # Metadata Block
    meta_p = doc.add_paragraph()
    meta_p.paragraph_format.space_after = Pt(18)
    meta_run = meta_p.add_run("Target Domain: Dentistry & Healthcare Practice Management | Status: Comprehensive Architectural Specification & Build Plan")
    meta_run.font.size = Pt(9)
    meta_run.font.color.rgb = COLOR_MUTED

    # Divider Line
    div_p = doc.add_paragraph()
    div_p.paragraph_format.space_after = Pt(14)
    pBdr = parse_xml(f'<w:pBdr {nsdecls("w")}><w:bottom w:val="single" w:sz="18" w:space="1" w:color="{HEX_PRIMARY}"/></w:pBdr>')
    div_p._p.get_or_add_pPr().append(pBdr)

    # -------------------------------------------------------------
    # SECTION 1: EXECUTIVE SUMMARY
    # -------------------------------------------------------------
    add_custom_heading_1("1. Executive Summary")
    
    p = doc.add_paragraph()
    p.add_run("In modern dental practices, front-desk staff spend over 65% of their working hours answering inbound phone calls, managing scheduling, handling cancellations, triaging patient complaints, and checking insurance. Unanswered calls (especially after-hours and during peak clinic hours) result in an estimated $100,000–$250,000 in lost annual production per dental operatory.\n\n"
              "This document outlines the complete technical blueprint for an ")
    r_b = p.add_run("Autonomous AI Dental Voice & Scheduling Agent")
    r_b.bold = True
    p.add_run(". The system ingests incoming phone calls, converses naturally with human-like voice latency (<600ms), conducts clinical triage (differentiating between routine cleanings, cosmetic consultations, and acute pulpitis/emergencies), checks real-time doctor availability via Dental Practice Management Software (PMS), and commits the confirmed booking directly into the doctor's calendar.")

    add_callout("Yes, we can 100% build, customize, and deploy this autonomous agent for your dental practice or SaaS platform using modern low-latency Voice AI infrastructure (Twilio/LiveKit + Deepgram Nova-2 + GPT-4o/Gemini + Cartesia/ElevenLabs + Dental PMS APIs).", "FEASIBILITY CONFIRMATION")

    # -------------------------------------------------------------
    # SECTION 2: EXISTING MARKET SOLUTIONS & BENCHMARKING
    # -------------------------------------------------------------
    add_custom_heading_1("2. Market Landscape: Existing AI Dental Agents")

    p = doc.add_paragraph()
    p.add_run("Several specialized AI agents and voice platforms currently operate in the dental reception and patient scheduling domain. Understanding their architectures and strengths helps guide our build:")

    add_custom_heading_2("2.1 Specialized Dental AI Receptionists")
    
    p = doc.add_paragraph()
    p.add_run("1. Arini AI: ").bold = True
    p.add_run("A dedicated AI dental receptionist that plugs into dental PMS (Dentrix, Open Dental, Eaglesoft). Handles after-hours booking, multi-chair scheduling, and insurance FAQ answering.\n\n")
    p.add_run("2. Rondah AI: ").bold = True
    p.add_run("Provides real-time bidirectional PMS synchronization, conversational phone handling, and automated post-call SMS follow-ups for dental clinics.\n\n")
    p.add_run("3. Dentina AI: ").bold = True
    p.add_run("Voice-driven dental receptionist with clinical triage capabilities, specialized operatory allocation (hygiene chair vs. surgical chair), and doctor routing.\n\n")
    p.add_run("4. NexHealth Voice / Online Sync: ").bold = True
    p.add_run("The gold standard in dental PMS integration APIs, offering universal read/write synchronization with over 40+ dental management software systems.\n\n")
    p.add_run("5. Kickcall & OpenMic AI: ").bold = True
    p.add_run("Niche voice agents tailored for single and multi-location dental offices focusing on low-latency call deflection and high appointment conversion.")

    add_custom_heading_2("2.2 Core Voice AI Infrastructure Engines")
    p = doc.add_paragraph()
    p.add_run("Behind specialized dental bots are foundational voice platforms such as ")
    p.add_run("Vapi.ai, Retell AI, Bland AI, and LiveKit Voice Agents").bold = True
    p.add_run(". These platforms provide telephony bridges (WebSockets, SIP trunks), audio streaming pipelines, fast Speech-to-Text (STT), LLM orchestrators, and Text-to-Speech (TTS) synthesis.")

    # Comparative Table
    add_custom_heading_3("Comparative Feature Matrix: Top Dental AI Solutions")
    
    headers = ["Vendor / Platform", "Primary Domain", "PMS Sync Level", "Average Latency", "Emergency Triage", "Deployment Model"]
    table_data = [
        ["Arini AI", "Dental Dedicated", "Level 4 (2-Way Write)", "~700ms - 900ms", "Yes (Rules/LLM)", "SaaS / PMS Plugin"],
        ["Rondah AI", "Dental Dedicated", "Level 4 (Real-time Sync)", "~800ms", "Yes (SMS alert)", "Cloud SaaS"],
        ["Dentina AI", "Dental & Ortho", "Level 3 (Read / Hold)", "~750ms", "Yes (Transfer)", "Cloud SaaS"],
        ["NexHealth", "Universal Dental API", "Level 5 (Direct Sync)", "API Sync", "N/A (Data Layer)", "API & Webhook Engine"],
        ["Retell / Vapi (Custom)", "Custom Voice Platform", "Full Custom (Any PMS)", "<500ms (Ultra-Fast)", "Configurable", "Self-Hosted / Hybrid Cloud"],
        ["Smith.ai Hybrid", "General Medical/Legal", "Level 2 (Zapier / Webhook)", "Human-in-Loop", "Manual Warm Transfer", "Managed Service"]
    ]
    
    tbl = doc.add_table(rows=len(table_data) + 1, cols=len(headers))
    style_table(tbl, [1.1, 1.1, 1.1, 0.9, 1.1, 1.2], headers, table_data)

    # -------------------------------------------------------------
    # SECTION 3: SYSTEM ARCHITECTURE
    # -------------------------------------------------------------
    add_custom_heading_1("3. End-to-End System Architecture")

    p = doc.add_paragraph()
    p.add_run("An enterprise-grade Dental AI Voice Agent requires a modular 6-layer architecture designed for sub-second latency, clinical safety, HIPAA compliance, and reliable PMS write-back.")

    add_custom_heading_2("3.1 The 6 Architectural Layers")

    layers = [
        ("Layer 1: Telephony & Audio Streaming", "Ingests PSTN phone calls via SIP Trunking / Twilio / Telnyx. Streams bidirectional raw audio over WebSockets (PCM 16-bit, 8kHz or 16kHz) to the voice gateway."),
        ("Layer 2: Real-Time Speech Pipeline", "Speech-to-Text (STT) via Deepgram Nova-2 (Medical/Conversational model) with sub-150ms transcription and Voice Activity Detection (VAD) for natural interruptions. Text-to-Speech (TTS) via Cartesia Sonic or ElevenLabs Flash (<100ms first-byte audio)."),
        ("Layer 3: Dental LLM Orchestrator & Triage", "Powered by GPT-4o-mini / Claude 3.5 Sonnet / Gemini 1.5 Flash. Executes prompt engineering specifically trained on dental terminology (prophylaxis, root canal, crown, bridge, extraction, veneer, emergency pulpitis, pediatric care). Executes structured tool-calling / function-calling."),
        ("Layer 4: Dental PMS & EHR Integration Layer", "Communicates bi-directionally with Dental Practice Management Systems (Open Dental API, Dentrix Developer API, Eaglesoft via Bridge, NexHealth API, Curve Dental, or Google/Outlook Calendar for private practices). Handles real-time slot lock to prevent double-booking."),
        ("Layer 5: Notification & Human Warm-Transfer", "Triggers instantaneous SMS appointment confirmations, calendar invites (.ics), doctor WhatsApp/Slack alerts, and initiates SIP live-call transfers to on-duty dental staff for acute emergencies."),
        ("Layer 6: Security, Compliance & Observability", "Enforces HIPAA compliance, AES-256 encryption at rest/in transit, zero data retention on voice logs containing PHI, BAA (Business Associate Agreement) contracts, and real-time call tracing.")
    ]

    for title, desc in layers:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(4)
        r_t = p.add_run(f"• {title}: ")
        r_t.bold = True
        r_t.font.color.rgb = COLOR_PRIMARY
        p.add_run(desc)

    add_custom_heading_2("3.2 Architectural Flow Diagram")
    
    diagram_box = doc.add_table(rows=1, cols=1)
    diagram_box.alignment = WD_TABLE_ALIGNMENT.CENTER
    d_cell = diagram_box.cell(0,0)
    set_cell_background(d_cell, HEX_BG_LIGHT)
    set_cell_margins(d_cell, 120, 120, 160, 160)
    
    dp = d_cell.paragraphs[0]
    dp.paragraph_format.space_before = Pt(0)
    dp.paragraph_format.space_after = Pt(0)
    d_text = dp.add_run(
"""[Incoming Caller: Patient]
         │ (PSTN Call)
         ▼
[Twilio / Telnyx Telephony SIP Trunk]
         │ (Bidirectional Audio Stream / WebSockets)
         ▼
[Voice Gateway / Orchestration Server (FastAPI / LiveKit / Vapi)]
    ├── [STT: Deepgram Nova-2] ────────────► Transcribed Utterance
    │                                              │
    ├── [Dental AI Engine (GPT-4o / Claude)] ◄─────┘
    │        │
    │        ├── [Tool: CheckDoctorAvailability()] ──► [Dental PMS: Dentrix / OpenDental]
    │        ├── [Tool: BookAppointmentSlot()]      ──► [Database / Operatory Calendar]
    │        └── [Tool: TriageEmergencyTransfer()]  ──► [SIP Live Transfer to Clinic]
    │        │
    ├── [TTS: Cartesia Sonic / ElevenLabs] ◄── Generated Speech Token Stream
    │        │
    └────────┴───────────────────────────────► Output Audio to Caller Phone
                                                   │
                                      [Post-Call Dispatcher]
                                      ├── SMS Confirmation (Twilio)
                                      └── Doctor Dashboard Summary"""
    )
    d_text.font.name = "Consolas"
    d_text.font.size = Pt(8.5)
    d_text.font.color.rgb = COLOR_DARK

    # -------------------------------------------------------------
    # SECTION 4: CALL WORKFLOW & CONVERSATIONAL STATE MACHINE
    # -------------------------------------------------------------
    add_custom_heading_1("4. Step-by-Step Call Handling Workflow")

    p = doc.add_paragraph()
    p.add_run("The AI Dental Manager follows a deterministic, clinically safe conversational state machine. Below is the step-by-step workflow from the moment the patient dials the dental clinic:")

    wf_steps = [
        ("Step 1: Greeting & Intent Identification", 
         "• AI greets caller with custom clinic branding (e.g., 'Thank you for calling BrightSmile Dental, I'm Maya, Dr. Smith's AI assistant. How can I help you today?').\n"
         "• Caller states intent: (e.g., 'I have a terrible toothache', 'I need to book a routine cleaning', 'Do you take Delta Dental?')."),
        
        ("Step 2: Patient Verification & Intake",
         "• AI asks: 'Have you visited Dr. Smith before, or are you a new patient?'\n"
         "• Existing Patient: AI looks up record via caller ID phone number in PMS database.\n"
         "• New Patient: AI collects First Name, Last Name, Date of Birth, and Mobile Number."),
        
        ("Step 3: Clinical Triage & Operatory Assignment",
         "• The AI classifies the appointment type and maps it to the appropriate chair and provider:\n"
         "  - Routine Prophylaxis / Hygiene: 45-60 min -> Dental Hygienist / Hygiene Chair.\n"
         "  - Severe Pain / Broken Tooth: 30-45 min Urgent Evaluation -> Associate/Lead Dentist.\n"
         "  - Orthodontic / Invisalign Consult: 30 min -> Orthodontist.\n"
         "  - Cosmetic / Veneers / Whitening: 45 min -> Lead Cosmetic Dentist.\n"
         "• Emergency Protocol Check: If patient mentions uncontrolled bleeding, facial swelling extending to the eye, or difficulty breathing, the AI activates EMERGENCY PROTOCOL -> advises immediate ER / warm transfers to dentist on-call."),

        ("Step 4: Real-Time Doctor Schedule Query",
         "• AI executes get_available_slots(provider_id, procedure_type, preferred_date_range).\n"
         "• The system cross-references provider working hours, operatory availability, and buffer times.\n"
         "• AI offers 2-3 specific choices: 'Dr. Smith has an opening this Thursday at 10:30 AM or Friday afternoon at 2:00 PM. Which one works better for you?'"),

        ("Step 5: Slot Reservation & Conflict Resolution",
         "• Caller selects: 'Thursday at 10:30 AM works great.'\n"
         "• AI puts a temporary soft lock on the PMS slot to prevent concurrent double-booking.\n"
         "• If caller requests an unavailable time, AI offers the nearest alternative or adds them to the VIP Cancellation Waitlist."),

        ("Step 6: Insurance & Intake Pre-Screening",
         "• AI inquires: 'Will you be using dental insurance such as Delta Dental, Cigna, or MetLife, or will you be self-paying?'\n"
         "• Records insurance carrier name and policy ID if provided, or notes for front-desk follow-up."),

        ("Step 7: Appointment Confirmation & PMS Write-Back",
         "• AI executes create_appointment_booking() in Dentrix / Open Dental.\n"
         "• AI provides verbal recap: 'You are all set for Thursday, October 24th at 10:30 AM with Dr. Smith for an exam and cleaning at our Main Street office.'\n"
         "• Automatically triggers Twilio SMS with a calendar link (.ics), clinic address, and digital health history intake form link."),

        ("Step 8: Post-Call Analytics & Doctor Alert",
         "• AI generates a clean structured clinical summary: SOAP note draft (Subjective complaint), patient contact details, insurance info.\n"
         "• Pushes notification to Doctor / Clinic Manager Portal via Webhook / Email / Slack.")
    ]

    for title, details in wf_steps:
        add_custom_heading_2(title)
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(4)
        p.add_run(details)

    # -------------------------------------------------------------
    # SECTION 5: CAN WE BUILD THIS AGENT? (IMPLEMENTATION PLAN)
    # -------------------------------------------------------------
    add_custom_heading_1("5. Implementation Blueprint: How We Can Build It")

    p = doc.add_paragraph()
    p.add_run("Yes, we can build a fully operational, production-ready AI Dental Voice Receptionist. Below is the exact architecture, technology stack, and step-by-step roadmap to execute this project:")

    add_custom_heading_2("5.1 Recommended Production Tech Stack")

    tech_headers = ["Layer / Module", "Recommended Technology", "Purpose & Key Capabilities"]
    tech_data = [
        ["Telephony Provider", "Twilio Elastic SIP / Telnyx", "Inbound/Outbound phone numbers, WebRTC media streams, SIP call bridging."],
        ["Voice Gateway", "LiveKit Voice Agent / Retell AI / Vapi", "Sub-500ms audio streaming, VAD (Voice Activity Detection), interruptibility handling."],
        ["Speech-to-Text (STT)", "Deepgram Nova-2 Medical", "Ultra-fast (<150ms) speech recognition trained on medical & dental vocabulary."],
        ["LLM Brain", "OpenAI GPT-4o / Anthropic Claude 3.5 Sonnet", "High-accuracy tool calling, natural empathy, dental triage rules, slot negotiation."],
        ["Text-to-Speech (TTS)", "Cartesia Sonic / ElevenLabs Flash", "Hyper-realistic voice cloning with natural cadence, breathing pauses, and low latency."],
        ["Backend & API", "FastAPI (Python) / Node.js TypeScript", "Asynchronous webhook management, PMS API connectors, business logic orchestration."],
        ["Dental PMS Connector", "Open Dental API / NexHealth Universal API", "Bidirectional reading/writing of provider schedules, chairs, and patient charts."],
        ["Database & Caching", "PostgreSQL + Redis", "Session state storage, caller history caching, temporary slot reservation locks."],
        ["Security & Compliance", "AWS HIPAA Architecture / Cloudflare Zero Trust", "End-to-end encryption, BAA compliance, PHI redaction from call transcripts."]
    ]

    tech_tbl = doc.add_table(rows=len(tech_data) + 1, cols=len(tech_headers))
    style_table(tech_tbl, [1.5, 2.0, 3.0], tech_headers, tech_data)

    add_custom_heading_2("5.2 Phased Development Roadmap")

    phases = [
        ("Phase 1: Conversational Design & Dental Knowledge Base", 
         "Define dental service taxonomy, provider schedule rules (operatory mapping, treatment duration buffers), emergency red flags, and prompt personas."),
        
        ("Phase 2: Voice Pipeline & Telephony Integration", 
         "Set up Twilio phone number, configure WebSockets audio streaming to LiveKit / Retell server, integrate Deepgram STT and Cartesia/ElevenLabs TTS."),
        
        ("Phase 3: Dental PMS & Calendar Tool Integration", 
         "Develop custom API integrations with Open Dental / Dentrix / NexHealth or Google Calendar API. Implement get_doctor_availability, hold_slot, and confirm_booking tools."),
        
        ("Phase 4: Triage Logic & Live Call Transfer Fallback", 
         "Implement intelligent urgency detection. If caller reports emergency symptoms or requests a human receptionist, execute an automated SIP warm transfer."),
        
        ("Phase 5: HIPAA Hardening, Testing & Deployment", 
         "Sign BAAs with all API vendors, implement audio & text PHI scrubbing, run end-to-end call testing with simulated patients, and deploy on production cloud.")
    ]

    for p_title, p_desc in phases:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(4)
        p.add_run(f"• {p_title}: ").bold = True
        p.add_run(p_desc)

    # -------------------------------------------------------------
    # SECTION 6: FUNCTION CALLING SPECIFICATIONS (CODE SCHEMA)
    # -------------------------------------------------------------
    add_custom_heading_1("6. Core Function Calling / Tool Schemas")

    p = doc.add_paragraph()
    p.add_run("The LLM interacts with the dental database using standard JSON Schema function definitions. Below are the key tools executed during a live call:")

    add_custom_heading_2("6.1 Tool: check_doctor_availability")
    
    code_box1 = doc.add_table(rows=1, cols=1)
    code_box1.alignment = WD_TABLE_ALIGNMENT.CENTER
    c1 = code_box1.cell(0,0)
    set_cell_background(c1, HEX_BG_LIGHT)
    set_cell_margins(c1, 100, 100, 140, 140)
    p1 = c1.paragraphs[0]
    p1.paragraph_format.space_before = Pt(0)
    p1.paragraph_format.space_after = Pt(0)
    r1 = p1.add_run(
"""{
  "name": "check_doctor_availability",
  "description": "Checks available dental appointment slots for a specific doctor or procedure type.",
  "parameters": {
    "type": "object",
    "properties": {
      "doctor_id": {"type": "string", "description": "Optional specific doctor ID (e.g., 'dr_smith')"},
      "procedure_type": {
        "type": "string",
        "enum": ["cleaning_prophylaxis", "emergency_pain", "consultation", "root_canal", "crown", "whitening"],
        "description": "Category of dental procedure"
      },
      "preferred_date": {"type": "string", "description": "Date in YYYY-MM-DD format"},
      "time_preference": {"type": "string", "enum": ["morning", "afternoon", "any"]}
    },
    "required": ["procedure_type", "preferred_date"]
  }
}"""
    )
    r1.font.name = "Consolas"
    r1.font.size = Pt(8.5)
    r1.font.color.rgb = COLOR_DARK

    add_custom_heading_2("6.2 Tool: book_dental_appointment")
    
    code_box2 = doc.add_table(rows=1, cols=1)
    code_box2.alignment = WD_TABLE_ALIGNMENT.CENTER
    c2 = code_box2.cell(0,0)
    set_cell_background(c2, HEX_BG_LIGHT)
    set_cell_margins(c2, 100, 100, 140, 140)
    p2 = c2.paragraphs[0]
    p2.paragraph_format.space_before = Pt(0)
    p2.paragraph_format.space_after = Pt(0)
    r2 = p2.add_run(
"""{
  "name": "book_dental_appointment",
  "description": "Confirms and writes a booked dental appointment into the clinic PMS calendar.",
  "parameters": {
    "type": "object",
    "properties": {
      "patient_first_name": {"type": "string"},
      "patient_last_name": {"type": "string"},
      "patient_phone": {"type": "string"},
      "patient_dob": {"type": "string", "description": "YYYY-MM-DD"},
      "doctor_id": {"type": "string"},
      "slot_start_time": {"type": "string", "description": "ISO 8601 timestamp"},
      "procedure_type": {"type": "string"},
      "insurance_provider": {"type": "string", "description": "e.g. Delta Dental, MetLife, Self-Pay"},
      "clinical_notes": {"type": "string", "description": "Patient symptoms or special requests"}
    },
    "required": ["patient_first_name", "patient_last_name", "patient_phone", "doctor_id", "slot_start_time", "procedure_type"]
  }
}"""
    )
    r2.font.name = "Consolas"
    r2.font.size = Pt(8.5)
    r2.font.color.rgb = COLOR_DARK

    # -------------------------------------------------------------
    # SECTION 7: HIPAA COMPLIANCE & CLINICAL GOVERNANCE
    # -------------------------------------------------------------
    add_custom_heading_1("7. HIPAA Compliance, Security & Clinical Governance")

    p = doc.add_paragraph()
    p.add_run("Deploying an AI agent in healthcare requires adherence to strict data privacy and clinical safety standards:")

    hipaa_points = [
        ("Business Associate Agreements (BAAs)", "Executed with Twilio, AWS/GCP, Deepgram, and OpenAI to ensure all PHI (Protected Health Information) processing is compliant."),
        ("Zero-Retention Voice Logging", "Audio recordings and transcription logs containing patient names, medical histories, and phone numbers are scrubbed or stored only in encrypted, HIPAA-compliant databases with auto-expiration policies."),
        ("Clinical Triage Safety Safeguards", "The AI is strictly bounded by clinical prompt safeguards: it never provides diagnostic or medical advice, but rather categorizes symptoms to route patients to the correct dentist."),
        ("Fail-Safe Live Call Forwarding", "If the caller expresses distress, confusion, or severe dental trauma, the voice agent smoothly announces a transfer and initiates an immediate PSTN/SIP bridge to the dental clinic front desk.")
    ]

    for title, desc in hipaa_points:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(4)
        r_t = p.add_run(f"• {title}: ")
        r_t.bold = True
        r_t.font.color.rgb = COLOR_PRIMARY
        p.add_run(desc)

    # -------------------------------------------------------------
    # SECTION 8: CONCLUSION & NEXT STEPS
    # -------------------------------------------------------------
    add_custom_heading_1("8. Next Steps & Kickoff")

    p = doc.add_paragraph()
    p.add_run("We are ready to proceed with building this AI Dental Receptionist for your specific requirements. To kick off implementation, we can immediately begin with:\n\n"
              "1. Target PMS Selection: Confirm whether your target clinic uses Open Dental, Dentrix, Eaglesoft, NexHealth, or Google Calendar.\n"
              "2. Voice Platform Architecture: Deploy the core FastAPI + Twilio + Retell/LiveKit voice bridge on your cloud.\n"
              "3. Custom Clinic Prompt Tuning: Load doctor profiles, operatory configurations, pricing sheets, and accepted insurance plans into the agent's knowledge base.\n\n"
              "Let me know if you would like me to generate the backend starter codebase (FastAPI + Twilio Voice Webhook + Dental PMS Tool Calling)!")

    # Save document
    doc.save(output_path)
    print(f"Document saved successfully to: {output_path}")

if __name__ == "__main__":
    output_file = r"C:\Users\huwai\.gemini\antigravity\scratch\AI_Dental_Manager_Scheduling_Agent_Architecture.docx"
    create_dental_ai_document(output_file)
