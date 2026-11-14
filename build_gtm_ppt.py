import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def build_limra_presentation(output_path):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Color Palette - Modern Executive Healthcare Theme
    C_NAVY = RGBColor(15, 23, 42)       # #0F172A (Deep Slate Navy)
    C_PRIMARY = RGBColor(30, 58, 138)   # #1E3A8A (Corporate Royal Blue)
    C_TEAL = RGBColor(13, 148, 136)     # #0D9488 (Teal Accent)
    C_DARK = RGBColor(30, 41, 59)       # #1E293B (Body Text)
    C_MUTED = RGBColor(100, 116, 139)   # #64748B (Muted text)
    C_BG_CARD = RGBColor(248, 250, 252) # #F8FAFC (Card Background)
    C_BORDER = RGBColor(226, 232, 240)  # #E2E8F0 (Border)
    C_WHITE = RGBColor(255, 255, 255)
    C_ACCENT_BG = RGBColor(240, 253, 250) # Light Teal BG
    C_RED = RGBColor(225, 29, 72)       # Rose 600

    def add_header(slide, title_text, category_text="LIMRA DENTAL AI — STRATEGIC IMPLEMENTATION PLAN"):
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

        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.72), Inches(11.7), Inches(0.65))
        tf = title_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.name = "Arial"
        p.font.size = Pt(21)
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
    # SLIDE 1: Title Slide (Executive Dark Theme)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = C_NAVY
    bg1.line.fill.background()

    bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.2), Inches(1.6), Inches(0.8), Inches(0.08))
    bar.fill.solid()
    bar.fill.fore_color.rgb = C_TEAL
    bar.line.fill.background()

    t_box = s1.shapes.add_textbox(Inches(1.2), Inches(1.9), Inches(10.8), Inches(3.5))
    tf1 = t_box.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.text = "LIMRA DENTAL AI — COMMERCIAL PLATFORM BLUEPRINT"
    p0.font.name = "Arial"
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = C_TEAL
    p0.space_after = Pt(12)

    p1 = tf1.add_paragraph()
    p1.text = "Building a Scalable, Commercial AI Platform:\nFrom Shifa Dental Pilot to Market Expansion"
    p1.font.name = "Arial"
    p1.font.size = Pt(30)
    p1.font.bold = True
    p1.font.color.rgb = C_WHITE
    p1.space_after = Pt(16)

    p2 = tf1.add_paragraph()
    p2.text = "Technical Approach • Multi-Agent Suite • Tools • 12-Week Roadmap • Unit Economics • Go-to-Market Strategy"
    p2.font.name = "Calibri"
    p2.font.size = Pt(14)
    p2.font.color.rgb = RGBColor(203, 213, 225)

    foot_box = s1.shapes.add_textbox(Inches(1.2), Inches(6.0), Inches(10.8), Inches(0.8))
    tf_f = foot_box.text_frame
    p_f = tf_f.paragraphs[0]
    p_f.text = "PILOT LOCATIONS: Shifa Dental (Plano & Garland, TX)  |  TARGET: Multi-Location DSOs  |  MODEL: Proprietary B2B SaaS"
    p_f.font.name = "Arial"
    p_f.font.size = Pt(10)
    p_f.font.bold = True
    p_f.font.color.rgb = RGBColor(148, 163, 184)

    set_notes(s1,
        "Good morning/afternoon. Today, I am presenting our strategic roadmap to build and commercialize Limra Dental AI.\n\n"
        "Our goal is not just to replace Dentina AI at Shifa Dental, but to use Shifa Dental's Plano and Garland locations as our pilot launchpad to build a highly scalable, proprietary B2B SaaS product that we can expand to hundreds of dental practices across Texas and the US.\n\n"
        "This presentation covers our technical approach, the three-agent umbrella architecture, the exact tools, a 12-week development roadmap, full unit economics with 60%+ profit margins, and our Go-to-Market expansion strategy."
    )

    # =========================================================================
    # SLIDE 2: Executive Summary & Strategic Positioning
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Executive Summary: Strategic Opportunity & The 'Customize' Approach")

    cards_s2 = [
        ("The Current Pain", "Dentina AI Limitations", "Shifa Dental is paying $300-$400/mo for Dentina AI, which suffers from robotic latency (>800ms), stiff English/Spanish translation, rigid scheduling, and zero white-label resale rights.", C_RED),
        ("The Platform Solution", "Limra Dental AI Umbrella", "We license HIPAA-compliant low-latency voice infrastructure (Retell AI) and build our proprietary dental intelligence layer, Open Dental direct adapter, and unified dashboard.", C_PRIMARY),
        ("The Market Opportunity", "B2B SaaS with >60% Margin", "By starting with Shifa Dental (Plano & Garland), we validate clinical workflows and package a repeatable 3-Agent Dental Operations Suite priced at $599-$899/month per clinic.", C_TEAL)
    ]

    for i, (tag, title, desc, col) in enumerate(cards_s2):
        left = 0.8 + i * 3.95
        add_card(s2, left, 1.6, 3.8, 3.3, C_BG_CARD, C_BORDER)
        tb = s2.shapes.add_textbox(Inches(left + 0.25), Inches(1.8), Inches(3.3), Inches(2.9))
        tf = tb.text_frame
        tf.word_wrap = True

        p_t = tf.paragraphs[0]
        p_t.text = tag.upper()
        p_t.font.name = "Arial"
        p_t.font.size = Pt(10)
        p_t.font.bold = True
        p_t.font.color.rgb = col
        p_t.space_after = Pt(4)

        p_h = tf.add_paragraph()
        p_h.text = title
        p_h.font.name = "Arial"
        p_h.font.size = Pt(13)
        p_h.font.bold = True
        p_h.font.color.rgb = C_NAVY
        p_h.space_after = Pt(8)

        p_d = tf.add_paragraph()
        p_d.text = desc
        p_d.font.name = "Calibri"
        p_d.font.size = Pt(10.5)
        p_d.font.color.rgb = C_DARK

    add_card(s2, 0.8, 5.15, 11.7, 1.8, C_ACCENT_BG, C_TEAL)
    tb_b = s2.shapes.add_textbox(Inches(1.1), Inches(5.3), Inches(11.1), Inches(1.5))
    tf_b = tb_b.text_frame
    tf_b.word_wrap = True

    pb1 = tf_b.paragraphs[0]
    pb1.text = "🎯 OUR STRATEGIC THESIS: CUSTOMIZE, DON'T RESELL OR REINVENT"
    pb1.font.name = "Arial"
    pb1.font.size = Pt(11)
    pb1.font.bold = True
    pb1.font.color.rgb = C_TEAL
    pb1.space_after = Pt(4)

    pb2 = tf_b.add_paragraph()
    pb2.text = "Reselling closed agents (Arini, Viva, Dentina) makes us a low-margin referral partner. Building voice engines from scratch takes 6+ months and adds no defensible value. By licensing voice infrastructure and building our own dental operational IP, we get to market in 12 weeks with full equity value."
    pb2.font.name = "Calibri"
    pb2.font.size = Pt(10.5)
    pb2.font.color.rgb = C_NAVY

    set_notes(s2,
        "Here is the executive summary: Shifa Dental's current experience with Dentina AI showed us the opportunity and the limitation.\n\n"
        "Dentina is a closed box—we cannot customize it, white-label it, or build real commercial equity on top of it. Our strategy is simple: 'Customize'.\n\n"
        "We license proven voice plumbing (Retell AI), while we build and own the core dental intelligence: direct Open Dental scheduling, automated insurance eligibility, and treatment recovery. This positions Limra AI as a defensible software company."
    )

    # =========================================================================
    # SLIDE 3: The 3-Agent Umbrella Architecture
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Product Architecture: The Tri-Agent Umbrella Platform")

    agents = [
        ("Agent 1: Bilingual Voice Concierge", 
         "• Real-Time Inbound Receptionist\n• Sub-450ms Latency (<0.5s response time)\n• Native English & Mexican-Spanish Auto-Detect\n• Operatory Chair Triage (Hygiene vs. Doctor)\n• Real-Time Open Dental Calendar Booking\n• Automatic SMS Invite & Digital Intake Link", C_PRIMARY),
        ("Agent 2: Real-Time Insurance Verification", 
         "• Automated Payer Eligibility Engine\n• Connects to Clearinghouses / pVerify / Availity\n• Queries Delta Dental, MetLife, Cigna, etc.\n• Extracts Deductibles, Maximums, Co-pays\n• Verifies eligibility 48h prior to visit\n• Writes verified breakdown into Open Dental", C_TEAL),
        ("Agent 3: Treatment Pending & Recall Agent", 
         "• Revenue Recovery & Case Acceptance\n• Scans Open Dental uncompleted treatment ledger\n• Proactive empathetic SMS & Voice outreach\n• End-of-Year expiring benefits campaign\n• Books pending crowns, fillings & deep cleanings\n• Recovers $30K-$50K/mo in unscheduled care", C_PRIMARY),
    ]

    for i, (title, details, col) in enumerate(agents):
        left = 0.8 + i * 3.95
        add_card(s3, left, 1.6, 3.8, 5.2, C_BG_CARD, C_BORDER)
        tb = s3.shapes.add_textbox(Inches(left + 0.2), Inches(1.8), Inches(3.4), Inches(4.8))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = f"0{i+1}"
        p.font.name = "Arial"
        p.font.size = Pt(20)
        p.font.bold = True
        p.font.color.rgb = col
        p.space_after = Pt(2)

        p_t = tf.add_paragraph()
        p_t.text = title
        p_t.font.name = "Arial"
        p_t.font.size = Pt(12)
        p_t.font.bold = True
        p_t.font.color.rgb = C_NAVY
        p_t.space_after = Pt(8)

        p_d = tf.add_paragraph()
        p_d.text = details
        p_d.font.name = "Calibri"
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = C_DARK

    set_notes(s3,
        "Here is the core product umbrella we are offering under Limra Dental AI:\n\n"
        "Agent 1 is the Front-Desk Concierge: It handles all inbound calls in English and Spanish with unmatched human warmth, sub-450ms latency, and books into Open Dental.\n\n"
        "Agent 2 is Insurance Verification: It solves the #1 time-sink of front-desk staff. It automatically verifies patient eligibility before the appointment and writes the breakdown into the patient's file.\n\n"
        "Agent 3 is Treatment Recovery: It solves the dental clinic's biggest revenue leak—patients who get diagnosed with crowns or fillings but leave without scheduling. It reaches out empathetically to book them."
    )

    # =========================================================================
    # SLIDE 4: Technical Approach & Integration Architecture
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Technical Approach: Voice Pipeline & Open Dental Adapter")

    tech_blocks = [
        ("Telephony & Audio Layer", "Twilio SIP Trunking + WebSockets", "Handles inbound caller phone lines for Plano and Garland clinic DIDs. Streams raw 16-bit PCM audio bidirectionally with zero jitter."),
        ("Voice Gateway & Models", "Retell AI + Cartesia Sonic", "Provides sub-450ms conversational turn-taking, background noise suppression, and hyper-realistic Mexican-Spanish/US-English voices."),
        ("Dental Logic & API Engine", "FastAPI (Python) + PostgreSQL", "Our proprietary Limra backend. Executes clinical triage rules, session state management, idempotency, and calendar lock mechanisms."),
        ("Open Dental Direct Adapter", "Open Dental REST API ($35/mo Tier)", "Direct read/write synchronization with Shifa's Open Dental server. Operatory-aware slot calculation and patient record verification."),
        ("Payer Eligibility Connector", "pVerify / Keragon / Availity API", "Automated EDI 270/271 real-time eligibility inquiry engine to parse complex dental benefit summaries into clean JSON."),
        ("Unified Limra Dashboard", "Next.js / React Web Portal", "Multi-tenant clinic portal showing call recordings, language breakdown, booked appointments, verified insurance, and ROI metrics.")
    ]

    for i, (title, tech, desc) in enumerate(tech_blocks):
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
        p.font.size = Pt(11)
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
        p_d.font.size = Pt(9.5)
        p_d.font.color.rgb = C_DARK

    set_notes(s4,
        "Here is the technical stack that powers the platform:\n\n"
        "We are decoupling the voice layer from the business logic. Retell AI handles the telephony and speech generation with Cartesia Sonic, which gives us industry-leading latency.\n\n"
        "All business logic, scheduling rules, and Open Dental API queries live inside our own proprietary FastAPI backend. This means Retell never owns our data or scheduling rules—if we ever decide to switch to open-source LiveKit later, we can swap the voice vendor without rewriting our dental core."
    )

    # =========================================================================
    # SLIDE 5: Solving the "Human Touch" Problem (Why We Beat Dentina)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "The 'Human Touch' Benchmark: Dentina AI vs. Limra Dental AI")

    features = [
        ("Conversational Latency", "800ms - 1,200ms (Awkward pauses, cross-talk)", "<450ms (Instant, natural conversational rhythm)"),
        ("Voice Synthesis Quality", "Mechanical, robotic cadence; sounds synthesized", "Warm, emotional tone, breathing pauses, conversational fillers"),
        ("Spanish Language Handling", "Stiff literal translation; robotic pronunciation", "Native Mexican/Texas Spanish adaptation & idioms"),
        ("Mid-Sentence Interruptions", "Frequently resets or cuts off caller clumsily", "Smooth turn-taking via real-time Voice Activity Detection"),
        ("Multi-Chair Clinic Routing", "Rigid generic booking; struggles with chair rules", "Operatory-aware (Hygiene chair vs. Doctor operatory)"),
        ("Brand Ownership / White-Label", "100% Dentina branded; zero partner customization", "100% White-Labeled under Limra Dental AI platform"),
    ]

    add_card(s5, 0.8, 1.6, 11.7, 5.2, C_BG_CARD, C_BORDER)
    tb = s5.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.3), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True

    p_hdr = tf.paragraphs[0]
    p_hdr.text = f"{'EVALUATION CRITERIA':<28} | {'DENTINA AI (CURRENT BENCHMARK)':<36} | {'LIMRA DENTAL AI (PROPOSED PLATFORM)'}"
    p_hdr.font.name = "Arial"
    p_hdr.font.size = Pt(11)
    p_hdr.font.bold = True
    p_hdr.font.color.rgb = C_PRIMARY
    p_hdr.space_after = Pt(10)

    for crit, dentina, limra in features:
        p_row = tf.add_paragraph()
        p_row.space_after = Pt(8)
        
        r1 = p_row.add_run()
        r1.text = f"• {crit}: "
        r1.font.name = "Arial"
        r1.font.size = Pt(10)
        r1.font.bold = True
        r1.font.color.rgb = C_NAVY

        r2 = p_row.add_run()
        r2.text = f"[Dentina: {dentina}]  ➔  "
        r2.font.name = "Calibri"
        r2.font.size = Pt(10)
        r2.font.color.rgb = C_RED

        r3 = p_row.add_run()
        r3.text = f"[Limra: {limra}]"
        r3.font.name = "Calibri"
        r3.font.size = Pt(10)
        r3.font.bold = True
        r3.font.color.rgb = C_TEAL

    set_notes(s5,
        "This slide directly addresses the core issue: 'Dentina is fine, but not good, and lacks human touch.'\n\n"
        "Why does Dentina sound robotic? Because its latency is over 800ms. In phone conversations, an 800ms silence feels like an eternity and forces callers to ask 'Hello, are you there?'.\n\n"
        "With Limra AI running on Retell + Cartesia, latency drops below 450ms. The agent uses realistic conversational fillers like 'Got it, let me check Dr. Smith's chair for you'. In Plano and Garland, our Spanish voice sounds like a native speaker from the area, not a machine translation."
    )

    # =========================================================================
    # SLIDE 6: 12-Week Development Roadmap & Milestones
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Development Roadmap: 12 Weeks from Build to Pilot Launch")

    phases_s6 = [
        ("Phase 1: Foundation (Weeks 1-3)", "API Keys & Voice Pipeline", "• Secure Open Dental Developer API key ($35 tier)\n• Execute Retell BAA & Twilio SIP trunk setup\n• Build bilingual prompt library for Shifa Dental\n• Establish local dev & test harness", C_PRIMARY),
        ("Phase 2: Open Dental Adapter (Weeks 4-6)", "PMS Scheduling Engine", "• Connect direct Open Dental API (Plano & Garland)\n• Implement operatory chair slot calculation\n• Build lock mechanism to prevent double-booking\n• Automated SMS confirmation & intake links", C_PRIMARY),
        ("Phase 3: Tri-Agent Expansion (Weeks 7-9)", "Insurance & Treatment Recovery", "• Integrate pVerify/eligibility API for Agent 2\n• Build treatment plan scanner for Agent 3\n• Develop initial Limra Admin Dashboard\n• Internal call simulation & edge-case testing", C_TEAL),
        ("Phase 4: Shifa Pilot & Launch (Weeks 10-12)", "Production Deployment", "• Deploy live on Shifa Garland & Plano phone lines\n• Parallel shadow run with front-desk staff\n• Daily call auditing & prompt calibration\n• Document pilot case study & ROI metrics", C_NAVY)
    ]

    for i, (title, sub, details, col) in enumerate(phases_s6):
        left = 0.8 + i * 2.92
        add_card(s6, left, 1.6, 2.8, 5.2, C_BG_CARD, C_BORDER)
        tb = s6.shapes.add_textbox(Inches(left + 0.15), Inches(1.8), Inches(2.5), Inches(4.8))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = f"MILESTONE 0{i+1}"
        p.font.name = "Arial"
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = col
        p.space_after = Pt(2)

        p_t = tf.add_paragraph()
        p_t.text = title
        p_t.font.name = "Arial"
        p_t.font.size = Pt(11)
        p_t.font.bold = True
        p_t.font.color.rgb = C_NAVY
        p_t.space_after = Pt(2)

        p_s = tf.add_paragraph()
        p_s.text = sub
        p_s.font.name = "Arial"
        p_s.font.size = Pt(9.5)
        p_s.font.bold = True
        p_s.font.color.rgb = C_TEAL
        p_s.space_after = Pt(8)

        p_d = tf.add_paragraph()
        p_d.text = details
        p_d.font.name = "Calibri"
        p_d.font.size = Pt(9.5)
        p_d.font.color.rgb = C_DARK

    set_notes(s6,
        "Here is our 12-week development execution plan.\n\n"
        "Weeks 1 to 3 establish our voice pipeline, Twilio numbers, and Open Dental developer credentials.\n\n"
        "Weeks 4 to 6 are the most important technical phase: building our proprietary Open Dental scheduling engine that queries chairs and writes bookings without conflict.\n\n"
        "Weeks 7 to 9 add the insurance verification connector and pending treatment recovery engine, along with the management dashboard.\n\n"
        "Weeks 10 to 12 are our production pilot at Shifa Dental in Plano and Garland, running alongside staff to prove our ROI before full market launch."
    )

    # =========================================================================
    # SLIDE 7: Resource Allocation & Team Requirements
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Resource Allocation: Lean Team & Cloud Infrastructure")

    team = [
        ("Lead AI Voice & Backend Engineer", "Full-Time (Core Developer)", "Owns FastAPI backend, Retell AI voice orchestration, tool calling schemas, and Open Dental REST API integration."),
        ("Frontend & Dashboard Developer", "Part-Time / Contract (Weeks 6-12)", "Builds the clean Next.js/React multi-tenant dashboard for clinic owners to view call logs, recordings, and analytics."),
        ("Dental Clinical SME / Prompt Designer", "Advisory (Shifa Office Manager)", "Provides exact clinic rules, insurance codes, operatory chair mapping, and evaluates English/Spanish conversational quality."),
        ("HIPAA & Security Compliance Lead", "Advisory / Project Lead", "Executes BAAs across vendors (Retell, Twilio, AWS), enforces AES-256 encryption, and oversees PHI audit trails.")
    ]

    for i, (role, type_str, desc) in enumerate(team):
        col_idx = i % 2
        row_idx = i // 2
        left = 0.8 + col_idx * 5.95
        top = 1.6 + row_idx * 2.65
        add_card(s7, left, top, 5.75, 2.45, C_BG_CARD, C_BORDER)

        tb = s7.shapes.add_textbox(Inches(left + 0.25), Inches(top + 0.2), Inches(5.25), Inches(2.05))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = role
        p.font.name = "Arial"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = C_PRIMARY
        p.space_after = Pt(2)

        p_s = tf.add_paragraph()
        p_s.text = type_str
        p_s.font.name = "Arial"
        p_s.font.size = Pt(9.5)
        p_s.font.bold = True
        p_s.font.color.rgb = C_TEAL
        p_s.space_after = Pt(6)

        p_d = tf.add_paragraph()
        p_d.text = desc
        p_d.font.name = "Calibri"
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = C_DARK

    set_notes(s7,
        "We can execute this with a very lean engineering team.\n\n"
        "We need one strong Lead Backend & Voice AI engineer to build the pipeline and Open Dental adapter. A frontend developer comes in mid-way to build the clinic dashboard.\n\n"
        "Critically, we have an unfair advantage: we have direct access to Shifa Dental's clinical staff to act as our domain experts, ensuring our prompt scripts and chair allocation logic match real-world Texas practice standards."
    )

    # =========================================================================
    # SLIDE 8: Unit Economics & Operational Cost Breakdown
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Unit Economics: Estimated Costs per Dental Location")

    cost_items = [
        ("Voice Engine & Telephony (Retell AI)", "600 calls/mo @ 3 mins = 1,800 mins @ ~$0.10 - $0.14/min", "$180 - $250 / mo"),
        ("Open Dental Direct API Fee", "Standard Open Dental developer tier per practice location", "$35 / mo"),
        ("Phone Numbers & Carrier DIDs (Twilio)", "2 dedicated clinic phone numbers + SMS confirmations", "$15 - $25 / mo"),
        ("Payer Eligibility API (pVerify / Keragon)", "~150 new patient verifications @ $0.30 - $0.50/check", "$45 - $75 / mo"),
        ("Cloud Hosting & Database (AWS / Render)", "PostgreSQL, Redis cache, secure FastAPI container", "$30 - $50 / mo"),
        ("TOTAL VARIABLE COST PER LOCATION", "All-in cost to operate Limra AI per dental office", "$305 - $435 / mo"),
    ]

    add_card(s8, 0.8, 1.6, 11.7, 5.2, C_BG_CARD, C_BORDER)
    tb = s8.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.3), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True

    p_h = tf.paragraphs[0]
    p_h.text = f"{'INFRASTRUCTURE COMPONENT':<35} | {'USAGE / VOLUME ASSUMPTION':<48} | {'ESTIMATED MONTHLY COST'}"
    p_h.font.name = "Arial"
    p_h.font.size = Pt(10.5)
    p_h.font.bold = True
    p_h.font.color.rgb = C_PRIMARY
    p_h.space_after = Pt(10)

    for comp, usage, cost in cost_items:
        p = tf.add_paragraph()
        p.space_after = Pt(8)
        is_total = "TOTAL" in comp

        r1 = p.add_run()
        r1.text = f"• {comp:<32} "
        r1.font.name = "Arial"
        r1.font.size = Pt(10 if not is_total else 11)
        r1.font.bold = True
        r1.font.color.rgb = C_NAVY if not is_total else C_TEAL

        r2 = p.add_run()
        r2.text = f"({usage:<45}) ➔ "
        r2.font.name = "Calibri"
        r2.font.size = Pt(10)
        r2.font.color.rgb = C_MUTED

        r3 = p.add_run()
        r3.text = f"{cost}"
        r3.font.name = "Arial"
        r3.font.size = Pt(10 if not is_total else 11.5)
        r3.font.bold = True
        r3.font.color.rgb = C_DARK if not is_total else C_PRIMARY

    set_notes(s8,
        "Here are our real-world unit economics based on Shifa Dental's call volume data.\n\n"
        "Assuming a busy practice handles 600 calls per month at 3 minutes per call (1,800 minutes total), the voice pipeline costs roughly $180 to $250. Open Dental charges $35. With telephony, hosting, and insurance verification, our total cost to operate one clinic location is roughly $305 to $435 per month.\n\n"
        "Notice how low this is compared to the $3,500/month salary of an in-person receptionist. This creates massive margin potential."
    )

    # =========================================================================
    # SLIDE 9: Commercial Pricing Model & Profit Margins
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Commercial Pricing Strategy: Maximizing Gross Margins")

    tiers = [
        ("Starter Receptionist", "$599 / month", "Per Location", 
         "• Agent 1: 24/7 Bilingual Inbound Voice\n• Direct Open Dental Calendar Sync\n• Operatory Chair Triage\n• Automated SMS Reminders\n• Basic Analytics Dashboard\n\nCOGS: ~$270/mo  |  Gross Margin: 55%", C_PRIMARY),
        ("Growth Suite (Recommended)", "$899 / month", "Per Location (Most Popular)", 
         "• Everything in Starter PLUS:\n• Agent 2: Automated Insurance Verification\n• Up to 200 eligibility checks/mo\n• Dedicated bilingual Mexican-Spanish voice\n• Live warm-transfer to staff\n\nCOGS: ~$360/mo  |  Gross Margin: 60%", C_TEAL),
        ("Full Practice DSO Suite", "$1,299 / month", "Per Location (Multi-Provider)", 
         "• Everything in Growth PLUS:\n• Agent 3: Treatment Pending Recovery\n• Unscheduled Treatment Recall Engine\n• End-of-Year Benefits Outreach\n• Priority Multi-Doctor Chair Allocation\n\nCOGS: ~$430/mo  |  Gross Margin: 67%", C_PRIMARY),
    ]

    for i, (name, price, sub, desc, col) in enumerate(tiers):
        left = 0.8 + i * 3.95
        add_card(s9, left, 1.6, 3.8, 5.2, C_BG_CARD, C_BORDER)
        tb = s9.shapes.add_textbox(Inches(left + 0.2), Inches(1.8), Inches(3.4), Inches(4.8))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = name.upper()
        p.font.name = "Arial"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = col
        p.space_after = Pt(2)

        p_pr = tf.add_paragraph()
        p_pr.text = price
        p_pr.font.name = "Arial"
        p_pr.font.size = Pt(22)
        p_pr.font.bold = True
        p_pr.font.color.rgb = C_NAVY
        p_pr.space_after = Pt(1)

        p_sb = tf.add_paragraph()
        p_sb.text = sub
        p_sb.font.name = "Arial"
        p_sb.font.size = Pt(9.5)
        p_sb.font.bold = True
        p_sb.font.color.rgb = C_TEAL
        p_sb.space_after = Pt(8)

        p_d = tf.add_paragraph()
        p_d.text = desc
        p_d.font.name = "Calibri"
        p_d.font.size = Pt(9.5)
        p_d.font.color.rgb = C_DARK

    set_notes(s9,
        "Here is our recommended pricing model when we take Limra Dental AI to market.\n\n"
        "We offer three tiers:\n"
        "Starter at $599/month covers just the bilingual voice receptionist, leaving a 55% gross margin.\n"
        "Growth at $899/month bundles the receptionist and insurance verification, which is our flagship tier at 60% gross margin.\n"
        "Full Practice at $1,299/month includes Agent 3 for treatment recovery, yielding a 67% margin.\n\n"
        "Dentists are used to paying $3,000+ for front-desk staff. At $899, Limra AI saves them $25,000 annually while providing 24/7 bilingual coverage."
    )

    # =========================================================================
    # SLIDE 10: Go-to-Market (GTM) Strategy & Scale
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Go-to-Market Strategy: From Shifa Pilot to 50+ Clinics")

    gtm_stages = [
        ("Phase 1: Prove (Weeks 10-14)", "Shifa Dental Pilot (Plano & Garland)", "• Run live in both Shifa locations.\n• Capture hard proof: 0 missed calls, % of Spanish calls converted, insurance hours saved.\n• Produce verified case study & ROI video testimonial.", C_PRIMARY),
        ("Phase 2: Local Cluster (Months 4-6)", "Dallas-Fort Worth Community Expansion", "• Target 15-20 independent dental clinics in Plano, Garland, Frisco, and Richardson.\n• Leverage local community networks (Masjid business directories, local dental societies).\n• Offer 14-day free pilot on overflow calls.", C_TEAL),
        ("Phase 3: DSO & Regional Scale (Months 7-12)", "Texas DSOs & Dental Marketing Agencies", "• Expand to Dental Support Organizations (DSOs) with 5-20 locations running Open Dental.\n• Partner with dental marketing agencies running Google/Meta Ads to guarantee call conversion.\n• Reach 50 active locations ($45K-$60K Monthly Recurring Revenue).", C_NAVY)
    ]

    for i, (stage, focus, details, col) in enumerate(gtm_stages):
        left = 0.8 + i * 3.95
        add_card(s10, left, 1.6, 3.8, 5.2, C_BG_CARD, C_BORDER)
        tb = s10.shapes.add_textbox(Inches(left + 0.2), Inches(1.8), Inches(3.4), Inches(4.8))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = f"STAGE 0{i+1}"
        p.font.name = "Arial"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = col
        p.space_after = Pt(2)

        p_t = tf.add_paragraph()
        p_t.text = stage
        p_t.font.name = "Arial"
        p_t.font.size = Pt(12)
        p_t.font.bold = True
        p_t.font.color.rgb = C_NAVY
        p_t.space_after = Pt(2)

        p_f = tf.add_paragraph()
        p_f.text = focus
        p_f.font.name = "Arial"
        p_f.font.size = Pt(9.5)
        p_f.font.bold = True
        p_f.font.color.rgb = C_TEAL
        p_f.space_after = Pt(8)

        p_d = tf.add_paragraph()
        p_d.text = details
        p_d.font.name = "Calibri"
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = C_DARK

    set_notes(s10,
        "Here is our Go-to-Market expansion roadmap:\n\n"
        "Stage 1 is our proving ground: We deploy at Shifa Dental in Plano and Garland. We gather hard metrics—how many after-hours calls were saved, how many Spanish callers were booked, and how much treatment was recovered.\n\n"
        "Stage 2 targets our immediate backyard: North Texas (Plano, Garland, Richardson, Frisco). Dental practices talk to each other, and local community networks provide high-trust referrals.\n\n"
        "Stage 3 scales to DSOs and regional dental groups across Texas, targeting 50 locations to achieve $50,000+ in high-margin Monthly Recurring Revenue."
    )

    # =========================================================================
    # SLIDE 11: Risks, Mitigations & Immediate Next Steps
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "Risk Management & Next Steps for Tomorrow's Discussion")

    add_card(s11, 0.8, 1.6, 5.75, 5.2, C_BG_CARD, C_BORDER)
    tb_l = s11.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.35), Inches(4.8))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True

    pl1 = tf_l.paragraphs[0]
    pl1.text = "KEY OPERATIONAL RISKS & MITIGATIONS"
    pl1.font.name = "Arial"
    pl1.font.size = Pt(12)
    pl1.font.bold = True
    pl1.font.color.rgb = C_PRIMARY
    pl1.space_after = Pt(8)

    risks = [
        ("• Open Dental API Rate Limits:", " Cache provider working blocks in Redis; query narrow time windows during call."),
        ("• Spanish Voice Accents:", " Conduct rigorous bilingual User Acceptance Testing (UAT) with Shifa's native Spanish staff."),
        ("• Double-Booking Edge Cases:", " Implement atomic 5-minute slot reservations (soft locks) before final write-back."),
        ("• Emergency Triage Liability:", " Hard-coded red-flag keywords trigger instant SIP warm-transfers to on-call doctors.")
    ]
    for b_t, d_t in risks:
        p = tf_l.add_paragraph()
        p.space_after = Pt(6)
        rb = p.add_run()
        rb.text = b_t
        rb.font.name = "Arial"
        rb.font.size = Pt(9.5)
        rb.font.bold = True
        rb.font.color.rgb = C_NAVY
        rd = p.add_run()
        rd.text = d_t
        rd.font.name = "Calibri"
        rd.font.size = Pt(9.5)
        rd.font.color.rgb = C_DARK

    add_card(s11, 6.75, 1.6, 5.75, 5.2, C_ACCENT_BG, C_TEAL)
    tb_r = s11.shapes.add_textbox(Inches(6.95), Inches(1.8), Inches(5.35), Inches(4.8))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True

    pr1 = tf_r.paragraphs[0]
    pr1.text = "IMMEDIATE ACTION ITEMS FOR TOMORROW"
    pr1.font.name = "Arial"
    pr1.font.size = Pt(12)
    pr1.font.bold = True
    pr1.font.color.rgb = C_TEAL
    pr1.space_after = Pt(8)

    actions_s11 = [
        ("1. Approve Technical Architecture:", " Confirm Retell AI + Open Dental direct API approach as the official build foundation."),
        ("2. Request Open Dental Developer Key:", " Submit application for the $35/mo API tier with Vendor Relations."),
        ("3. Sign Retell AI BAA:", " Execute self-signed Business Associate Agreement for HIPAA compliance."),
        ("4. Authorize Phase 1 Sprint:", " Kick off 3-week sprint to build the bilingual prompt harness and local Open Dental test adapter.")
    ]
    for b_t, d_t in actions_s11:
        p = tf_r.add_paragraph()
        p.space_after = Pt(6)
        rb = p.add_run()
        rb.text = b_t
        rb.font.name = "Arial"
        rb.font.size = Pt(9.5)
        rb.font.bold = True
        rb.font.color.rgb = C_NAVY
        rd = p.add_run()
        rd.text = d_t
        rd.font.name = "Calibri"
        rd.font.size = Pt(9.5)
        rd.font.color.rgb = C_DARK

    set_notes(s11,
        "To conclude, every risk has a clear technical mitigation already planned:\n"
        "We handle Open Dental throttling through Redis caching. We guarantee Spanish quality through staff calibration, and we prevent double-booking with atomic soft-locks.\n\n"
        "For tomorrow's discussion, the immediate decisions needed are: approving the Retell + Open Dental approach, applying for the developer key, and authorizing Phase 1.\n\n"
        "Thank you, and I look forward to leading the implementation."
    )

    prs.save(output_path)
    print(f"Presentation saved successfully to: {output_path}")

if __name__ == "__main__":
    out_file = r"C:\Users\huwai\Desktop\AI Dental Agent\Limra_Dental_AI_GTM_Strategy.pptx"
    build_limra_presentation(out_file)
