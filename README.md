# Student Report AI System
### AI-powered parent conference report system for Singapore secondary schools

**Portfolio project by Eva Sun Guizi** · Data Scientist Application · SG Secondary School

---

## Live Demo

| File | Description |
|------|-------------|
| [Portfolio Overview](portfolio.html) | Start here — project summary and navigation |
| [ReportReady](reportready_v2.html) | Main system — teacher comments + AI report generation |
| [School Analytics Dashboard](school_analytics.html) | Leadership intelligence — upload CSV to view school-wide analytics |

> **To run locally:** Download all files into one folder and open `portfolio.html` in your browser. All files must be in the same folder for links to work.

---

## The Problem

Every Parent-Teacher Conference, teachers spend days before the event opening School Cockpit for CCA records, RPMS for existing reports, and multiple Excel files from subject teachers — just to piece together a complete picture of one student. Nothing talks to anything else.

- **Fragmented data** — grades in RPMS, CCA in Cockpit, comments in individual Excel files
- **Repetitive manual work** — teachers copy-pasting scores into comment templates
- **No early warning** — at-risk students identified reactively, after exam results, not before

---

## What This System Does

### Module 1 — Data Pipeline (`student_pipeline.py`)
A Python ETL pipeline that simulates 500 student records across four data domains — academics, attendance, CCA, and pastoral — then applies a **weighted risk-scoring model** to classify every student into High, Medium, or Low risk tiers.

```
Academic (50%) + Attendance (30%) + Behavioural (20%) → Risk Score 0–100
```

In production, this pipeline would connect directly to School Cockpit and RPMS via API, replacing the manual Excel upload step.

**Output files:**
- `student_analytics.csv` — 500 students, 25 features, feeds the analytics dashboard
- `high_risk_students.csv` — high-risk subset for AI letter generation
- `class_summary.csv` — 16-class aggregated summary for leadership reporting

---

### Module 2 — ReportReady (`reportready_v2.html`)
A full web application that replaces the fragmented pre-conference workflow.

**Subject Teacher view:**
- Select subject (English, Mathematics, Science, Mother Tongue, Humanities, Art)
- See each student's WA1, WA2, and Semester 1 average
- Write comments or click **AI Draft** to generate a starting point
- Upload score Excel — system auto-matches students by Student ID

**Form Teacher view (Ms Sun Guizi):**
- Overview — class comment completion status, progress per student
- Analytics — class-level charts: subject performance, WA1 vs WA2, risk distribution
- **Generate AI Parent Letter** — Claude synthesises all subject comments + student data into a personalised 300-word parent letter
- **Send via Email** — review, edit, and send directly to parents
- System Design — data architecture, privacy principles, PDPA compliance, n8n roadmap
- Sent Log — full audit trail of every email sent

---

### Module 3 — School Analytics Dashboard (`school_analytics.html`)
A leadership-level intelligence dashboard that reads `student_analytics.csv` and renders four charts:

| Chart | Intelligence type |
|-------|------------------|
| Subject performance — school average | Diagnostic |
| Risk distribution by year level | Predictive |
| Attendance trend — Sem 1 vs Sem 2 | Evaluative |
| Classes ranked by at-risk student count | Evaluative |

Includes a filterable high-risk student table with risk score explanation.

> Click **"Try with sample data"** to see the dashboard without uploading a file.

---

## How the Files Connect

```
student_pipeline.py
        ↓ generates
student_analytics.csv  ──→  school_analytics.html  (leadership dashboard)
high_risk_students.csv ──→  ReportReady AI letters  (Module 2 & 3)
class_summary.csv      ──→  class-level reporting

Teacher Excel files ──→  ReportReady Upload tab  (Student ID join)
                                ↓
                    Unified student record
                                ↓
                    AI-generated parent letter
                                ↓
                    Email to parent + audit log
```

In production, the manual Excel upload would be replaced by an **n8n automation workflow** — scores updated in Google Classroom trigger an automatic pipeline run, and form teachers are notified of newly flagged students every Monday morning.

---

## Key Design Decisions

**Student ID as universal join key** — stable across all school systems, enables reliable cross-source matching without name-matching errors.

**Client-side Excel parsing (SheetJS)** — student data never leaves the teacher's device. No server required, no PDPA risk from data transmission.

**Human-in-the-loop before every send** — AI drafts letters, but a teacher must review and approve before anything is sent. Every action is logged with timestamp and approver.

**Risk score weights informed by education research** — attendance is weighted at 30% because chronic absenteeism is the earliest detectable indicator of student disengagement, often appearing before academic decline.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Data pipeline | Python, pandas, NumPy |
| AI letter generation | Claude API (claude-sonnet-4-6) |
| Frontend | HTML, CSS, JavaScript |
| Excel parsing | SheetJS (client-side) |
| Data visualisation | Chart.js |
| CSV parsing | Papa Parse |
| Deployment | GitHub Pages |

---

## Data Privacy

All student data in this portfolio is **fully simulated**. No real student information was used at any stage. The simulation mirrors realistic Singapore secondary school data distributions for demonstration purposes only.

---

## About

**Eva Sun Guizi** — Former MOE teacher with 7 years in Singapore secondary schools, transitioning into data science. This portfolio demonstrates how domain knowledge and technical skills combine to solve real problems in education.

*Built as a portfolio project for a Data Scientist role at a Singapore secondary school, 2026.*
