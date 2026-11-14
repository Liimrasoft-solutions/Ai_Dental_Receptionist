import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def create_comparison_document(output_path):
    doc = Document()

    # Margins
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Color Palette - Professional Deep Slate & Teal
    HEX_PRIMARY = "0F172A"      # Slate 900
    HEX_SECONDARY = "0D9488"    # Teal 600
    HEX_BLUE = "1E3A8A"         # Navy Blue
    HEX_DARK = "1E293B"         # Slate 800 (text)
    HEX_MUTED = "64748B"        # Slate 500 (muted)
    HEX_BG_LIGHT = "F8FAFC"     # Slate 50 (table light row)
    HEX_BORDER = "CBD5E1"       # Slate 300 (border)
    HEX_ACCENT_BG = "F0FDFA"    # Teal light bg
    HEX_GREEN_BG = "ECFDF5"     # Green light bg
    HEX_RED_BG = "FEF2F2"       # Red light bg

    COLOR_PRIMARY = RGBColor(15, 23, 42)
    COLOR_SECONDARY = RGBColor(13, 148, 136)
    COLOR_BLUE = RGBColor(30, 58, 138)
    COLOR_DARK = RGBColor(30, 41, 59)
    COLOR_MUTED = RGBColor(100, 116, 139)
    COLOR_GREEN = RGBColor(16, 185, 129)
    COLOR_RED = RGBColor(225, 29, 72)

    # Base typography
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(10.5)
    normal_style.font.color.rgb = COLOR_DARK

    def set_cell_background(cell, fill_hex):
        tcPr = cell._tc.get_or_add_tcPr()
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
        tcPr.append(shd)

    def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
        tcPr.append(tcMar)

    def add_custom_heading_1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Arial'
        run.font.size = Pt(15)
        run.bold = True
        run.font.color.rgb = COLOR_BLUE
        return p

    def add_custom_heading_2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Arial'
        run.font.size = Pt(12.5)
        run.bold = True
        run.font.color.rgb = COLOR_SECONDARY
        return p

    def add_callout(title, text, bg_hex=HEX_ACCENT_BG, border_hex=HEX_SECONDARY):
        table = doc.add_table(rows=1, cols=1)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False
        table.columns[0].width = Inches(6.5)
        cell = table.cell(0, 0)
        set_cell_background(cell, bg_hex)
        set_cell_margins(cell, top=120, bottom=120, left=180, right=180)
        
        tcPr = cell._tc.get_or_add_tcPr()
        borders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:top w:val="none"/><w:left w:val="single" w:sz="24" w:space="0" w:color="{border_hex}"/><w:bottom w:val="none"/><w:right w:val="none"/></w:tcBorders>')
        tcPr.append(borders)
        
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(2)
        r_title = p.add_run(f"📌 {title}: ")
        r_title.bold = True
        r_title.font.name = 'Arial'
        r_title.font.size = Pt(10.5)
        r_title.font.color.rgb = COLOR_SECONDARY if border_hex == HEX_SECONDARY else COLOR_RED
        
        r_text = p.add_run(text)
        r_text.font.size = Pt(10)
        r_text.font.color.rgb = COLOR_DARK
        doc.add_paragraph().paragraph_format.space_after = Pt(4)

    def style_table(table, col_widths, headers, data):
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False
        
        hdr_row = table.rows[0]
        for idx, header_text in enumerate(headers):
            cell = hdr_row.cells[idx]
            cell.width = Inches(col_widths[idx])
            set_cell_background(cell, HEX_PRIMARY)
            set_cell_margins(cell, top=100, bottom=100, left=100, right=100)
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            run = p.add_run(header_text)
            run.bold = True
            run.font.name = 'Arial'
            run.font.color.rgb = RGBColor(255, 255, 255)
            run.font.size = Pt(9)
            
        for r_idx, row_data in enumerate(data):
            row = table.rows[r_idx + 1]
            bg_color = HEX_BG_LIGHT if r_idx % 2 == 1 else "FFFFFF"
            for c_idx, cell_value in enumerate(row_data):
                cell = row.cells[c_idx]
                cell.width = Inches(col_widths[c_idx])
                set_cell_background(cell, bg_color)
                set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
                
                tcPr = cell._tc.get_or_add_tcPr()
                borders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:top w:val="single" w:sz="4" w:space="0" w:color="{HEX_BORDER}"/><w:left w:val="single" w:sz="4" w:space="0" w:color="{HEX_BORDER}"/><w:bottom w:val="single" w:sz="4" w:space="0" w:color="{HEX_BORDER}"/><w:right w:val="single" w:sz="4" w:space="0" w:color="{HEX_BORDER}"/></w:tcBorders>')
                tcPr.append(borders)
                
                p = cell.paragraphs[0]
                p.paragraph_format.space_before = Pt(0)
                p.paragraph_format.space_after = Pt(0)
                run = p.add_run(cell_value)
                run.font.size = Pt(9)
                run.font.color.rgb = COLOR_DARK

    # -------------------------------------------------------------
    # DOCUMENT COVER / TITLE
    # -------------------------------------------------------------
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(20)
    title_p.paragraph_format.space_after = Pt(4)
    r_title = title_p.add_run("Voice AI Infrastructure & Dental Receptionist Comparison")
    r_title.bold = True
    r_title.font.name = 'Arial'
    r_title.font.size = Pt(22)
    r_title.font.color.rgb = COLOR_PRIMARY

    sub_p = doc.add_paragraph()
    sub_p.paragraph_format.space_after = Pt(12)
    r_sub = sub_p.add_run("Deep Technical Evaluation: Retell AI vs. Vapi vs. Bland vs. LiveKit vs. Synthflow vs. Closed Dental Agents (Dentina, Viva, Arini)")
    r_sub.font.name = 'Arial'
    r_sub.font.size = Pt(12)
    r_sub.font.color.rgb = COLOR_SECONDARY

    meta_p = doc.add_paragraph()
    meta_p.paragraph_format.space_after = Pt(16)
    r_meta = meta_p.add_run("Project: Limra Dental AI | Prepared for: Management & Strategic Decision Making | Status: Final Comparative Analysis")
    r_meta.font.size = Pt(9)
    r_meta.font.color.rgb = COLOR_MUTED

    div_p = doc.add_paragraph()
    div_p.paragraph_format.space_after = Pt(14)
    pBdr = parse_xml(f'<w:pBdr {nsdecls("w")}><w:bottom w:val="single" w:sz="18" w:space="1" w:color="{HEX_BLUE}"/></w:pBdr>')
    div_p._p.get_or_add_pPr().append(pBdr)

    # -------------------------------------------------------------
    # SECTION 1: EXECUTIVE DECISION SUMMARY
    # -------------------------------------------------------------
    add_custom_heading_1("1. Executive Decision Summary: Which To Go With and Why")

    p = doc.add_paragraph()
    p.add_run("When building a commercial dental platform like ")
    p.add_run("Limra Dental AI").bold = True
    p.add_run(", we must evaluate two completely different categories of voice AI:\n\n"
              "1. ")
    p.add_run("Category A: Developer Voice Infrastructure (Retell AI, Vapi, Bland, LiveKit): ").bold = True
    p.add_run("These are flexible developer building blocks. They provide real-time telephony, speech-to-text, LLMs, and speech synthesis via APIs. You build your own branding, scheduling logic, and dental integrations on top of them.\n"
              "2. ")
    p.add_run("Category B: Turnkey Dental Products (Dentina AI, Viva AI, Arini AI): ").bold = True
    p.add_run("These are finished consumer products sold directly to dentists. You cannot white-label them or build your own software company on top of them.")

    add_callout("THE CORE VERDICT FOR LIMRA DENTAL AI", 
                "GO WITH RETELL AI for the pilot and initial rollout, with LIVEKIT AGENTS as the long-term cost-reduction exit path. DO NOT RESELL closed agents like Dentina or Viva, because they prevent white-labeling, provide zero equity value, and yield near-zero gross margins.", 
                HEX_ACCENT_BG, HEX_SECONDARY)

    # -------------------------------------------------------------
    # SECTION 2: MASTER COMPARISON MATRIX
    # -------------------------------------------------------------
    add_custom_heading_1("2. Master Comparative Matrix: All Top Competitors")

    headers = [
        "Platform / Agent",
        "Category",
        "Conversational Latency",
        "HIPAA (BAA) Model",
        "White-Label Capability",
        "Level of Customization",
        "Approx. Cost / Minute",
        "Final Verdict"
    ]

    col_widths = [1.0, 0.9, 0.8, 0.9, 0.9, 0.9, 0.7, 0.8]

    table_data = [
        ["Retell AI", "Dev Voice Platform", "<450ms (Fastest)", "Free Self-Signed BAA (Pay-as-you-go)", "100% via Custom API & Backend", "High (Full tool calling & webhook control)", "$0.08 - $0.12 / min", "WINNER (Go with this)"],
        ["Vapi.ai", "Dev Voice Platform", "~500ms - 600ms", "$2,000/mo Enterprise Add-On", "100% via Custom API & Backend", "Extreme (Granular model/pipeline control)", "$0.08 - $0.14 / min", "Strong runner-up (HIPAA expensive)"],
        ["Bland AI", "Dev Voice Platform", "~600ms - 800ms", "Enterprise tier only (Custom quote)", "Partial (Agency portal & webhooks)", "Moderate (Proprietary model pathways)", "$0.12 / min + plans", "Better for outbound sales"],
        ["LiveKit Agents", "Open-Source Framework", "<350ms (Self-tuned)", "You manage on your own AWS/GCP cloud", "100% Full Source Code Ownership", "Complete (Modify every raw audio byte)", "$0.04 - $0.06 (raw infra)", "Long-term exit (Phase 2/3)"],
        ["Synthflow AI", "No-Code Agency Tool", "~800ms - 1,000ms", "Enterprise tier ($450+/mo)", "Native white-label client portal", "Low-Medium (Locked in vendor UI)", "$29 - $450/mo + credits", "Good for no-code agencies"],
        ["Dentina.Ai", "Closed Dental Product", "800ms - 1,200ms (Lag)", "Included in direct clinic subscription", "0% (Strictly Dentina branded)", "Zero (Fixed closed product)", "$299 - $399 / mo flat", "REPLACE (Slow & rigid)"],
        ["Viva AI", "Closed Dental Product", "~500ms - 650ms", "Included in direct clinic subscription", "0% (Strictly Viva branded)", "Zero (Fixed closed product)", "$349 - $899 / mo flat", "Quality benchmark only"],
        ["Arini AI", "Closed Dental Product", "~700ms - 900ms", "Included in direct clinic subscription", "0% (Strictly Arini branded)", "Zero (Fixed closed product)", "$300 - $500 / mo flat", "Direct practice competitor"]
    ]

    tbl = doc.add_table(rows=len(table_data) + 1, cols=len(headers))
    style_table(tbl, col_widths, headers, table_data)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # -------------------------------------------------------------
    # SECTION 3: WHAT CAN BE WHITE-LABELED & WHAT IS CUSTOMIZABLE?
    # -------------------------------------------------------------
    add_custom_heading_1("3. Detailed Analysis: White-Labeling & Customizability")

    p = doc.add_paragraph()
    p.add_run("White-labeling and customizability are the two most critical factors when deciding whether to build a lasting software business or just act as a reseller. Here is how each option stacks up:")

    add_custom_heading_2("3.1 White-Labeling Analysis (Can you put 'Limra Dental AI' on it?)")
    
    wl_points = [
        ("Retell AI & Vapi (100% White-Label via Custom Backend):", 
         "Retell and Vapi provide raw REST APIs and WebSockets. The end-user (Shifa Dental or any clinic) NEVER sees Retell or Vapi. The clinic only sees the 'Limra Dental AI' portal, receives SMS from 'Limra AI', and hears 'Limra Dental Assistant' on the phone. You own the brand completely."),
        ("Synthflow AI (Native White-Label Portal):", 
         "Synthflow offers an out-of-the-box white-label agency plan where you can connect your custom domain (e.g., portal.limradental.com) and your own logo without writing code. However, you are forced to use their exact user interface and feature limitations."),
        ("LiveKit Agents (100% Intellectual Property Ownership):", 
         "LiveKit is open source (Apache 2.0). There is no third-party vendor name to hide—every line of code belongs to your company."),
        ("Dentina AI, Viva AI, Arini AI (0% White-Label / Impossible):", 
         "None of these platforms allow white-labeling or reseller sublicensing. If you use them, the clinic logs into Dentina or Viva's website, pays their brand, and knows you are just a middleman who can be bypassed at any time.")
    ]

    for title, desc in wl_points:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(4)
        r = p.add_run(f"• {title} ")
        r.bold = True
        r.font.name = 'Arial'
        r.font.color.rgb = COLOR_BLUE
        p.add_run(desc)

    add_custom_heading_2("3.2 Customizability Analysis (Can you adapt it to Open Dental & Texas clinics?)")

    cust_points = [
        ("High Customizability (Retell AI & Vapi):", 
         "You can program exact dental triage rules: if a patient mentions severe pain, book 45 minutes with the Lead Doctor in Operatory 1; if they need a routine cleaning, book 60 minutes with the Hygienist in Operatory 3. You can execute custom Python code during the call to check Open Dental in real time."),
        ("Maximum Customizability (LiveKit):", 
         "Gives you direct control over raw audio streams, audio codecs, model temperature, and local telephony SIP servers. Ideal when engineering custom AI agents at scale."),
        ("Zero Customizability (Dentina, Viva, Arini):", 
         "You cannot change their core scheduling algorithms, you cannot hook into external databases easily, and you cannot customize multi-agent workflows like insurance verification.")
    ]

    for title, desc in cust_points:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(4)
        r = p.add_run(f"• {title} ")
        r.bold = True
        r.font.name = 'Arial'
        r.font.color.rgb = COLOR_SECONDARY
        p.add_run(desc)

    # -------------------------------------------------------------
    # SECTION 4: IN-DEPTH PROS & CONS OF EACH PLATFORM
    # -------------------------------------------------------------
    add_custom_heading_1("4. In-Depth Pros & Cons: Voice AI Competitors")

    competitors_detail = [
        ("1. Retell AI (The Recommended Winner)",
         "Retell AI is a developer voice platform specifically optimized for low-latency conversational phone agents.",
         [
             ("Lowest Latency in the Industry (<450ms):", " Conversational turn-taking feels instant, eliminating the awkward pauses seen in older bots."),
             ("Free Self-Signed HIPAA BAA:", " Unlike competitors that charge $2,000/mo, Retell offers a signed BAA on their standard pay-as-you-go plan."),
             ("Native Spanish Voice Quality:", " Outstanding Cartesia Sonic and ElevenLabs integration for Mexican-Spanish accents tailored for Texas demographics."),
             ("Per-Client Workspaces:", " Easy to isolate Shifa Plano from Shifa Garland with separate API keys and tracking.")
         ],
         [
             ("Not a Turnkey Dental Product:", " You must build the dental booking logic and Open Dental API adapter yourself."),
             ("Retell Dashboard is for Developers:", " The end clinic owner cannot log into Retell's dashboard; you must build the Limra web interface.")
         ]),

        ("2. Vapi.ai (The Direct 1:1 Competitor)",
         "Vapi is the most popular direct alternative to Retell, offering granular developer controls.",
         [
             ("Extreme Model Flexibility:", " Swap between OpenAI, Anthropic, Groq, Deepgram, and custom fine-tuned LLMs on the fly."),
             ("Huge Open-Source Community:", " Hundreds of pre-built GitHub boilerplates and active developer Discord support."),
             ("Strong Function Calling:", " Very robust tool execution and webhook schema verification.")
         ],
         [
             ("Prohibitive HIPAA Cost:", " Vapi charges a $2,000/month Enterprise add-on for a signed BAA, making it uneconomical for early pilots."),
             ("Slightly Higher Latency:", " Average response time is ~550ms-650ms, slightly slower than Retell's optimized voice pipeline.")
         ]),

        ("3. Bland AI (The Outbound Calling Specialist)",
         "Bland AI is engineered for high-throughput automated telephone campaigns and enterprise dialers.",
         [
             ("High Outbound Scale:", " Can initiate hundreds of concurrent outbound calls simultaneously for recall campaigns."),
             ("Visual Pathway Builder:", " Drag-and-drop conversational decision trees for complex logic."),
             ("All-in-One Voice Models:", " Proprietary models designed to bypass standard STT-LLM-TTS latency stacking.")
         ],
         [
             ("Tuned for Sales, Not Healthcare:", " Inbound clinical empathy and dental triage feel more scripted and mechanical."),
             ("Unclear BAA Terms:", " Healthcare compliance is buried behind custom enterprise sales contracts."),
             ("Higher Vendor Lock-in:", " Harder to migrate away from their proprietary models.")
         ]),

        ("4. LiveKit Agents (The Open-Source Long-Term Path)",
         "LiveKit is an open-source real-time WebRTC infrastructure framework (Apache 2.0).",
         [
             ("100% Code & Data Ownership:", " No middleman, zero platform markup, completely self-hosted."),
             ("Cheapest at Scale:", " Costs drop to $0.04-$0.06/minute (only raw STT/LLM/TTS and cloud costs)."),
             ("Zero Third-Party HIPAA Exposure:", " Since you host the code in your own AWS HIPAA cloud, all patient audio stays within your private VPC.")
         ],
         [
             ("High Initial Engineering Burden:", " Requires 4 to 8 weeks of specialized senior backend engineering to build and maintain the voice pipeline."),
             ("You Own Infrastructure Reliability:", " If voice packets drop or audio jitters occur, your team has to debug the WebRTC pipeline.")
         ]),

        ("5. Synthflow AI (The No-Code Agency White-Label Tool)",
         "Synthflow is designed for digital agencies that want to resell voice agents without writing code.",
         [
             ("Ready-to-Use White-Label Portal:", " Gives you a client-facing login portal with your logo and domain out of the box."),
             ("No-Code Drag-and-Drop Editor:", " Visual prompt setup and simple webhook triggers.")
         ],
         [
             ("Noticeable Latency (~800ms+):", " Noticeable conversational delay during live phone calls."),
             ("Restricted Customization:", " Cannot easily build complex multi-table Open Dental appointment slot conflict resolution.")
         ]),

        ("6. Dentina AI, Viva AI & Arini AI (Closed Turnkey Dental Agents)",
         "These are ready-made commercial dental receptionists sold directly to dental offices.",
         [
             ("Pre-Built Dental Knowledge:", " Understand dental codes and tooth procedures out of the box."),
             ("Plug-and-Play Setup:", " Can be installed in a clinic within 1 to 2 weeks.")
         ],
         [
             ("Zero White-Labeling or Reselling:", " They will never allow you to rebrand their product as Limra Dental AI."),
             ("Zero Equity Value for Your Company:", " If you resell them, you are just an affiliate earning a 10% commission while they own the customer."),
             ("High Fixed Subscriptions ($300-$900/mo):", " Leaves no room for software gross margins.")
         ])
    ]

    for name, overview, pros, cons in competitors_detail:
        add_custom_heading_2(name)
        p_ov = doc.add_paragraph()
        p_ov.add_run(overview).font.color.rgb = COLOR_DARK
        p_ov.paragraph_format.space_after = Pt(4)

        p_pro_hdr = doc.add_paragraph()
        p_pro_hdr.paragraph_format.space_before = Pt(4)
        p_pro_hdr.paragraph_format.space_after = Pt(2)
        r_ph = p_pro_hdr.add_run("Key Advantages (Pros):")
        r_ph.bold = True
        r_ph.font.color.rgb = COLOR_SECONDARY

        for p_title, p_desc in pros:
            p_p = doc.add_paragraph()
            p_p.paragraph_format.space_after = Pt(2)
            r_pt = p_p.add_run(f"  ✓ {p_title} ")
            r_pt.bold = True
            r_pt.font.color.rgb = COLOR_PRIMARY
            p_p.add_run(p_desc)

        p_con_hdr = doc.add_paragraph()
        p_con_hdr.paragraph_format.space_before = Pt(4)
        p_con_hdr.paragraph_format.space_after = Pt(2)
        r_ch = p_con_hdr.add_run("Key Drawbacks (Cons):")
        r_ch.bold = True
        r_ch.font.color.rgb = COLOR_RED

        for c_title, c_desc in cons:
            p_c = doc.add_paragraph()
            p_c.paragraph_format.space_after = Pt(2)
            r_ct = p_c.add_run(f"  ✗ {c_title} ")
            r_ct.bold = True
            r_ct.font.color.rgb = COLOR_PRIMARY
            p_c.add_run(c_desc)

    # -------------------------------------------------------------
    # SECTION 5: HOW TO IMPLEMENT (STEP-BY-STEP BLUEPRINT)
    # -------------------------------------------------------------
    add_custom_heading_1("5. How to Implement: The Winning Architectural Strategy")

    p = doc.add_paragraph()
    p.add_run("To build a commercially viable SaaS company, we recommend the following phased implementation strategy:\n\n"
              "1. ")
    p.add_run("Phase 1 (Pilot Launch at Shifa Dental): ").bold = True
    p.add_run("Use Retell AI for telephony and low-latency voice orchestration (<450ms). Sign Retell's free self-signed BAA. Build the Open Dental direct REST adapter ($35/mo) in Python FastAPI and connect it via Retell's custom tool calling.\n\n"
              "2. ")
    p.add_run("Phase 2 (The Limra Platform Layer): ").bold = True
    p.add_run("Build the custom web dashboard in Next.js/React. Clinics log in to view call transcripts, listened recordings, appointment conversions, and language metrics under the 'Limra Dental AI' brand.\n\n"
              "3. ")
    p.add_run("Phase 3 (Tri-Agent Expansion): ").bold = True
    p.add_run("Trigger automated insurance verification (Agent 2) via pVerify APIs and pending treatment recall campaigns (Agent 3) via Open Dental database queries.\n\n"
              "4. ")
    p.add_run("Phase 4 (Long-Term Cost Optimization): ").bold = True
    p.add_run("Once Limra reaches 30 to 50 active clinic locations, migrate the underlying voice layer from Retell AI to self-hosted LiveKit Agents. This will cut voice costs in half (from $0.12/min to $0.05/min), driving gross margins above 75%.")

    add_callout("FINAL ACTION ITEM", 
                "Authorize Retell AI + Open Dental Direct API integration for the Shifa Dental pilot. This gives us the fastest time to market (10-12 weeks), zero vendor lock-in, full white-label brand ownership, and the highest conversational 'human touch' available today.", 
                HEX_GREEN_BG, HEX_SECONDARY)

    # Save document
    doc.save(output_path)
    print(f"Comparison document saved successfully to: {output_path}")

if __name__ == "__main__":
    out_file = r"C:\Users\huwai\Desktop\AI Dental Agent\Voice_AI_Competitors_Comparison_and_WhiteLabel_Guide.docx"
    create_comparison_document(out_file)
