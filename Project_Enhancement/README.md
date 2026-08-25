# 🤖 Gemini Smart Chatbot

A multimodal AI chatbot built with **Python, Streamlit, LangGraph, Google Gemini, SQLite, and Hugging Face Inference Providers**.

The project combines conversational AI, prompt engineering, code assistance, file analysis, image understanding, image generation, and persistent conversation management in a single beginner-friendly application.

---

## 📸 Project Preview

### 🏠 Main Chat Interface

<!-- Replace this placeholder with your screenshot -->

![Main Chat Interface](images/main-interface.png)

> **Screenshot placeholder:** Add a screenshot of the main Streamlit chatbot interface here.

---

### ⚙️ AI Modes

<!-- Replace this placeholder with your screenshot -->

![AI Modes](images/ai-modes.png)

The application currently provides two response modes:

* **General Assistant** — general-purpose conversational assistance.
* **Code Assistant** — programming-focused explanations, debugging, code generation, and code improvement.

---

### 🔍 Chat Search

<!-- Replace this placeholder with your screenshot -->

![Chat Search](images/chat-search.png)

Search previous conversations by:

* Chat title
* Message content
* Matching conversation snippets

---

### 🗑️ Chat Deletion

<!-- Replace this placeholder with your screenshot -->

![Chat Deletion](images/chat-delete.png)

Users can delete individual conversation threads without affecting other chats.

---

### 💻 Code File Analysis

<!-- Replace this placeholder with your screenshot -->

![Code File Analysis](images/code-file-analysis.png)

Upload supported programming/text files and ask the Code Assistant to:

* Explain code
* Debug code
* Find errors
* Refactor code
* Improve code
* Generate revised code

The generated code can be downloaded directly from the application.

---

### 🖼️ Image Understanding

<!-- Replace this placeholder with your screenshot -->

![Image Analysis](images/image-analysis.png)

Upload an image and ask Gemini questions about its content.

Example:

> "Explain this diagram."

---

### 🎨 Image Generation

<!-- Replace this placeholder with your screenshot -->

![Image Generation](images/image-generation.png)

Generate images from natural-language descriptions using **Hugging Face Inference Providers**.

Example:

> "A futuristic university campus surrounded by mountains at sunset, cinematic digital art."

Generated images can be downloaded as PNG files.

---

## ✨ Features

### 💬 AI Conversation

* Natural-language conversation using Google Gemini.
* Streaming AI responses.
* Persistent conversation context.
* Multiple independent chat threads.
* New-chat creation.
* Previous conversation loading.

### 🧠 Prompt-Engineered Response Modes

#### General Assistant

Designed for:

* General questions
* Explanations
* Learning
* Summaries
* Everyday assistance

#### Code Assistant

Designed for:

* Programming questions
* Debugging
* Code explanation
* Code generation
* Refactoring
* Code improvement

The assistant behavior changes dynamically according to the selected mode.

---

### 🔎 Searchable Chat History

Search through stored conversations using:

* Conversation titles
* User messages
* Assistant messages
* Matching text snippets

Chat search is performed locally using SQLite-backed conversation data and does not require an additional AI or vector-search service.

---

### 🗑️ Conversation Management

Users can:

* Create new conversations.
* Open existing conversations.
* Search conversations.
* Delete individual conversations.
* Continue previous conversations.

---

### 📁 Code/Text File Input

Supported extensions currently include:

```text
.py
.js
.java
.c
.cpp
.cs
.html
.css
.sql
.json
.txt
```

Uploaded files are read as text and provided as context to the Code Assistant.

The application does **not execute uploaded code**.

---

### 📥 Code Output

When Gemini returns code in Markdown code blocks, the application extracts the code and provides a download button.

This allows workflows such as:

```text
Upload source file
        ↓
Code Assistant
        ↓
Analyze / Debug / Improve
        ↓
Generated code
        ↓
Download revised file
```

---

### 🖼️ Image Input

Supported image formats:

```text
PNG
JPG
JPEG
WEBP
```

Images can be uploaded and analyzed using Gemini's multimodal capabilities.

Examples:

* Explain diagrams.
* Analyze screenshots.
* Interpret visual content.
* Ask questions about an image.
* Understand educational figures.

---

### 🎨 Image Generation

Image generation is implemented separately from the Gemini conversational model.

The application uses:

