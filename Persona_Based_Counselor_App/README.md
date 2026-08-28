# AI Career Counsellor — Persona-Based Guidance (Gemini API)

A single-page web app where a student asks one career question and receives answers from up to four distinct AI counsellor personas — each with its own Role, Audience, Context, Format, Constraints, and Language — generated live by the **Gemini API**.

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

## 6. Screenshots

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

### Demo
[Watch Demo Video](YOUR_DEMO_VIDEO_LINK)

## 7. Six-Element Prompt Cards

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

## 8. Persona Differentiation Strategy

Differentiation is enforced at three levels:

1. **Prompt level** — every persona's full Prompt Card (all six elements) is sent to Gemini, and the instruction explicitly tells the model that personas must not imitate each other or converge on one generic answer.
2. **Structural level** — each persona has its own `Format`, so a Technical answer is shaped as a roadmap while an HR answer is shaped as an employability assessment — the *shape* of the answer differs, not just the wording.
3. **Verification level** — the frontend requests a `priority` and `mainRecommendation` field per persona and renders them side by side in the comparison table, making it visually obvious when two personas actually agree vs. disagree.

## 9. Prompt Construction Flow

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

## 10. Multi-Persona API Strategy

When multiple personas are selected, the app does **not** fire one API call per persona. Instead:

- All selected personas' Prompt Cards are concatenated into a single prompt.
- The prompt explicitly instructs Gemini to answer once per persona, independently, without blending perspectives.
- The request sets `generationConfig.responseMimeType: "application/json"` and a `responseSchema` describing an array of `{ persona, response, mainRecommendation, priority, suggestedAction }` objects, so Gemini returns structured, machine-parseable output in one round trip.
- The frontend then matches each returned entry back to the persona that was selected (by name, with a positional fallback), and flags anything unexpectedly missing.

This keeps the app to **one Gemini request regardless of how many personas are selected**, minimizing latency and rate-limit usage.

## 11. Technology Used

- Vanilla HTML5, CSS3, JavaScript (ES6+) — no framework, no build step.
- Google Fonts (Lora, IBM Plex Mono, Inter) via CDN `<link>`.
- Gemini API (`generateContent` endpoint) called directly via `fetch`.

## 12. Gemini API Integration

- Endpoint: `https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={apiKey}`
- Default model: `gemini-3.5-flash` — editable in the "Gemini model" field in the setup panel, since Google periodically renames/retires model versions. If a model name stops working, check Google's current model list and type the new name into that field.
- Called directly from the browser (`fetch`), with the API key supplied at runtime by the student — no key is ever stored in the code or repository.

## 13. Application Architecture

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

## 14. Comparison Functionality

When two or more personas are selected, the app renders a table with one column per persona and one row each for **Main Recommendation**, **Top Priority**, and **Suggested Next Action** — all populated from the same single Gemini response, not a separate summarization call.

## 15. Limitations

- Persona differentiation depends on Gemini following the prompt; while the schema and instructions are designed to make convergence unlikely, no hard guarantee exists that two personas won't occasionally overlap on straightforward questions.
- The comparison table summarizes each persona in three short fields — it is not a substitute for reading the full response.
- No conversation memory: each question is a fresh request.

## 16. Possible Future Improvements

- Optional backend proxy to fully hide the API key for public deployment.
- Persona response history / session log.
- Ability for students to define and save their own custom persona Prompt Cards.
- Export comparison table as PDF/CSV.

## 17. Learning Outcomes

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

## 18. How to Use the Application

This application is a client-side, single-page AI Career Counsellor powered by the Google Gemini API. GitHub users can run it locally and interact with multiple AI career-counsellor personas.

### 1. Download or Clone the Repository

Clone the repository using:

```bash
git clone https://github.com/SaurabhBhuptani/PEGAI/tree/main/Persona_Based_Counselor_App.git
```

Then enter the project directory:

```bash
cd Persona_Based_Counselor_App
```

