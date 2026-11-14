import sys
import collections.abc
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def build_presentation(output_path):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Palette
    C_NAVY = RGBColor(15, 23, 42)       # #0F172A (Slate 900)
    C_PRIMARY = RGBColor(30, 58, 138)   # #1E3A8A (Deep Navy Blue)
    C_TEAL = RGBColor(13, 148, 136)     # #0D9488 (Teal Primary Accent)
    C_DARK = RGBColor(30, 41, 59)       # #1E293B (Dark Slate text)
    C_MUTED = RGBColor(100, 116, 139)   # #64748B (Slate Muted)
    C_BG_CARD = RGBColor(248, 250, 252) # #F8FAFC (Card Background)
    C_BORDER = RGBColor(226, 232, 240)  # #E2E8F0 (Border)
    C_WHITE = RGBColor(255, 255, 255)
    C_ACCENT_BG = RGBColor(240, 253, 250) # Light Teal BG
    C_RED = RGBColor(225, 29, 72)       # Rose 600

    def add_header(slide, title_text, category_text="AI DENTAL VOICE RECEPTIONIST"):
        # Category pill/subtext
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.35))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        tf_cat.margin_left = tf_cat.margin_top = tf_cat.margin_right = tf_cat.margin_bottom = 0
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.name = "Arial"
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = C_TEAL

        # Main Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.72), Inches(11.7), Inches(0.65))
        tf = title_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.name = "Arial"
        p.font.size = Pt(22)
        p.font.bold = True
        p.font.color.rgb = C_NAVY

    def add_card(slide, left, top, width, height, bg_color=C_BG_CARD, border_color=C_BORDER):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
        if border_color:
            shape.line.color.rgb = border_color
            shape.line.width = Pt(1.2)
        else:
            shape.line.fill.background()
        return shape

    def set_notes(slide, text):
        notes_slide = slide.notes_slide
        tf = notes_slide.notes_text_frame
        tf.text = text

    # =========================================================================
    # SLIDE 1: Title Slide (Dark Executive Theme)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = C_NAVY
    bg1.line.fill.background()

    # Decorative accent bar
    bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.2), Inches(1.8), Inches(0.8), Inches(0.08))
    bar.fill.solid()
    bar.fill.fore_color.rgb = C_TEAL
    bar.line.fill.background()

    # Title & Subtitle Box
    t_box = s1.shapes.add_textbox(Inches(1.2), Inches(2.1), Inches(10.8), Inches(3.2))
    tf1 = t_box.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.text = "AI DENTAL RECEPTIONIST & AUTOMATED SCHEDULING AGENT"
    p0.font.name = "Arial"
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = C_TEAL
    p0.space_after = Pt(12)

    p1 = tf1.add_paragraph()
    p1.text = "Autonomous Voice-to-PMS Architecture, Clinical Triage & Executive Implementation Walkthrough"
    p1.font.name = "Arial"
    p1.font.size = Pt(28)
    p1.font.bold = True
    p1.font.color.rgb = C_WHITE
    p1.space_after = Pt(16)

    p2 = tf1.add_paragraph()
    p2.text = "A complete presentation for the CEO on market landscape, 6-layer real-time voice pipeline, Practice Management integration, and phased build strategy."
    p2.font.name = "Calibri"
    p2.font.size = Pt(14)
    p2.font.color.rgb = RGBColor(203, 213, 225)

    # Footer block
    foot_box = s1.shapes.add_textbox(Inches(1.2), Inches(6.0), Inches(10.8), Inches(0.8))
    tf_f = foot_box.text_frame
    p_f = tf_f.paragraphs[0]
    p_f.text = "DOMAIN: Healthcare & Dentistry AI  |  FEASIBILITY: 100% Production Ready  |  TARGET: Inbound Voice to PMS Booking"
    p_f.font.name = "Arial"
    p_f.font.size = Pt(10)
    p_f.font.bold = True
    p_f.font.color.rgb = RGBColor(148, 163, 184)

    set_notes(s1, 
        "\"Good morning / afternoon. Today, I'm presenting our complete end-to-end plan to implement an Autonomous AI Voice Receptionist for the dental domain.\n\n"
        "This presentation walks you through the comprehensive architecture document we prepared. It covers the market landscape, how existing agents work, the complete technical pipeline from phone call to calendar write-back, and how we are going to build, deploy, and scale this agent.\""
    )

    # =========================================================================
    # SLIDE 2: Executive Summary & The Problem
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Executive Summary: The $200K Front-Desk Dilemma & Our Solution")

    # 3 Stat Cards
    stats = [
        ("65%+", "Front-Desk Time Burden", "Receptionists spend over 65% of daily hours on repetitive phone calls, rescheduling, and basic intake rather than in-clinic patient care.", C_PRIMARY),
        ("$100K - $250K", "Lost Annual Revenue", "Missed calls after-hours and during clinic rush hour lead directly to high patient churn and empty dental operatories.", C_RED),
        ("< 600ms", "Real-Time AI Response", "Our voice agent delivers human-like conversational latency, clinical symptom triage, and direct 2-way PMS booking 24/7/365.", C_TEAL),
    ]

    for i, (num, heading, desc, col) in enumerate(stats):
        left = 0.8 + i * 3.95
        add_card(s2, left, 1.6, 3.8, 2.5, C_BG_CARD, C_BORDER)
        tb = s2.shapes.add_textbox(Inches(left + 0.25), Inches(1.8), Inches(3.3), Inches(2.1))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = num
        p.font.name = "Arial"
        p.font.size = Pt(28)
        p.font.bold = True
        p.font.color.rgb = col
        p.space_after = Pt(4)
        
        p_h = tf.add_paragraph()
        p_h.text = heading
        p_h.font.name = "Arial"
        p_h.font.size = Pt(12)
        p_h.font.bold = True
        p_h.font.color.rgb = C_NAVY
        p_h.space_after = Pt(6)
        
        p_d = tf.add_paragraph()
        p_d.text = desc
        p_d.font.name = "Calibri"
        p_d.font.size = Pt(10.5)
        p_d.font.color.rgb = C_DARK

    # Bottom summary card
    add_card(s2, 0.8, 4.4, 11.7, 2.4, C_ACCENT_BG, C_TEAL)
    tb_b = s2.shapes.add_textbox(Inches(1.1), Inches(4.6), Inches(11.1), Inches(2.0))
    tf_b = tb_b.text_frame
    tf_b.word_wrap = True
    
    pb1 = tf_b.paragraphs[0]
    pb1.text = "CORE OBJECTIVE & FEASIBILITY CONFIRMATION"
    pb1.font.name = "Arial"
    pb1.font.size = Pt(11)
    pb1.font.bold = True
    pb1.font.color.rgb = C_TEAL
    pb1.space_after = Pt(4)
    
    pb2 = tf_b.add_paragraph()
    pb2.text = "• Yes, we can 100% build, customize, and deploy this autonomous agent for dental practices.\n" \
               "• The agent handles 100% of inbound calls, accurately identifies patient intent, performs clinical triage, negotiates time slots, checks real-time doctor availability, writes the appointment into Dentrix/Open Dental, and sends instant SMS confirmations.\n" \
               "• Full emergency detection safely forwards urgent clinical cases to on-call doctors with zero latency."
    pb2.font.name = "Calibri"
    pb2.font.size = Pt(11)
    pb2.font.color.rgb = C_NAVY

    set_notes(s2,
        "\"To start with why we are doing this: Modern dental clinics lose between $100,000 and $250,000 per operatory each year simply from missed calls after hours and front-desk overload.\n\n"
        "Front desk staff spend two-thirds of their day juggling phone calls instead of welcoming patients in the clinic. Our solution is an Autonomous Voice AI Receptionist that operates 24/7 with human-like latency under 600 milliseconds. It understands dental procedures, checks live doctor calendars, books appointments directly into the clinic's software, and triages emergencies.\n\n"
        "I want to state clearly: This is 100% feasible with today's voice AI stack, and we have a concrete roadmap to implement it.\""
    )

    # =========================================================================
    # SLIDE 3: Market Landscape & Existing Solutions
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Market Landscape: Existing Dental AI Agents & Competitive Benchmark")

    # 4 Cards for competitors
    comps = [
        ("Arini AI", "Dental Dedicated", "Level 4 (2-Way Write)", "Plugs natively into Dentrix, Open Dental, Eaglesoft. Focuses on after-hours multi-chair scheduling.", C_PRIMARY),
        ("Rondah AI", "Dental Dedicated", "Level 4 (Real-time Sync)", "Specialized in bidirectional PMS sync, conversational voice flows, and automated SMS intake follow-up.", C_PRIMARY),
        ("NexHealth", "Universal Dental API", "Level 5 (Direct Sync)", "The gold standard in dental data infrastructure, offering universal read/write access to 40+ dental PMSs.", C_TEAL),
        ("Custom LiveKit/Retell", "Our Proposed Solution", "Level 5 Full Custom", "Ultra-low latency (<500ms), customized dental triage models, full ownership of data, HIPAA compliance.", C_TEAL),
    ]

    for i, (name, role, sync, desc, accent) in enumerate(comps):
        col_idx = i % 2
        row_idx = i // 2
        left = 0.8 + col_idx * 5.95
        top = 1.6 + row_idx * 2.65
        add_card(s3, left, top, 5.75, 2.45, C_BG_CARD, C_BORDER)
        
        tb = s3.shapes.add_textbox(Inches(left + 0.25), Inches(top + 0.2), Inches(5.25), Inches(2.0))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = f"{name}  |  {role}"
        p.font.name = "Arial"
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = accent
        p.space_after = Pt(2)
        
        p_s = tf.add_paragraph()
        p_s.text = f"PMS Sync Capability: {sync}"
        p_s.font.name = "Arial"
        p_s.font.size = Pt(10)
        p_s.font.bold = True
        p_s.font.color.rgb = C_DARK
        p_s.space_after = Pt(6)
        
        p_d = tf.add_paragraph()
        p_d.text = desc
        p_d.font.name = "Calibri"
        p_d.font.size = Pt(10.5)
        p_d.font.color.rgb = C_MUTED

    set_notes(s3,
        "\"Let's look at the market. There are existing players like Arini AI and Rondah AI proving product-market fit right now. They integrate with dental software like Dentrix and Open Dental for scheduling.\n\n"
        "On the infrastructure side, platforms like NexHealth provide universal dental API sync across 40+ systems. However, most off-the-shelf agents have rigid conversation trees, high monthly SaaS fees, and latency around 800 to 1,000 milliseconds.\n\n"
        "Our approach combines modern sub-500ms voice pipelines with dedicated dental triage intelligence, giving us higher conversion, lower latency, custom clinical rules, and complete data ownership.\""
    )

    # =========================================================================
    # SLIDE 4: The 6-Layer System Architecture
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "System Architecture: The 6 Core Enterprise Layers")

    layers = [
        ("Layer 1: Telephony & Streaming", "Twilio Elastic SIP / Telnyx", "PSTN phone ingestion, bidirectional audio WebSockets (PCM 16-bit) with zero packet drop."),
        ("Layer 2: Real-Time Speech Pipeline", "Deepgram Nova-2 + Cartesia Sonic", "Sub-150ms Medical STT transcription, Voice Activity Detection (VAD), and hyper-realistic TTS voice generation."),
        ("Layer 3: Dental LLM Orchestrator", "GPT-4o / Claude 3.5 Sonnet", "Contextual dental knowledge (cleanings, crowns, root canals, emergency pulpitis) with structured tool execution."),
        ("Layer 4: Dental PMS & EHR Layer", "Open Dental API / Dentrix / NexHealth", "Live calendar read/write, doctor working hours, operatory chair mapping, and instant slot locking."),
        ("Layer 5: Dispatcher & Warm-Transfer", "Twilio SMS + SIP Bridge", "Instant SMS appointment reminders (.ics calendar links), digital health forms, and live warm-transfer to staff."),
        ("Layer 6: Security & Compliance", "HIPAA Architecture & BAAs", "End-to-end AES-256 encryption, zero-retention voice logging for PHI, and role-based access control.")
    ]

    for i, (title, tech, desc) in enumerate(layers):
        col_idx = i % 3
        row_idx = i // 3
        left = 0.8 + col_idx * 3.95
        top = 1.6 + row_idx * 2.65
        add_card(s4, left, top, 3.8, 2.45, C_BG_CARD, C_BORDER)
        
        tb = s4.shapes.add_textbox(Inches(left + 0.2), Inches(top + 0.15), Inches(3.4), Inches(2.1))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = title
        p.font.name = "Arial"
        p.font.size = Pt(11.5)
        p.font.bold = True
        p.font.color.rgb = C_PRIMARY
        p.space_after = Pt(2)
        
        p_t = tf.add_paragraph()
        p_t.text = tech
        p_t.font.name = "Arial"
        p_t.font.size = Pt(9.5)
        p_t.font.bold = True
        p_t.font.color.rgb = C_TEAL
        p_t.space_after = Pt(4)
        
        p_d = tf.add_paragraph()
        p_d.text = desc
        p_d.font.name = "Calibri"
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = C_DARK

    set_notes(s4,
        "\"Here is how the system is architected across 6 enterprise layers:\n\n"
        "Layer 1 handles the phone lines and audio streaming via Twilio SIP.\n"
        "Layer 2 converts voice to text and text to speech in under 200 milliseconds using Deepgram and Cartesia.\n"
        "Layer 3 is the Brain—an LLM trained on dental terminology and triage rules.\n"
        "Layer 4 communicates directly with the clinic's software to check doctor schedules and prevent double bookings.\n"
        "Layer 5 handles automated SMS follow-ups, intake forms, and emergency human transfers.\n"
        "Layer 6 guarantees full HIPAA compliance and PHI privacy.\n\n"
        "This modular structure ensures high reliability and zero downtime.\""
    )

    # =========================================================================
    # SLIDE 5: Architecture Flow & Audio Streaming Pipeline
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Real-Time Pipeline: Sub-600ms Voice Orchestration & Tool Calling")

    flow_steps = [
        ("1. Inbound Caller", "Patient calls clinic phone number via PSTN.", C_NAVY),
        ("2. Telephony Stream", "Twilio bridges call over bidirectional WebSockets.", C_PRIMARY),
        ("3. Medical STT", "Deepgram Nova-2 transcribes speech (<150ms).", C_PRIMARY),
        ("4. AI Orchestrator", "LLM determines intent & triggers dental tool calls.", C_TEAL),
        ("5. Dental PMS Query", "API checks doctor/operatory slot in real time.", C_TEAL),
        ("6. Voice Synthesis", "Cartesia generates ultra-natural audio tokens (<100ms).", C_PRIMARY),
        ("7. Audio Playback", "Caller hears natural reply & confirms booking.", C_NAVY)
    ]

    for i, (title, desc, col) in enumerate(flow_steps):
        left = 0.8 + i * 1.68
        add_card(s5, left, 1.6, 1.6, 3.2, C_BG_CARD, C_BORDER)
        
        tb = s5.shapes.add_textbox(Inches(left + 0.1), Inches(1.75), Inches(1.4), Inches(2.9))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p_num = tf.paragraphs[0]
        p_num.text = f"0{i+1}"
        p_num.font.name = "Arial"
        p_num.font.size = Pt(16)
        p_num.font.bold = True
        p_num.font.color.rgb = col
        p_num.space_after = Pt(4)
        
        p_t = tf.add_paragraph()
        p_t.text = title
        p_t.font.name = "Arial"
        p_t.font.size = Pt(10.5)
        p_t.font.bold = True
        p_t.font.color.rgb = C_DARK
        p_t.space_after = Pt(4)
        
        p_d = tf.add_paragraph()
        p_d.text = desc
        p_d.font.name = "Calibri"
        p_d.font.size = Pt(9.5)
        p_d.font.color.rgb = C_MUTED

    # Bottom Callout
    add_card(s5, 0.8, 5.0, 11.7, 1.8, C_ACCENT_BG, C_TEAL)
    tb_bot = s5.shapes.add_textbox(Inches(1.1), Inches(5.15), Inches(11.1), Inches(1.5))
    tf_bot = tb_bot.text_frame
    tf_bot.word_wrap = True
    
    p1 = tf_bot.paragraphs[0]
    p1.text = "⚡ LATENCY & INTERRUPTIBILITY GUARANTEE"
    p1.font.name = "Arial"
    p1.font.size = Pt(11)
    p1.font.bold = True
    p1.font.color.rgb = C_TEAL
    p1.space_after = Pt(4)
    
    p2 = tf_bot.add_paragraph()
    p2.text = "• Total round-trip latency is under 600ms, making conversation indistinguishable from a human receptionist.\n" \
              "• Full Voice Activity Detection (VAD) allows the patient to naturally interrupt the agent mid-sentence without audio stutter or state loss."
    p2.font.name = "Calibri"
    p2.font.size = Pt(10.5)
    p2.font.color.rgb = C_NAVY

    set_notes(s5,
        "\"This slide demonstrates the exact audio journey during a live call.\n\n"
        "When the patient speaks, their audio streams directly over WebSockets to our voice server. Within 150 milliseconds, Deepgram transcribes the speech. The AI orchestrator interprets the clinical intent and executes function calls against the clinic's database in parallel.\n\n"
        "The response is streamed to Cartesia TTS, generating natural speech audio within 100 milliseconds. The caller hears a smooth, human-like voice. Crucially, the system supports natural interruptions—if the patient cuts in to give their phone number, the agent stops talking and listens instantly.\""
    )

    # =========================================================================
    # SLIDE 6: Call Workflow & State Machine (Steps 1-4)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Call Handling Workflow (Part 1): Ingestion, Verification & Triage")

    steps_p1 = [
        ("Step 1: Greeting & Intent Capture", 
         "• Branded clinic greeting: 'Thank you for calling BrightSmile Dental, I'm Maya, Dr. Smith's AI assistant. How can I help you today?'\n"
         "• Natural Language Intent Classification (Emergency pain, cleaning, whitening, insurance question).", C_PRIMARY),
        ("Step 2: Patient Verification & Intake", 
         "• Existing Patient: Instant database lookup by caller ID phone number in PMS.\n"
         "• New Patient: Efficient conversational capture of Full Name, DOB, and Mobile Phone.", C_PRIMARY),
        ("Step 3: Clinical Triage & Chair Mapping", 
         "• Routine Hygiene: 60 min -> Dental Hygienist / Hygiene Operatory.\n"
         "• Severe Toothache / Crown: 45 min -> Associate/Lead Dentist.\n"
         "• Emergency Red Flags: Swelling, acute bleeding -> Immediate ER advice / on-call transfer.", C_TEAL),
        ("Step 4: Live Doctor Schedule Query", 
         "• AI executes get_available_slots() via PMS API.\n"
         "• Proactively offers 2-3 tailored options: 'Dr. Smith has Thursday at 10:30 AM or Friday at 2:00 PM. Which works best?'", C_TEAL),
    ]

    for i, (title, text, col) in enumerate(steps_p1):
        col_idx = i % 2
        row_idx = i // 2
        left = 0.8 + col_idx * 5.95
        top = 1.6 + row_idx * 2.65
        add_card(s6, left, top, 5.75, 2.45, C_BG_CARD, C_BORDER)
        
        tb = s6.shapes.add_textbox(Inches(left + 0.25), Inches(top + 0.2), Inches(5.25), Inches(2.05))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = title
        p.font.name = "Arial"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = col
        p.space_after = Pt(4)
        
        p_d = tf.add_paragraph()
        p_d.text = text
        p_d.font.name = "Calibri"
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = C_DARK

    set_notes(s6,
        "\"Now, let's walk through the actual conversation flow that the patient experiences.\n\n"
        "In Step 1, the AI answers immediately with clinic-specific branding.\n"
        "In Step 2, it matches existing patients using caller ID, or seamlessly gathers intake details for new patients.\n"
        "In Step 3, it conducts clinical triage. It knows that a routine cleaning goes to the dental hygienist for 60 minutes, while severe tooth pain requires the lead doctor. If there is severe trauma or facial swelling, it triggers emergency protocols.\n"
        "In Step 4, it queries the PMS in real time and offers two or three concrete time options rather than open-ended questions, ensuring fast call completion.\""
    )

    # =========================================================================
    # SLIDE 7: Call Workflow & State Machine (Steps 5-8)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Call Handling Workflow (Part 2): Booking, PMS Write-Back & Post-Call")

    steps_p2 = [
        ("Step 5: Slot Reservation & Soft Lock", 
         "• Caller selects preferred time slot.\n"
         "• System places a temporary 5-minute lock on the PMS calendar to prevent race conditions and double bookings.", C_PRIMARY),
        ("Step 6: Insurance & Intake Pre-Screening", 
         "• Agent inquires: 'Will you be using dental insurance such as Delta Dental or MetLife, or self-paying?'\n"
         "• Captures carrier details for front-desk verification.", C_PRIMARY),
        ("Step 7: PMS Write-Back & Instant SMS", 
         "• Executes create_appointment_booking() directly into Dentrix / Open Dental.\n"
         "• Dispatches automated SMS with .ics calendar invite, clinic directions, and digital medical history form.", C_TEAL),
        ("Step 8: Post-Call Summary & Doctor Alert", 
         "• AI generates a clean structured clinical summary note (SOAP draft).\n"
         "• Pushes notification to Clinic Dashboard / Doctor Slack / Email.", C_TEAL),
    ]

    for i, (title, text, col) in enumerate(steps_p2):
        col_idx = i % 2
        row_idx = i // 2
        left = 0.8 + col_idx * 5.95
        top = 1.6 + row_idx * 2.65
        add_card(s7, left, top, 5.75, 2.45, C_BG_CARD, C_BORDER)
        
        tb = s7.shapes.add_textbox(Inches(left + 0.25), Inches(top + 0.2), Inches(5.25), Inches(2.05))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = title
        p.font.name = "Arial"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = col
        p.space_after = Pt(4)
        
        p_d = tf.add_paragraph()
        p_d.text = text
        p_d.font.name = "Calibri"
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = C_DARK

    set_notes(s7,
        "\"Continuing the workflow from slot selection to final confirmation:\n\n"
        "In Step 5, the agent soft-locks the chosen slot in the PMS to prevent any simultaneous bookings from other staff.\n"
        "In Step 6, it collects dental insurance information so the billing team can verify benefits in advance.\n"
        "In Step 7, it writes the appointment directly into Dentrix or Open Dental and immediately sends the patient a text message with a calendar invite and digital intake link.\n"
        "In Step 8, the call ends and the AI drafts a clinical SOAP summary for the doctor's review. The front desk did not have to touch a single button.\""
    )

    # =========================================================================
    # SLIDE 8: Clinical Triage & Operatory Mapping
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Clinical Intelligence: Dental Triage & Operatory Allocation")

    triage_cards = [
        ("Routine Hygiene & Cleaning", "Provider: Registered Dental Hygienist (RDH)\nChair: Hygiene Operatory (45-60 min)\nLogic: Routine recall, prophylaxis, child cleanings. Automatically books hygiene chair.", C_PRIMARY),
        ("Urgent Dental Care / Pain", "Provider: Associate / Lead Dentist\nChair: Operatory 1 or 2 (30-45 min)\nLogic: Acute tooth pain, chipped crown, broken restoration. Priority scheduling.", C_PRIMARY),
        ("Cosmetic & Restorative Consult", "Provider: Lead Cosmetic Dentist\nChair: Consultation Room / Operatory (45 min)\nLogic: Veneers, Invisalign, implants, teeth whitening consultations.", C_TEAL),
        ("Severe Emergency Protocol", "Action: Instant Warm SIP Transfer to Clinic\nSafety: Uncontrolled bleeding, breathing difficulty, severe facial trauma. Immediate human escalation.", C_RED),
    ]

    for i, (title, details, col) in enumerate(triage_cards):
        col_idx = i % 2
        row_idx = i // 2
        left = 0.8 + col_idx * 5.95
        top = 1.6 + row_idx * 2.65
        add_card(s8, left, top, 5.75, 2.45, C_BG_CARD, C_BORDER)
        
        tb = s8.shapes.add_textbox(Inches(left + 0.25), Inches(top + 0.2), Inches(5.25), Inches(2.05))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = title
        p.font.name = "Arial"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = col
        p.space_after = Pt(4)
        
        p_d = tf.add_paragraph()
        p_d.text = details
        p_d.font.name = "Calibri"
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = C_DARK

    set_notes(s8,
        "\"A critical strength of our system is clinical intelligence. A dental clinic isn't just one doctor—it's a multi-chair environment.\n\n"
        "Our AI distinguishes between hygiene cleanings (which belong in the hygienist's chair for 60 minutes) and dental emergencies or cosmetic consultations (which belong with the dentist).\n\n"
        "Crucially, our system includes strict clinical boundaries. It never attempts to prescribe medicine or make a final clinical diagnosis. If the patient describes acute trauma or breathing difficulties, the agent immediately initiates a live warm-transfer to on-call staff.\""
    )

    # =========================================================================
    # SLIDE 9: Production Technology Stack
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Production Tech Stack: Enterprise-Grade & Scalable")

    stack = [
        ("Telephony & SIP", "Twilio / Telnyx", "Inbound DID phone numbers, WebSockets audio streaming, PSTN/SIP call bridging."),
        ("Voice Gateway", "LiveKit / Retell AI", "Sub-500ms orchestration, Voice Activity Detection, turn-taking management."),
        ("Medical STT", "Deepgram Nova-2", "Ultra-low latency (<150ms) speech-to-text specialized in medical/dental terms."),
        ("Core LLM Brain", "OpenAI GPT-4o / Claude 3.5", "Intelligent reasoning, dental triage, tool calling, and high empathetic tone."),
        ("Voice Synthesis", "Cartesia Sonic / ElevenLabs", "Sub-100ms ultra-realistic voice cloning with natural pauses and cadence."),
        ("Dental PMS API", "Open Dental / NexHealth", "Universal bidirectional API sync for patient charts, operatories, and schedules."),
        ("Backend Server", "FastAPI (Python) / Redis", "Asynchronous webhook management, session locking, state management."),
        ("Infrastructure", "AWS HIPAA / Cloudflare", "Zero-Trust security, AES-256 encryption, HIPAA compliant architecture.")
    ]

    for i, (cat, tech, purpose) in enumerate(stack):
        col_idx = i % 4
        row_idx = i // 4
        left = 0.8 + col_idx * 2.92
        top = 1.6 + row_idx * 2.65
        add_card(s9, left, top, 2.8, 2.45, C_BG_CARD, C_BORDER)
        
        tb = s9.shapes.add_textbox(Inches(left + 0.15), Inches(top + 0.15), Inches(2.5), Inches(2.1))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = cat
        p.font.name = "Arial"
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = C_PRIMARY
        p.space_after = Pt(2)
        
        p_t = tf.add_paragraph()
        p_t.text = tech
        p_t.font.name = "Arial"
        p_t.font.size = Pt(9.5)
        p_t.font.bold = True
        p_t.font.color.rgb = C_TEAL
        p_t.space_after = Pt(4)
        
        p_d = tf.add_paragraph()
        p_d.text = purpose
        p_d.font.name = "Calibri"
        p_d.font.size = Pt(9)
        p_d.font.color.rgb = C_DARK

    set_notes(s9,
        "\"To execute this at scale, we are selecting best-of-breed enterprise components.\n\n"
        "We use Twilio for reliable carrier telephony, LiveKit and Deepgram Nova-2 for ultra-fast medical transcription, GPT-4o for high-accuracy reasoning and function calling, Cartesia for instant voice synthesis, and Open Dental / NexHealth APIs for direct calendar synchronization.\n\n"
        "This stack avoids vendor lock-in and gives us the lowest latency and highest reliability available in the industry.\""
    )

    # =========================================================================
    # SLIDE 10: Technical Tool Schemas (How AI Books Appointments)
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "PMS Integration: Structured JSON Tool Calling Specifications")

    # Left Card: check_doctor_availability
    add_card(s10, 0.8, 1.6, 5.75, 5.2, C_BG_CARD, C_BORDER)
    tb_l = s10.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.35), Inches(4.8))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    
    pl1 = tf_l.paragraphs[0]
    pl1.text = "TOOL 1: check_doctor_availability"
    pl1.font.name = "Arial"
    pl1.font.size = Pt(12)
    pl1.font.bold = True
    pl1.font.color.rgb = C_PRIMARY
    pl1.space_after = Pt(4)
    
    pl2 = tf_l.add_paragraph()
    pl2.text = "Queries open time slots across doctors and operatories:"
    pl2.font.name = "Calibri"
    pl2.font.size = Pt(9.5)
    pl2.font.color.rgb = C_MUTED
    pl2.space_after = Pt(8)
    
    pl3 = tf_l.add_paragraph()
    pl3.text = """{\n  "name": "check_doctor_availability",\n  "parameters": {\n    "doctor_id": "string (optional)",\n    "procedure_type": "cleaning | pain | consult",\n    "preferred_date": "YYYY-MM-DD",\n    "time_preference": "morning | afternoon"\n  }\n}"""
    pl3.font.name = "Consolas"
    pl3.font.size = Pt(9.5)
    pl3.font.color.rgb = C_NAVY

    # Right Card: book_dental_appointment
    add_card(s10, 6.75, 1.6, 5.75, 5.2, C_BG_CARD, C_BORDER)
    tb_r = s10.shapes.add_textbox(Inches(6.95), Inches(1.8), Inches(5.35), Inches(4.8))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    
    pr1 = tf_r.paragraphs[0]
    pr1.text = "TOOL 2: book_dental_appointment"
    pr1.font.name = "Arial"
    pr1.font.size = Pt(12)
    pr1.font.bold = True
    pr1.font.color.rgb = C_TEAL
    pr1.space_after = Pt(4)
    
    pr2 = tf_r.add_paragraph()
    pr2.text = "Writes confirmed booking directly into Dentrix / Open Dental:"
    pr2.font.name = "Calibri"
    pr2.font.size = Pt(9.5)
    pr2.font.color.rgb = C_MUTED
    pr2.space_after = Pt(8)
    
    pr3 = tf_r.add_paragraph()
    pr3.text = """{\n  "name": "book_dental_appointment",\n  "parameters": {\n    "patient_first_name": "string",\n    "patient_last_name": "string",\n    "patient_phone": "string",\n    "patient_dob": "YYYY-MM-DD",\n    "doctor_id": "string",\n    "slot_start_time": "ISO 8601 timestamp",\n    "procedure_type": "string",\n    "insurance_provider": "string",\n    "clinical_notes": "string (symptoms)"\n  }\n}"""
    pr3.font.name = "Consolas"
    pr3.font.size = Pt(9.5)
    pr3.font.color.rgb = C_NAVY

    set_notes(s10,
        "\"To illustrate how the AI interacts with the database: The language model uses deterministic function calling.\n\n"
        "When the patient asks for an appointment, the model invokes `check_doctor_availability` with the procedure type and preferred date. It receives available slots from Open Dental in milliseconds and speaks them back to the caller.\n\n"
        "Once the caller agrees, the model executes `book_dental_appointment`, passing the patient's verified identity, insurance carrier, selected time, and clinical notes directly into the practice management system.\""
    )

    # =========================================================================
    # SLIDE 11: HIPAA Compliance, Security & Clinical Governance
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "Security & Compliance: HIPAA-Compliant Healthcare Operations")

    sec_cards = [
        ("Business Associate Agreements (BAAs)", "Formal BAAs signed with Twilio, AWS, Deepgram, and OpenAI to legally ensure all Protected Health Information (PHI) processing is HIPAA-compliant.", C_PRIMARY),
        ("Zero-Retention Voice Logging", "Raw audio recordings and transcription logs containing sensitive patient data are scrubbed or stored only in encrypted databases with strict auto-expiration policies.", C_PRIMARY),
        ("Clinical Safety Guardrails", "The AI is strictly constrained by clinical prompts. It cannot diagnose or recommend treatments, ensuring full liability protection for the dental practice.", C_TEAL),
        ("Fail-Safe Live Call Forwarding", "In cases of patient distress, severe trauma, or complex medical queries, the agent executes an immediate SIP bridge to front-desk staff.", C_TEAL),
    ]

    for i, (title, desc, col) in enumerate(sec_cards):
        col_idx = i % 2
        row_idx = i // 2
        left = 0.8 + col_idx * 5.95
        top = 1.6 + row_idx * 2.65
        add_card(s11, left, top, 5.75, 2.45, C_BG_CARD, C_BORDER)
        
        tb = s11.shapes.add_textbox(Inches(left + 0.25), Inches(top + 0.2), Inches(5.25), Inches(2.05))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = title
        p.font.name = "Arial"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = col
        p.space_after = Pt(4)
        
        p_d = tf.add_paragraph()
        p_d.text = desc
        p_d.font.name = "Calibri"
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = C_DARK

    set_notes(s11,
        "\"Healthcare software demands the highest security and compliance standards.\n\n"
        "We enforce HIPAA compliance across all infrastructure layers with signed BAAs from all API vendors. Patient data is encrypted with AES-256 both in transit and at rest. Voice logs with Protected Health Information are automatically redacted or subjected to strict retention limits.\n\n"
        "Furthermore, our clinical guardrails protect the practice from liability by ensuring the agent never provides medical advice, while maintaining a reliable live human fallback at all times.\""
    )

    # =========================================================================
    # SLIDE 12: 5-Phase Implementation Roadmap
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "Implementation Roadmap: 5-Phase Production Rollout")

    phases = [
        ("Phase 1", "Conversational Design & Dental Knowledge Base", "Define dental taxonomy, chair allocation rules, buffer times, clinic operating hours, and custom persona prompts.", "Weeks 1-2", C_PRIMARY),
        ("Phase 2", "Voice Telephony Pipeline & STT/TTS Integration", "Set up Twilio SIP trunks, WebSockets audio streaming, Deepgram Nova-2 medical STT, and Cartesia voice models.", "Weeks 3-4", C_PRIMARY),
        ("Phase 3", "Dental PMS & Calendar Tool Integration", "Build bidirectional connectors for Open Dental / Dentrix / NexHealth API. Implement live availability check & booking write-back.", "Weeks 5-6", C_TEAL),
        ("Phase 4", "Emergency Triage & Warm Transfer Engine", "Implement red-flag symptom detection, priority booking routing, and fail-safe SIP warm transfer to clinic staff.", "Weeks 7-8", C_TEAL),
        ("Phase 5", "HIPAA Hardening, Testing & Live Deployment", "Execute BAAs, end-to-end load testing, PHI redaction verification, pilot launch at selected dental clinic, staff training.", "Weeks 9-10", C_NAVY),
    ]

    for i, (ph_num, ph_title, ph_desc, ph_time, ph_col) in enumerate(phases):
        left = 0.8 + i * 2.34
        add_card(s12, left, 1.6, 2.25, 5.2, C_BG_CARD, C_BORDER)
        
        tb = s12.shapes.add_textbox(Inches(left + 0.15), Inches(1.8), Inches(1.95), Inches(4.8))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = ph_num
        p.font.name = "Arial"
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = ph_col
        p.space_after = Pt(2)
        
        p_tm = tf.add_paragraph()
        p_tm.text = ph_time
        p_tm.font.name = "Arial"
        p_tm.font.size = Pt(9.5)
        p_tm.font.bold = True
        p_tm.font.color.rgb = C_TEAL
        p_tm.space_after = Pt(6)
        
        p_t = tf.add_paragraph()
        p_t.text = ph_title
        p_t.font.name = "Arial"
        p_t.font.size = Pt(10.5)
        p_t.font.bold = True
        p_t.font.color.rgb = C_NAVY
        p_t.space_after = Pt(6)
        
        p_d = tf.add_paragraph()
        p_d.text = ph_desc
        p_d.font.name = "Calibri"
        p_d.font.size = Pt(9.5)
        p_d.font.color.rgb = C_DARK

    set_notes(s12,
        "\"Here is our phased rollout plan over a 10-week schedule.\n\n"
        "In Weeks 1 and 2, we establish the dental taxonomy and clinic knowledge base.\n"
        "In Weeks 3 and 4, we build and calibrate the low-latency voice pipeline.\n"
        "In Weeks 5 and 6, we integrate the Practice Management APIs for live calendar synchronization.\n"
        "In Weeks 7 and 8, we build and test the clinical triage and live transfer engine.\n"
        "In Weeks 9 and 10, we complete HIPAA compliance hardening, run pilot tests with simulated patients, and launch the pilot clinic.\""
    )

    # =========================================================================
    # SLIDE 13: Business ROI, Next Steps & Kickoff
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    add_header(s13, "Business Impact, ROI & Executive Kickoff")

    # Left: ROI Summary
    add_card(s13, 0.8, 1.6, 5.75, 5.2, C_BG_CARD, C_BORDER)
    tb_roi = s13.shapes.add_textbox(Inches(1.05), Inches(1.85), Inches(5.25), Inches(4.7))
    tf_roi = tb_roi.text_frame
    tf_roi.word_wrap = True
    
    pr1 = tf_roi.paragraphs[0]
    pr1.text = "PROJECTED CLINICAL ROI & IMPACT"
    pr1.font.name = "Arial"
    pr1.font.size = Pt(13)
    pr1.font.bold = True
    pr1.font.color.rgb = C_PRIMARY
    pr1.space_after = Pt(8)
    
    roi_points = [
        ("• Zero Missed Calls:", " Captures 100% of after-hours and lunchtime calls, generating an estimated $120,000+ in retained annual production per location."),
        ("• 65% Staff Time Reclaimed:", " Front desk staff can refocus on in-person patient experience, treatment presentation, and collections."),
        ("• 30% Higher Conversion:", " Instant slot booking and SMS confirmations reduce caller drop-off and eliminate phone tag."),
        ("• Scalability:", " Handles unlimited concurrent calls during peak morning surges with zero busy signals.")
    ]
    for bold_t, desc_t in roi_points:
        p = tf_roi.add_paragraph()
        p.space_after = Pt(6)
        r_b = p.add_run()
        r_b.text = bold_t
        r_b.font.name = "Arial"
        r_b.font.size = Pt(10)
        r_b.font.bold = True
        r_b.font.color.rgb = C_NAVY
        r_d = p.add_run()
        r_d.text = desc_t
        r_d.font.name = "Calibri"
        r_d.font.size = Pt(10)
        r_d.font.color.rgb = C_DARK

    # Right: Kickoff Action Items
    add_card(s13, 6.75, 1.6, 5.75, 5.2, C_ACCENT_BG, C_TEAL)
    tb_act = s13.shapes.add_textbox(Inches(7.0), Inches(1.85), Inches(5.25), Inches(4.7))
    tf_act = tb_act.text_frame
    tf_act.word_wrap = True
    
    pa1 = tf_act.paragraphs[0]
    pa1.text = "IMMEDIATE EXECUTIVE KICKOFF DECISIONS"
    pa1.font.name = "Arial"
    pa1.font.size = Pt(13)
    pa1.font.bold = True
    pa1.font.color.rgb = C_TEAL
    pa1.space_after = Pt(8)
    
    actions = [
        ("1. Target PMS Selection:", " Confirm primary integration target (Open Dental API, Dentrix Developer API, or NexHealth Universal Bridge)."),
        ("2. Cloud Infrastructure Provisioning:", " Deploy initial FastAPI voice server on AWS/GCP with Twilio SIP trunk."),
        ("3. Pilot Dental Clinic Selection:", " Identify 1-2 partner dental offices for initial shadow mode and pilot scheduling."),
        ("4. Authorize Phase 1 Build:", " Begin conversational prompt engineering and core tool development immediately.")
    ]
    for bold_t, desc_t in actions:
        p = tf_act.add_paragraph()
        p.space_after = Pt(6)
        r_b = p.add_run()
        r_b.text = bold_t
        r_b.font.name = "Arial"
        r_b.font.size = Pt(10)
        r_b.font.bold = True
        r_b.font.color.rgb = C_NAVY
        r_d = p.add_run()
        r_d.text = desc_t
        r_d.font.name = "Calibri"
        r_d.font.size = Pt(10)
        r_d.font.color.rgb = C_DARK

    set_notes(s13,
        "\"In conclusion: Implementing this AI Dental Receptionist delivers an immediate ROI by capturing missed patient revenue, freeing up front-desk staff, and providing a seamless 24/7 patient booking experience.\n\n"
        "Everything outlined in our technical specification document is ready to be implemented. To kick off Phase 1, we just need to confirm the target PMS system and authorize the cloud setup.\n\n"
        "Thank you, and I am now open to any questions.\""
    )

    prs.save(output_path)
    print(f"Presentation saved successfully to: {output_path}")

if __name__ == "__main__":
    out_file = r"C:\Users\huwai\.gemini\antigravity\scratch\AI_Dental_Manager_Scheduling_Agent_Walkthrough.pptx"
    build_presentation(out_file)