```text
Hugging Face Inference Providers
        ↓
Qwen-Image
        ↓
Generated Image
```

The generated image can be displayed in Streamlit and downloaded as a PNG.

> **Note:** Hugging Face Inference Provider usage is subject to the account's current credits, provider availability, and applicable limits.

---

### 💾 Persistent Conversation Storage

Conversation state is stored using:

```text
SQLite
+
LangGraph SQLite Checkpointing
```

This allows conversations to remain available after restarting the Streamlit application.

---

## 🧠 Prompt Engineering

Prompt engineering is a central part of this project.

Instead of sending every request to the language model using the same instructions, the application dynamically selects task-specific prompts.

### General Assistant Prompt

The General Assistant is instructed to:

* Provide clear and accurate answers.
* Adapt the explanation depth to the question.
* Use Markdown when useful.
* Avoid unnecessary code.

### Code Assistant Prompt

The Code Assistant is instructed to:

* Identify programming languages when possible.
* Explain the programming approach.
* Analyze syntax, logical, and runtime issues.
* Provide corrected or improved code.
* Explain important changes.
* Preserve the user's intent.
* Never claim that code was executed unless it was actually executed.

### Image Generation Prompt Engineering

User image descriptions are passed through an additional prompt-enhancement layer before being sent to the image-generation model.

The enhancement instructs the image model to consider:

* Subject
* Composition
* Lighting
* Environment
* Mood
* Artistic style

Conceptually:

```text
User Image Description
          ↓
Prompt Enhancement
          ↓
Structured Image Prompt
          ↓
Hugging Face Image Model
          ↓
Generated Image
```

---

## 🏗️ System Architecture

```text
                           ┌──────────────────────┐
                           │      Streamlit       │
                           │      Web UI          │
                           └──────────┬───────────┘
                                      │
                 ┌────────────────────┼────────────────────┐
                 │                    │                    │
                 ▼                    ▼                    ▼
          Chat Management        AI Chat Modes       Image Generation
                 │                    │                    │
                 ▼                    ▼                    ▼
              SQLite             LangGraph          Hugging Face
                 │                    │              Inference API
                 │                    ▼
                 │              Google Gemini
                 │                    │
                 │            ┌───────┴────────┐
                 │            │                │
                 │       General Mode      Code Mode
                 │
                 └───────────────┐
                                 ▼
                         Persistent History
```

---

## 🔄 Chat Request Flow

A normal chat request follows:

```text
User
 ↓
Streamlit
 ↓
Selected AI Mode
 ↓
LangGraph
 ↓
System Prompt
 ↓
Conversation History
 ↓
Google Gemini
 ↓
Streaming Response
 ↓
Streamlit
 ↓
SQLite Checkpoint
```

---

## 💻 Code Analysis Flow

```text
User uploads source file
        ↓
File validation
        ↓
Read file as text
        ↓
Code Assistant mode
        ↓
Dynamic prompt construction
        ↓
Google Gemini
        ↓
Analysis / corrected code
        ↓
Code extraction
        ↓
Download button
```

---

## 🖼️ Image Analysis Flow

```text
User uploads image
        ↓
Validate image
        ↓
Convert image to supported request format
        ↓
Combine image + user question
        ↓
Google Gemini
        ↓
Multimodal response
```

---

## 🎨 Image Generation Flow

```text
User enters image description
        ↓
Prompt enhancement
        ↓
Hugging Face Inference Providers
        ↓
Qwen-Image
        ↓
Generated PIL image
        ↓
Streamlit preview
        ↓
PNG download
```

---

## 🗃️ Project Structure

```text
Project/
│
├── app.py
├── backend.py
├── .env
├── .gitignore
├── chatbot.db
│
├── venv/
│
└── images/
    ├── main-interface.png
    ├── ai-modes.png
    ├── chat-search.png
    ├── chat-delete.png
    ├── code-file-analysis.png
    └── image-generation.png
```

> `chatbot.db` is created automatically when the application uses SQLite checkpointing.

---

## 🛠️ Technologies Used

