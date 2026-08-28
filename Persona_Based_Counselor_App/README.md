# AI Career Counsellor — Persona-Based Guidance (Gemini API)

A single-page web app where a student asks one career question and receives answers from up to four distinct AI counsellor personas — each with its own Role, Audience, Context, Format, Constraints, and Language — generated live by the **Gemini API**.

---

## 1. Project Overview

This project fulfils an assignment brief requiring a web-based AI Persona Application built on the Gemini API, where selecting a different persona produces a **meaningfully different** answer to the same question — not just a relabeled one. The whole implementation (HTML, CSS, JavaScript) lives in a single `index.html` file, as required.

## 2. Problem Statement

Students often ask career questions ("Should I do placements or higher studies?") that have no single right answer — the "right" advice depends on whose lens you're looking through. A generic chatbot gives one homogenized answer. This app instead simulates four specialist counsellors so the student can see the tradeoffs across perspectives side by side.

## 3. Objective

- Demonstrate genuine **persona prompt engineering** using a six-element Prompt Card (Role, Audience, Context, Format, Constraints, Language).
- Let a student compare how a Technical, HR, Academic, and Entrepreneurship counsellor would each answer the *same* question.
- Do all of this with real Gemini-generated text — nothing is hard-coded.
- Handle multiple personas **efficiently**, using one Gemini request rather than one call per persona.

## 4. Key Features

- 4 built-in personas, each defined by a full six-element Prompt Card.
- Single or multi-persona selection via clickable "file" cards.
- One Gemini API request handles any number of selected personas at once (structured JSON output).
- Per-persona response cards, visually colour-coded by persona.
- An automatic comparison table (Main Recommendation / Priority / Suggested Action) when more than one persona is selected.
- Runtime-only API key entry (never stored, never committed).
- Loading state, empty state, and explicit error states for every failure mode listed in the assignment.
- Fully responsive, single-file, dependency-light (Google Fonts only).

## 5. Personas

| Persona | Focus |
|---|---|
| **Technical Career Counsellor** | AI/ML, programming, software development, DSA, projects, technical career prep |
| **HR & Placement Counsellor** | Resumes, interviews, employability, recruitment, internships, communication |
| **Academic & Research Counsellor** | MS/M.Tech, PhD, research, certifications, higher-study preparation |
| **Entrepreneurship Counsellor** | Startups, freelancing, product ideas, market validation, business opportunities |

## 6. Six-Element Prompt Cards

### Persona 1 — Technical Career Counsellor
- **Role:** Senior Technical Career Counsellor specializing in AI, ML and Software Engineering.
- **Audience:** Undergraduate ICT/Computer Science students.
- **Context:** The student is interested in technology careers and needs practical guidance about technical skills, projects, preparation, and career opportunities.
- **Format:** Recommendation + Skills to Develop + Project Suggestions + Career Roadmap.
- **Constraints:** Give practical and realistic advice. Do not guarantee jobs or salaries. Avoid unsupported assumptions.
- **Language:** Simple English.

### Persona 2 — HR & Placement Counsellor
- **Role:** Senior HR & Placement Counsellor specializing in campus recruitment, resumes, and interview readiness.
- **Audience:** Undergraduate ICT/Computer Science students preparing for placements and internships.
- **Context:** The student needs guidance on becoming employable — resumes, interviews, communication skills, and recruitment readiness — rather than deep technical skill-building.
- **Format:** Employability Assessment + Resume/Interview Focus Areas + Placement-Readiness Action Plan.
- **Constraints:** Do not guarantee placement, job offers, or salaries. Focus on employability signals recruiters look for, not raw technical depth. Avoid unsupported assumptions about the student's current resume.
- **Language:** Simple, professional English.

### Persona 3 — Academic & Research Counsellor
- **Role:** Senior Academic & Research Counsellor specializing in higher studies (MS/M.Tech/PhD), research, and certifications.
- **Audience:** Undergraduate ICT/Computer Science students considering higher education or research paths.
- **Context:** The student wants to know whether and how to pursue postgraduate study, research exposure, or certifications alongside or instead of industry entry.
- **Format:** Academic Fit Assessment + Research/Certification Suggestions + Higher-Study Roadmap.
- **Constraints:** Do not guarantee admission to any program. Avoid overstating the value of any single certification. Be realistic about the time and effort research and higher studies require.
- **Language:** Simple English with academic terms explained plainly.

