# AI Dental Receptionist & Automated Scheduling Agent

This project repository contains the complete architecture, implementation guides, CEO walkthrough scripts, and presentation assets for the **Autonomous AI Dental Voice Receptionist**.

---

## 📁 Project Directory Contents

| File Name | Description |
| :--- | :--- |
| **`AI_Dental_Manager_Architecture_With_Diagram.docx`** | Full comprehensive technical specification Word document, including system architecture, dental triage rules, API schemas, and the embedded 2D architecture diagram. |
| **`AI_Dental_Manager_Presentation_With_Diagram.pptx`** | Executive PowerPoint presentation with 13 widescreen slides, embedded presenter notes for every slide, and the 2D architecture diagram. |
| **`dental_ai_architecture.jpg`** | High-resolution 2D system architecture diagram (Telephony → Retell AI Gateway → Dental PMS / Calendar → SMS Dispatcher). |
| **`generate_ppt.py`** | Python automation script used to generate and customize the presentation slides. |
| **`create_docx.py`** | Python automation script used to compile and generate the Word documentation. |
| **`FULL_CONVERSATION_SUMMARY.md`** | Complete record of the project walkthrough, simple explanations, tool alternatives (n8n vs. Make vs. FastAPI), cost analysis, and CEO presentation script. |

---

## 🧠 System Architecture Overview

```
[ Patient (Inbound Caller) ]
              │ (Phone Call via PSTN)
              ▼
[ Telephony Layer (Twilio SIP & WebSockets Audio) ]
              │ (Live Audio Stream)
              ▼
[ Real-Time Voice AI Gateway (Retell AI / LiveKit) ]
   ├── 1. STT (Deepgram Nova-2 Medical Speech-to-Text <150ms)
   ├── 2. Dental LLM Brain (GPT-4o / Claude with Clinical Triage)
   └── 3. TTS (Cartesia Sonic Voice Synthesis <100ms)
              │
              ├── [ Dental Tool Calling API ]
              │       ├── check_doctor_availability()
              │       └── book_appointment()
              │               │
              │               ▼
              │   [ Dental PMS / Calendar (Open Dental / Dentrix / Google Calendar) ]
              │
              └──► [ Post-Call Dispatcher ]
                      ├── Instant SMS Confirmation (.ics Calendar Invite)
                      └── Doctor Dashboard SOAP Notes
```

---

## 🛠️ Key Technology Stack

- **Telephony & Phone Lines:** Twilio Elastic SIP / DID phone numbers
- **Voice AI Platform:** Retell AI (or Vapi.ai / LiveKit)
- **Speech-to-Text (STT):** Deepgram Nova-2 (Medical/Conversational)
- **Language Model (LLM):** OpenAI GPT-4o / Claude 3.5 Sonnet
- **Text-to-Speech (TTS):** Cartesia Sonic / ElevenLabs Flash
- **Calendar & PMS Sync:** Google Calendar API (free demo/production) or Open Dental / Dentrix APIs
- **Workflow / Glue:** Make.com, n8n, or a lightweight Python FastAPI server

---

## 💰 Cost & Resource Breakdown

- **Development & Testing:** 100% Free on your local machine using developer tiers (Retell \$10 free credits, Twilio \$15 trial, Google Calendar free API).
- **Production Costs:** ~\$0.10 to \$0.15 per completed patient booking call (pay-per-minute, no expensive mandatory \$500/month subscriptions).
