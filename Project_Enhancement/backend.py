import os
import sqlite3
from typing import Annotated, TypedDict

from dotenv import load_dotenv
from huggingface_hub import InferenceClient

from langchain_core.messages import BaseMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
HF_TOKEN = os.getenv("HF_TOKEN")


if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is missing. "
        "Add GEMINI_API_KEY to your .env file."
    )


# ============================================================
# SYSTEM PROMPTS
# ============================================================

GENERAL_SYSTEM_PROMPT = """
You are a helpful, accurate, and clear AI assistant.

Rules:
- Answer the user's question directly.
- Adapt the explanation depth to the user's needs.
- Use Markdown when useful.
- Prefer clear and organized explanations.
- Do not unnecessarily generate code unless requested.
- Do not invent facts.
""".strip()


CODE_SYSTEM_PROMPT = """
You are an experienced programming tutor and code assistant.

Rules:
- Identify the programming language when possible.
- Explain the approach before complex code.
- Analyze syntax, logical, runtime, and design problems.
- Provide corrected or improved code when appropriate.
- Explain important changes.
- Preserve the user's original intent.
- Use Markdown code blocks for code.
- Never claim that code was executed unless it actually was.
- Never execute uploaded code.
""".strip()


# ============================================================
# GEMINI MODEL
# ============================================================

llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=GEMINI_API_KEY,
)


# ============================================================
# HUGGING FACE IMAGE GENERATION
# ============================================================

IMAGE_MODEL = "Qwen/Qwen-Image"

hf_client = None

if HF_TOKEN:
    hf_client = InferenceClient(
        provider="auto",
        api_key=HF_TOKEN,
    )


def generate_image(prompt: str):
    """
    Generate an image using Hugging Face Inference Providers.

    Returns:
        PIL Image on success.

    Raises:
        RuntimeError if HF is unavailable/configuration is missing.
        ValueError if the prompt is empty.
    """

    if not hf_client:
        raise RuntimeError(
            "HF_TOKEN is not configured. "
            "Add HF_TOKEN to your .env file."
        )

    prompt = prompt.strip()

    if not prompt:
        raise ValueError(
            "Image prompt cannot be empty."
        )

    # Prompt-engineering layer for image generation.
    enhanced_prompt = (
        "Create a high-quality image based on the following "
        "description. Follow the requested subject, composition, "
        "lighting, environment, mood, and artistic style as closely "
        "as possible.\n\n"
        f"User description:\n{prompt}"
    )

    try:
        image = hf_client.text_to_image(
            prompt=enhanced_prompt,
            model=IMAGE_MODEL,
        )

        return image

    except Exception as error:
        raise RuntimeError(
            f"Hugging Face image generation failed: {error}"
        ) from error


# ============================================================
# LANGGRAPH STATE
# ============================================================

class State(TypedDict):
    messages: Annotated[
        list[BaseMessage],
        add_messages
    ]
    mode: str


# ============================================================
# CHAT NODE
# ============================================================

def chat_node(state: State):
    """
    Handles Gemini-based modes only.

    Image Generator mode is handled directly by Streamlit
    because it uses Hugging Face instead of Gemini.
    """

    mode = state.get(
        "mode",
        "General Assistant"
    )

    if mode == "Code Assistant":
        system_prompt = CODE_SYSTEM_PROMPT
    else:
        system_prompt = GENERAL_SYSTEM_PROMPT

    messages_to_send = [
        SystemMessage(
            content=system_prompt
        )
    ] + state["messages"]

    response = llm.invoke(
        messages_to_send
    )

    return {
        "messages": [response]
    }


# ============================================================
# SQLITE
# ============================================================

conn = sqlite3.connect(
    "chatbot.db",
    check_same_thread=False,
)

checkpointer = SqliteSaver(
    conn
)


# ============================================================
# LANGGRAPH
# ============================================================

graph = StateGraph(State)

graph.add_node(
    "chat_node",
    chat_node,
)

graph.add_edge(
    START,
    "chat_node",
)