### Persona 4 — Entrepreneurship Counsellor
- **Role:** Senior Entrepreneurship & Startup Counsellor specializing in student ventures, freelancing, and early product validation.
- **Audience:** Undergraduate ICT/Computer Science students exploring startups, freelancing, or independent product-building.
- **Context:** The student wants to know whether an idea, freelance path, or startup is worth pursuing, and what to try first.
- **Format:** Opportunity Assessment + Validation Steps + First Actions to Test the Idea.
- **Constraints:** Do not guarantee business success or funding. Do not encourage dropping out of studies. Emphasize low-cost validation before big commitments.
- **Language:** Simple, motivating English.

All four cards live in one place in the code — the `PERSONAS` object near the top of the `<script>` block in `index.html` — so they're easy to edit or extend.

## 7. Persona Differentiation Strategy

Differentiation is enforced at three levels:

1. **Prompt level** — every persona's full Prompt Card (all six elements) is sent to Gemini, and the instruction explicitly tells the model that personas must not imitate each other or converge on one generic answer.
2. **Structural level** — each persona has its own `Format`, so a Technical answer is shaped as a roadmap while an HR answer is shaped as an employability assessment — the *shape* of the answer differs, not just the wording.
3. **Verification level** — the frontend requests a `priority` and `mainRecommendation` field per persona and renders them side by side in the comparison table, making it visually obvious when two personas actually agree vs. disagree.

## 8. Prompt Construction Flow

```
Role
  +
Audience
  +
Context
  +
Format
  +
Constraints
  +
Language
  +
User Question
  ↓
Final Prompt (one persona block per selected persona)
  ↓
Gemini API (generateContent, single request)
  ↓
Structured JSON Response
  ↓
Parsed → Rendered per persona + Comparison table
```

## 9. Multi-Persona API Strategy

When multiple personas are selected, the app does **not** fire one API call per persona. Instead:

- All selected personas' Prompt Cards are concatenated into a single prompt.
- The prompt explicitly instructs Gemini to answer once per persona, independently, without blending perspectives.
- The request sets `generationConfig.responseMimeType: "application/json"` and a `responseSchema` describing an array of `{ persona, response, mainRecommendation, priority, suggestedAction }` objects, so Gemini returns structured, machine-parseable output in one round trip.
- The frontend then matches each returned entry back to the persona that was selected (by name, with a positional fallback), and flags anything unexpectedly missing.

This keeps the app to **one Gemini request regardless of how many personas are selected**, minimizing latency and rate-limit usage.

## 10. Technology Used

- Vanilla HTML5, CSS3, JavaScript (ES6+) — no framework, no build step.
- Google Fonts (Lora, IBM Plex Mono, Inter) via CDN `<link>`.
- Gemini API (`generateContent` endpoint) called directly via `fetch`.

## 11. Gemini API Integration

- Endpoint: `https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={apiKey}`
- Default model: `gemini-2.0-flash` — editable in the "Gemini model" field in the setup panel, since Google periodically renames/retires model versions. If a model name stops working, check Google's current model list and type the new name into that field.
- Called directly from the browser (`fetch`), with the API key supplied at runtime by the student — no key is ever stored in the code or repository.

## 12. Application Architecture

```
User
  │
  ▼
Question Input ──► Persona Selection ──► Read Prompt Cards
                                             │
                                             ▼
                              Construct Structured Prompt
                                             │
                                             ▼
                               ONE Gemini API Request
                                             │
                                             ▼
                             Parse Structured JSON Response
                                             │
                              ┌──────────────┴──────────────┐
                              ▼                              ▼
                 Render Individual Persona Cards   Render Comparison Table
                              │                              │
                              └──────────────┬───────────────┘
                                             ▼
                                     User Evaluation
```

## 13. Repository Structure

```
project/
│
├── index.html      # Complete app: HTML + CSS + JavaScript
├── README.md        # This file
└── assets/          # Screenshots for this README (add your own)
```

`index.html` intentionally contains the entire implementation — no separate `style.css` or `script.js` files, per the assignment's single-file constraint.

## 14. Complete Setup Instructions

### Step 1 — Prerequisites
- A modern browser (Chrome, Edge, Firefox, or Safari).
- A free Google account to obtain a Gemini API key.
- Optionally, Python or Node.js installed, to serve the file locally (see Step 6).