| Technology                           | Purpose                                                   |
| ------------------------------------ | --------------------------------------------------------- |
| **Python**                           | Core programming language                                 |
| **Streamlit**                        | Web interface                                             |
| **LangGraph**                        | Conversation-state and workflow management                |
| **LangChain**                        | LLM integration                                           |
| **Google Gemini API**                | Conversational AI, coding assistance, image understanding |
| **Hugging Face Inference Providers** | Image generation                                          |
| **Qwen-Image**                       | Text-to-image generation                                  |
| **SQLite**                           | Persistent conversation storage                           |
| **python-dotenv**                    | Environment-variable/API-key management                   |

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
```

Replace `YOUR_USERNAME` and `YOUR_REPOSITORY` with your GitHub details.

---

### 2. Create a virtual environment

Windows:

```powershell
python -m venv venv
```

Activate it:

```powershell
venv\Scripts\Activate.ps1
```

---

### 3. Install dependencies

```powershell
pip install -U streamlit langgraph langgraph-checkpoint-sqlite langchain-google-genai python-dotenv huggingface_hub
```

---

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
HF_TOKEN=YOUR_HUGGINGFACE_TOKEN
```

Never commit this file to GitHub.

---

### 5. Run the application

```powershell
streamlit run app.py
```

Open the local Streamlit URL shown in the terminal, normally:

```text
http://localhost:8501
```

---

## 🔐 Environment Variables

The project requires:

### `GEMINI_API_KEY`

Used for:

* General Assistant
* Code Assistant
* Image understanding

Obtain the key from Google AI Studio.

### `HF_TOKEN`

Used for:

* Image generation through Hugging Face Inference Providers

Create a Hugging Face access token with the permissions required for Inference Providers.

---

## ⚠️ Security

Never hard-code API keys in Python files.

Do **not** commit:

```text
.env
```

to GitHub.

Recommended `.gitignore`:

```gitignore
venv/
.env
__pycache__/
*.pyc
chatbot.db
```

If an API key is accidentally exposed publicly, revoke it and create a new key immediately.

---

## 🎯 Supported Use Cases

### General Assistant

Example:

```text
Explain recursion in simple terms.
```

### Code Assistant

Example:

```text
Why does this Python program produce an IndexError?
```

### Code File Analysis

Example:

```text
Upload:
calculator.py

Prompt:
Find the bugs and provide corrected code.
```

### Image Analysis

Example:

```text
Upload:
database_diagram.png

Prompt:
Explain this database diagram.
```

### Image Generation

Example:

```text
A futuristic university campus surrounded by mountains
at sunset, cinematic digital art.
```

### Chat Search

Example:

```text
Search:
LangGraph
```

The application searches stored conversation titles and message contents.

---

## ✅ Feature Checklist

* [x] Gemini-powered chatbot
* [x] Streamlit interface
* [x] LangGraph conversation management
* [x] SQLite persistent history
* [x] Multiple chat threads
* [x] New chat creation
* [x] Previous chat loading
* [x] Streaming responses
* [x] General Assistant mode
* [x] Code Assistant mode
* [x] Chat search
* [x] Chat deletion
* [x] Code/text file upload
* [x] Code analysis
* [x] Generated code download
* [x] Image upload
* [x] Image understanding
* [x] Image generation
* [x] Generated image download
* [x] Environment-variable API keys
* [x] File-size validation
* [x] Error handling

---

## 🔒 File and Code Safety

Uploaded code is treated as text and sent to the AI for analysis.

The application does **not** execute arbitrary uploaded source code.

This allows users to safely ask the Code Assistant to:

* Review code
* Explain code
* Find bugs
* Refactor code
* Improve code
* Generate revised code

---

## 🧪 Example Demonstration

A complete demonstration can be performed using the following sequence:

### 1. General Assistant

Select:

```text
General Assistant
```

Ask:

```text
Explain normalization in DBMS.
```

### 2. Code Assistant

Switch to:

```text
Code Assistant
```

Ask:

```text
Explain the following Python code and identify possible problems.
```

### 3. Upload a Code File

Upload:

```text
example.py
```

Ask:

```text
Find errors and provide an improved version.
```

Download the revised code.

### 4. Upload an Image

Upload:

```text
diagram.png
```

Ask:

```text
Explain this diagram.
```

### 5. Generate an Image

Enter:

```text
A futuristic university campus at sunset,
surrounded by mountains, cinematic digital art.
```

Generate and download the image.

### 6. Search Conversations

Search:

```text
normalization
```

Open the matching conversation.

### 7. Delete Conversation

Delete an unwanted chat from the sidebar.

---

## 📚 Prompt Engineering Techniques Demonstrated