graph.add_edge(
    "chat_node",
    END,
)

chatbot = graph.compile(
    checkpointer=checkpointer
)


# ============================================================
# MESSAGE CONTENT HELPER
# ============================================================

def message_to_text(message) -> str:
    """
    Convert normal or structured LangChain content
    into plain text.
    """

    content = getattr(
        message,
        "content",
        "",
    )

    if isinstance(content, list):

        text_parts = []

        for item in content:

            if isinstance(item, dict):

                if item.get("type") == "text":
                    text_parts.append(
                        str(
                            item.get(
                                "text",
                                "",
                            )
                        )
                    )

                elif "text" in item:
                    text_parts.append(
                        str(
                            item["text"]
                        )
                    )

            elif isinstance(item, str):

                text_parts.append(item)

            else:

                text_parts.append(
                    str(item)
                )

        return "".join(
            text_parts
        ).strip()

    return str(
        content
    ).strip()


# ============================================================
# GET ALL THREAD IDS
# ============================================================

def get_all_threads_id() -> list[str]:

    threads: dict[str, str] = {}

    try:

        for checkpoint in checkpointer.list(None):

            thread_id = (
                checkpoint.config
                .get(
                    "configurable",
                    {}
                )
                .get(
                    "thread_id"
                )
            )

            if not thread_id:
                continue

            timestamp = (
                checkpoint.checkpoint
                .get(
                    "ts",
                    "",
                )
            )

            threads[thread_id] = timestamp

    except Exception as error:

        print(
            f"Error retrieving threads: {error}"
        )

    sorted_threads = sorted(
        threads.items(),
        key=lambda item: item[1],
        reverse=True,
    )

    return [
        thread_id
        for thread_id, _ in sorted_threads
    ]


# ============================================================
# GET THREAD MESSAGES
# ============================================================

def get_thread_messages(
    thread_id: str,
):

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    try:

        state = chatbot.get_state(
            config
        )

    except Exception as error:

        print(
            f"Error loading thread "
            f"{thread_id}: {error}"
        )

        return []

    if not state.values:
        return []

    return state.values.get(
        "messages",
        []
    )


# ============================================================
# GET THREAD TITLE
# ============================================================

def get_thread_title(
    thread_id: str,
) -> str:

    messages = get_thread_messages(
        thread_id
    )

    for message in messages:

        if message.type != "human":
            continue

        title = message_to_text(
            message
        )

        if title:

            if len(title) > 50:
                return title[:47] + "..."

            return title

    return "New Chat"


# ============================================================
# SEARCH THREADS
# ============================================================

def search_threads(
    query: str,
) -> list[dict]:

    query = query.strip()

    if not query:
        return []

    query_lower = query.lower()

    results = []

    for thread_id in get_all_threads_id():

        title = get_thread_title(
            thread_id
        )

        messages = get_thread_messages(
            thread_id
        )

        title_match = (
            query_lower in title.lower()
        )

        matched = title_match
        snippet = title

        if not title_match:

            for message in messages:

                content = message_to_text(
                    message
                )

                content_lower = (
                    content.lower()
                )

                index = (
                    content_lower.find(
                        query_lower
                    )
                )

                if index != -1:

                    matched = True

                    start = max(
                        0,
                        index - 30,
                    )

                    end = min(
                        len(content),
                        index + len(query) + 60,
                    )

                    snippet = (
                        "..."
                        + content[
                            start:end
                        ].replace(
                            "\n",
                            " "
                        )
                        + "..."
                    )

                    break

        if matched:

            results.append(
                {
                    "thread_id": thread_id,
                    "title": title,
                    "snippet": snippet,
                }
            )

    return results


# ============================================================
# DELETE THREAD
# ============================================================

def delete_thread(
    thread_id: str,
) -> bool:

    if not thread_id:
        return False

    try:

        checkpointer.delete_thread(
            thread_id
        )

        return True

    except Exception as error:

        print(
            f"Error deleting thread "
            f"{thread_id}: {error}"
        )

        return False