### Step 2 — Obtain Gemini API access
Get a free API key from **Google AI Studio** (`aistudio.google.com` → "Get API key"). Treat this key like a password. **Never commit it to GitHub.**

### Step 3 — Clone/download the repository
```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
```

### Step 4 — Inspect project structure
- `index.html` — the entire application.
- `README.md` — this documentation.
- `assets/` — where you'll drop your own screenshots before submission.

### Step 5 — Configure runtime API access
This app deliberately does **not** ship with a key. Open `index.html` in your browser, expand the **"⚙ Gemini API setup"** panel at the top, and paste your key into the **"Your Gemini API key"** field. The key is held only in the page's JavaScript memory for that session — it is never written to disk, `localStorage`, or the repository.

### Step 6 — Launch the application
Some browsers restrict `fetch` requests from files opened directly as `file://`. Prefer a simple local server:

**Beginner-friendly (Python, usually pre-installed):**
```bash
python3 -m http.server 8000
```
Then open `http://localhost:8000/index.html`.

**Alternative (Node.js):**
```bash
npx serve .
```

You can also just double-click `index.html` — most current browsers will run it fine, but use the local-server method if you see network/CORS errors.

### Step 7 — Open the app
Navigate to the local URL from Step 6 (or open the file directly). You'll see the header, the API setup panel, the question box, and the four persona cards.

### Step 8 — Select a persona
Click any single persona card (e.g. "Technical Career Counsellor") to select it — it will highlight with a bold outline.

### Step 9 — Ask a career question
Type a question, e.g. *"I know Python and basic Machine Learning. What should I learn to become an AI Engineer?"* — or click one of the three sample-question chips to autofill.

### Step 10 — Generate advice
Click **Get Career Advice**. The button shows a loading spinner while Gemini responds; a single response card appears for your selected persona.

### Step 11 — Use multiple personas
Click additional persona cards before generating — try all four at once.

### Step 12 — Compare results
With two or more personas selected, a **comparison table** appears beneath the response cards, showing Main Recommendation / Priority / Suggested Action side by side.

### Step 13 — Troubleshoot errors

| Problem | What you'll see | Fix |
|---|---|---|
| No persona selected | "Please select at least one persona." | Select a persona card. |
| Empty question | "Please enter your career-related question." | Type a question. |
| Missing API key | Setup panel auto-opens with an error banner | Paste a valid key. |
| Invalid key / wrong model name | "Gemini rejected the request…" | Re-check the key and model field. |
| Network/CORS failure | "Could not reach the Gemini API…" | Serve via local HTTP server (Step 6); check your connection. |
| Rate limiting | "Gemini is rate-limiting requests…" | Wait, then retry. |
| Unexpected/empty response | "Gemini returned an empty response…" / "…unexpected format…" | Retry, or rephrase the question. |

### Step 14 — Run the test cases
See Section 15 below.

### Step 15 — Prepare GitHub submission
Commit `index.html`, `README.md`, and your `assets/` screenshots. **Do not** commit any file containing your real API key.

### Step 16 — Prepare demo video
See Section 18 checklist below.

### Step 17 — Final submission
See Section 19 checklist below.

## 15. Testing Procedure

Test with all three required questions, in both single- and multi-persona mode:

1. *"Should I prepare for placements or pursue higher studies?"*
2. *"I know Python but do not have any projects. What should I do?"*
3. *"Should I become an AI Engineer, Data Scientist or Software Developer?"*

For each question:
- Run it against **one persona at a time** (all four, individually).
- Run it against **all four personas together**.
- Run it against **at least one other combination** (e.g. Technical + Entrepreneurship only).
- Confirm the responses are structurally and substantively different — e.g. for Question 1, the Technical counsellor should foreground DSA/projects, HR should foreground employability signals, Academic should foreground research/postgrad fit, and Entrepreneurship should foreground opportunity cost of building vs. studying.

Record your actual observations (screenshots or notes) here before submission.

## 16. Error Handling

Implemented for: no persona selected, empty question, missing API key, invalid API key, network failure, invalid/unexpected JSON, empty AI response, and HTTP 429 rate limiting. All errors are shown as a readable banner near the Generate button — the app never crashes to a blank screen, and no internal error detail beyond Gemini's own message is exposed.