This project demonstrates multiple prompt-engineering techniques:

### Role Prompting

Different instructions are used for:

```text
General Assistant
Code Assistant
```

### Instruction Prompting

The model is given explicit instructions about:

* Response behavior
* Explanation depth
* Coding behavior
* Formatting

### Contextual Prompting

Uploaded code and images are added as context for the user's request.

### Task-Specific Prompting

Different tasks receive specialized instructions.

### Dynamic Prompt Composition

The final request depends on:

```text
Selected Mode
+
User Query
+
Conversation Context
+
Uploaded Content
```

### Image Prompt Engineering

Image descriptions are enhanced before being passed to the image-generation model.

---

## 📈 Possible Future Enhancements

Potential future improvements include:

* [ ] AI-generated chat titles
* [ ] Conversation summarization
* [ ] Rename conversations
* [ ] Regenerate response
* [ ] User feedback / ratings
* [ ] More programming languages
* [ ] PDF document analysis
* [ ] DOCX document support
* [ ] Multiple image-generation styles
* [ ] Image generation aspect-ratio selection
* [ ] Web search
* [ ] Retrieval-Augmented Generation (RAG)
* [ ] User authentication
* [ ] Cloud database
* [ ] Deployment to Streamlit Community Cloud

---

## 🚧 Current Limitations

* Gemini and Hugging Face APIs require valid API credentials.
* API quotas and rate limits depend on the provider and account.
* Hugging Face image generation depends on current provider/model availability and account credits.
* Uploaded source code is analyzed as text and is not executed.
* Conversation data is stored locally in SQLite.
* The application currently supports a limited list of file extensions.
* Image generation requires a separate service from the Gemini conversational model.

---

## 📊 Project Objectives

The primary objectives of this project are:

1. Develop a practical AI chatbot using a modern LLM API.
2. Demonstrate prompt engineering through task-specific response modes.
3. Provide programming assistance through code-aware prompts.
4. Support multimodal interaction through image input.
5. Provide text-to-image generation through an external inference API.
6. Improve conversation management using search and deletion.
7. Maintain persistent conversations using SQLite and LangGraph.
8. Provide a simple beginner-friendly user interface using Streamlit.

---

## 🎓 Academic Relevance

This project demonstrates the practical application of:

* Generative AI
* Large Language Models
* Prompt Engineering
* Multimodal AI
* Natural Language Processing
* AI-assisted Programming
* API Integration
* State Management
* Database Persistence
* Human-AI Interaction

The project particularly demonstrates how **prompt engineering can change the behavior of the same underlying language model according to the user's task**.

---

## 🌟 Why This Project?

The goal is not simply to create another chatbot.

The application combines several practical AI capabilities into one lightweight system:

```text
Conversation
    +
Prompt Engineering
    +
Code Assistance
    +
File Input
    +
Image Understanding
    +
Image Generation
    +
Chat Search
    +
Chat Management
    =
Multimodal AI Assistant
```

---

## 👨‍💻 Author

**Saurabh Bhuptani**

Marwadi University

> Add your GitHub profile link here.

```text
GitHub: https://github.com/YOUR_USERNAME
```

---

## 📄 License

This project is intended primarily for educational and academic purposes.

You may add a specific open-source license here, such as:

```text
MIT License
```

after deciding how you want others to use the project.

---

## ⭐ Acknowledgements

This project uses the following technologies and services:

* Google Gemini
* LangChain
* LangGraph
* Streamlit
* Hugging Face
* Qwen
* SQLite
* Python

Thank you to the open-source and AI developer communities that provide the frameworks, APIs, and tools used to build this project.

---

## 🚀 Quick Start

For experienced users:

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
python -m venv venv
venv\Scripts\activate
pip install -U streamlit langgraph langgraph-checkpoint-sqlite langchain-google-genai python-dotenv huggingface_hub
streamlit run app.py
```

Then configure:

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
HF_TOKEN=YOUR_HUGGINGFACE_TOKEN
```

and open:

```text
http://localhost:8501
```

---

## 🖼️ Suggested GitHub Screenshots

For the best-looking repository, add these files inside an `images/` folder:

```text
images/
├── main-interface.png
├── ai-modes.png
├── chat-search.png
├── chat-delete.png
├── code-file-analysis.png
├── image-analysis.png
└── image-generation.png
```

Then replace the placeholder images in this README with your actual screenshots.