Alternatively, click **Code → Download ZIP** on GitHub and extract the project.

### 2. Get a Gemini API Key

The application requires a Gemini API key to generate career advice.

Create a key through **Google AI Studio**:

https://aistudio.google.com/

Copy your API key after creating it.

> **Security Warning:** Do not add your Gemini API key to `index.html`, commit it to GitHub, or upload it anywhere publicly. This project accepts the key at runtime for demonstration purposes.

### 3. Start the Application

The application is contained entirely in `index.html`.

For the most reliable experience, run it through a local HTTP server.

#### Using Python

Make sure Python is installed, then run:

```bash
python -m http.server 8000
```

Open the following address in your browser:

```text
http://localhost:8000
```

You can also use VS Code's **Live Server** extension to open `index.html`.

### 4. Enter Your Gemini API Key

When the application opens:

1. Expand **Gemini API setup**.
2. Paste your Gemini API key into the API key field.
3. Verify the Gemini model shown in the model field.
4. Keep the key only for the current browser session.

The application does not require the API key to be stored inside the project files.

### 5. Enter a Career Question

Type a career-related question into the question box.

Example:

```text
Should I prepare for placements or pursue higher studies?
```

The application also provides sample-question buttons that can automatically populate the question field.

### 6. Select One or More Counsellors

Choose at least one persona from the available counsellors:

- **Technical Career Counsellor** — AI/ML, programming, software development, DSA, projects and technical preparation.
- **HR & Placement Counsellor** — resumes, interviews, internships, communication and employability.
- **Academic & Research Counsellor** — MS/M.Tech, PhD, research, certifications and higher-study preparation.
- **Entrepreneurship Counsellor** — startups, freelancing, product ideas, business opportunities and market validation.

You may select a single persona or multiple personas.

### 7. Generate Career Advice

Click:

**Get Career Advice**

The selected persona instructions and your question are combined into a structured prompt and sent to Gemini.

For a single selected persona, the application displays one persona-specific response.

For multiple selected personas, the same question is processed from each selected perspective and the responses are displayed separately.

### 8. Compare Multiple Perspectives

When multiple personas are selected, the application also provides a comparison section.

It summarizes aspects such as:

- Main recommendation
- Top priority
- Suggested next action

This makes it easier to understand how different career perspectives lead to different recommendations.

### 9. Try Different Questions

Some useful questions to try are:

```text
Should I prepare for placements or pursue higher studies?
```

```text
I know Python but do not have any projects. What should I do?
```

```text
Should I become an AI Engineer, Data Scientist or Software Developer?
```

For the best demonstration, try the same question with different combinations of counsellors and compare how their recommendations differ.

### 10. Handling Errors

The application provides basic validation and error handling.

Examples include:

- No persona selected → `Please select at least one persona.`
- Empty question → `Please enter your career-related question.`
- Missing API key → asks you to enter the key.
- Invalid API key → displays a Gemini API error.
- Network/API problems → displays a user-friendly error instead of crashing.

### 11. Clear Results and Start Again

Use **Clear results** to remove the current responses and comparison table.

You can then enter another question, select different personas, and generate a new set of recommendations.

### Typical User Flow

```text
Open Repository
      ↓
Run index.html locally
      ↓
Enter Gemini API Key
      ↓
Enter Career Question
      ↓
Select One or More Personas
      ↓
Click "Get Career Advice"
      ↓
Gemini Generates Persona-Specific Responses
      ↓
View Individual Responses
      ↓
Compare Recommendations
      ↓
Try Another Question
```

### Quick Start

For experienced users:

```bash
git clone https://github.com/SaurabhBhuptani/PEGAI/tree/main/Persona_Based_Counselor_App.git
cd Persona_Based_Counselor_App
python -m http.server 8000
```

Then visit:

```text
http://localhost:8000
```

Enter a Gemini API key in the application's setup panel, select one or more counsellors, enter a career-related question, and click **Get Career Advice**.