## 17. Demo Video Checklist

- [ ] Show the application interface.
- [ ] Show the four available personas and their focus areas.
- [ ] Select one persona.
- [ ] Enter a question.
- [ ] Show the generated response.
- [ ] Select multiple personas.
- [ ] Ask the same question again.
- [ ] Show the multiple generated responses.
- [ ] Show the comparison section.
- [ ] Briefly explain the Prompt Card (Role/Audience/Context/Format/Constraints/Language).
- [ ] Briefly explain the prompt-construction flow (Section 8 above).
- [ ] Demonstrate that multiple personas are handled in one Gemini request (e.g. show the Network tab with a single request for a multi-persona run).

## 18. Screenshots

*(Add your own screenshots to `assets/` before submitting, then these will render on GitHub.)*

### Homepage
![Homepage Screenshot](assets/homepage.png)

### Persona Selection
![Persona Selection](assets/persona-selection.png)

### Single Persona Response
![Single Persona Response](assets/single-persona-response.png)

### Multiple Persona Responses
![Multiple Persona Responses](assets/multiple-persona-responses.png)

### Comparison
![Persona Comparison](assets/persona-comparison.png)

## Application Flow

![Application Flow](assets/application-flow.png)

## Demo

[Watch Demo Video](YOUR_DEMO_VIDEO_LINK)

## 19. Comparison Functionality

When two or more personas are selected, the app renders a table with one column per persona and one row each for **Main Recommendation**, **Top Priority**, and **Suggested Next Action** — all populated from the same single Gemini response, not a separate summarization call.

## 20. Limitations

- The Gemini API key is entered and used client-side, which is appropriate for an educational single-page demo but is **not** a secure pattern for a real production app (see Section 21 — Security).
- Persona differentiation depends on Gemini following the prompt; while the schema and instructions are designed to make convergence unlikely, no hard guarantee exists that two personas won't occasionally overlap on straightforward questions.
- The comparison table summarizes each persona in three short fields — it is not a substitute for reading the full response.
- No conversation memory: each question is a fresh request.

## 21. Security — API Key Handling

**Critical:** this repository contains **no real API key**. The app prompts the student for their key at runtime, and it is held only in browser memory for that page session (never written to `localStorage`, `sessionStorage`, cookies, or any file).

However, because the Gemini request is made directly from the browser, the key **is technically visible** to anyone inspecting network traffic in that browser tab while the app is running. This is acceptable for a personal/educational demo run locally, but:
- Never commit a real key to `.env`, source code, or GitHub.
- Never deploy this pattern publicly with a real key pasted in by default.
- For a production app, the correct pattern is a backend proxy that holds the key server-side — intentionally out of scope here per the assignment's "don't overengineer" constraint.

## 22. Possible Future Improvements

- Optional backend proxy to fully hide the API key for public deployment.
- Persona response history / session log.
- Ability for students to define and save their own custom persona Prompt Cards.
- Export comparison table as PDF/CSV.

## 23. Team Members

- *(List team members here.)*

## 24. Final Submission Checklist

- [ ] `index.html` works
- [ ] HTML/CSS/JS are in one file
- [ ] At least 4 personas exist
- [ ] One persona works
- [ ] Multiple personas work
- [ ] Gemini API generates responses
- [ ] Multi-persona mode uses one Gemini request
- [ ] Persona responses are meaningfully different
- [ ] Six Prompt Card elements are defined for every persona
- [ ] Input validation works
- [ ] API errors are handled
- [ ] Required test questions tested (Section 15)
- [ ] Screenshots added to `assets/`
- [ ] Demo video prepared
- [ ] Prompt Card documentation prepared (Section 6)
- [ ] Team members listed (Section 23)
- [ ] No real API key is committed
- [ ] GitHub repository is ready for submission

## 25. Learning Outcomes

This project demonstrates:

```
Design a Persona → Define the Audience → Provide Context → Control the Output Format
  → Apply Constraints → Specify Language → Add User Input
  → Generate a Persona-Specific Response using Gemini
```

And, for multiple personas:

```
One User Question → Multiple Persona Instructions → One Efficient Gemini API Request
  → Multiple Distinct Perspectives → Meaningful Comparison
```

The project's success is measured by the **quality of the persona prompt design** and the **meaningfulness of the differences** between persona outputs — not by chatbot novelty alone.
