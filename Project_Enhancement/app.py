import base64
import re
import uuid
from io import BytesIO

import streamlit as st

from langchain_core.messages import HumanMessage

from backend import (
    chatbot,
    delete_thread,
    generate_image,
    get_all_threads_id,
    get_thread_messages,
    get_thread_title,
    search_threads,
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Multimodal AI Assistant",
    page_icon="🤖",
    layout="wide",
)


# ============================================================
# CONSTANTS
# ============================================================

MAX_CODE_FILE_SIZE_MB = 2
MAX_IMAGE_FILE_SIZE_MB = 5

SUPPORTED_CODE_EXTENSIONS = [
    "py",
    "js",
    "java",
    "c",
    "cpp",
    "cs",
    "html",
    "css",
    "sql",
    "json",
    "txt",
]

SUPPORTED_IMAGE_EXTENSIONS = [
    "png",
    "jpg",
    "jpeg",
    "webp",
]

AI_MODES = [
    "General Assistant",
    "Code Assistant",
    "Image Generator",
]


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def generate_unique_id() -> str:
    return str(uuid.uuid4())


def extract_code_blocks(
    text: str,
) -> str | None:

    if not text:
        return None

    pattern = (
        r"```(?:[a-zA-Z0-9_+#.-]+)?\s*\n"
        r"(.*?)"
        r"```"
    )

    matches = re.findall(
        pattern,
        text,
        re.DOTALL,
    )

    if not matches:
        return None

    return "\n\n".join(
        matches
    ).strip()


def load_thread_history(
    thread_id: str,
) -> list[dict]:

    messages = get_thread_messages(
        thread_id
    )

    history = []

    for message in messages:

        if message.type == "human":
            role = "user"

        elif message.type == "ai":
            role = "assistant"

        else:
            continue

        content = message.content

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

                    text_parts.append(
                        item
                    )

                else:

                    text_parts.append(
                        str(item)
                    )

            content = "".join(
                text_parts
            )

        else:

            content = str(
                content
            )

        history.append(
            {
                "role": role,
                "content": content,
            }
        )

    return history


def clear_generated_image():
    st.session_state.generated_image = None
    st.session_state.generated_image_prompt = ""


# ============================================================
# SESSION STATE
# ============================================================

if "thread_id" not in st.session_state:

    st.session_state.thread_id = (
        generate_unique_id()
    )


if "message_history" not in st.session_state:

    st.session_state.message_history = []


if "generated_image" not in st.session_state:

    st.session_state.generated_image = None


if "generated_image_prompt" not in st.session_state:

    st.session_state.generated_image_prompt = ""


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🤖 Multimodal AI Assistant")


    # --------------------------------------------------------
    # NEW CHAT
    # --------------------------------------------------------

    if st.button(
        "+ New Chat",
        use_container_width=True,
    ):

        st.session_state.thread_id = (
            generate_unique_id()
        )

        st.session_state.message_history = []

        clear_generated_image()

        st.rerun()


    st.divider()


    # --------------------------------------------------------
    # AI MODE
    # --------------------------------------------------------

    st.subheader("⚙️ AI Mode")

    ai_mode = st.selectbox(
        "Select Mode",
        AI_MODES,
        index=0,
        label_visibility="collapsed",
    )


    if ai_mode == "General Assistant":

        st.caption(
            "💬 General-purpose conversational AI."
        )

    elif ai_mode == "Code Assistant":

        st.caption(
            "💻 Debug, explain, improve, and generate code."
        )

    elif ai_mode == "Image Generator":

        st.caption(
            "🎨 Generate an image from a text description."
        )


    st.divider()


    # --------------------------------------------------------
    # SEARCH
    # --------------------------------------------------------

    st.subheader("🔍 Search Chats")

    search_query = st.text_input(
        "Search titles or contents...",
        key="chat_search_input",
    )


    if search_query.strip():

        search_results = search_threads(
            search_query
        )

        st.caption(
            f"Found {len(search_results)} match(es)"
        )


        if not search_results:

            st.info(
                "No matching conversations."
            )


        for result in search_results:

            tid = result[
                "thread_id"
            ]

            title = result[
                "title"
            ]

            snippet = result[
                "snippet"
            ]

            button_label = (
                f"💬 {title}\n"
                f"{snippet}"
            )


            if st.button(
                button_label,
                key=f"search_{tid}",
                use_container_width=True,
            ):

                st.session_state.thread_id = tid

                st.session_state.message_history = (
                    load_thread_history(
                        tid
                    )
                )

                clear_generated_image()

                st.rerun()


    else:

        # ----------------------------------------------------
        # PREVIOUS CHATS
        # ----------------------------------------------------

        st.subheader("📚 Previous Chats")

        threads = get_all_threads_id()


        if not threads:

            st.caption(
                "No previous chats."
            )

        else:

            for thread_id in threads:

                title = get_thread_title(
                    thread_id
                )

                col1, col2 = st.columns(
                    [0.80, 0.20]
                )


                with col1:

                    if st.button(
                        title,
                        key=f"thread_{thread_id}",
                        use_container_width=True,
                    ):

                        st.session_state.thread_id = (
                            thread_id
                        )

                        st.session_state.message_history = (
                            load_thread_history(
                                thread_id
                            )
                        )

                        clear_generated_image()

                        st.rerun()


                with col2:

                    with st.popover("🗑️"):

                        st.write(
                            "Delete this chat?"
                        )

                        if st.button(
                            "Confirm",
                            key=f"del_{thread_id}",
                            use_container_width=True,
                        ):

                            deleted = (
                                delete_thread(
                                    thread_id
                                )
                            )


                            if deleted:

                                if (
                                    st.session_state.thread_id
                                    == thread_id
                                ):

                                    st.session_state.thread_id = (
                                        generate_unique_id()
                                    )

                                    st.session_state.message_history = []

                                    clear_generated_image()


                                st.rerun()

                            else:

                                st.error(
                                    "Could not delete chat."
                                )


# ============================================================
# MAIN TITLE
# ============================================================

st.title(
    "💬 Multimodal AI Assistant"
)


if ai_mode == "General Assistant":

    st.caption(
        "General Assistant — ask questions, learn concepts, and have conversations."
    )

elif ai_mode == "Code Assistant":

    st.caption(
        "Code Assistant — analyze, debug, explain, improve, and generate code."
    )

elif ai_mode == "Image Generator":

    st.caption(
        "Image Generator — describe the image you want to create."
    )


# ============================================================
# GENERATED IMAGE DISPLAY
# ============================================================

if (
    st.session_state.generated_image
    is not None
):

    st.subheader(
        "🎨 Generated Image"
    )


    st.image(
        st.session_state.generated_image,
        caption=(
            st.session_state
            .generated_image_prompt
        ),
        use_container_width=True,
    )


    try:

        image_buffer = BytesIO()

        st.session_state.generated_image.save(
            image_buffer,
            format="PNG",
        )

        image_bytes = (
            image_buffer.getvalue()
        )


        st.download_button(
            "📥 Download Image",
            data=image_bytes,
            file_name="generated_image.png",
            mime="image/png",
            key="download_generated_image",
        )

    except Exception as error:

        st.error(
            f"Could not prepare image for download: {error}"
        )


    st.divider()


# ============================================================
# ATTACHMENTS
# ============================================================

with st.expander(
    "📎 Attach Code/Text File or Image",
    expanded=False,
):

    col_code, col_img = st.columns(
        2
    )


    # --------------------------------------------------------
    # CODE FILE
    # --------------------------------------------------------

    with col_code:

        uploaded_code_file = st.file_uploader(
            "Upload Code/Text File",
            type=SUPPORTED_CODE_EXTENSIONS,
            key="code_uploader",
        )


        if uploaded_code_file:

            size_kb = (
                uploaded_code_file.size
                / 1024
            )

            st.info(
                f"📄 **{uploaded_code_file.name}** "
                f"({size_kb:.1f} KB)"
            )


            if (
                uploaded_code_file.size
                > MAX_CODE_FILE_SIZE_MB
                * 1024
                * 1024
            ):

                st.error(
                    f"Code file exceeds the "
                    f"{MAX_CODE_FILE_SIZE_MB} MB limit."
                )


    # --------------------------------------------------------
    # IMAGE FILE
    # --------------------------------------------------------

    with col_img:

        uploaded_image_file = st.file_uploader(
            "Upload Image",
            type=SUPPORTED_IMAGE_EXTENSIONS,
            key="image_uploader",
        )


        if uploaded_image_file:

            size_mb = (
                uploaded_image_file.size
                / (1024 * 1024)
            )


            st.image(
                uploaded_image_file,
                caption=uploaded_image_file.name,
                width=250,
            )


            st.info(
                f"Size: {size_mb:.2f} MB"
            )


            if (
                uploaded_image_file.size
                > MAX_IMAGE_FILE_SIZE_MB
                * 1024
                * 1024
            ):

                st.error(
                    f"Image exceeds the "
                    f"{MAX_IMAGE_FILE_SIZE_MB} MB limit."
                )


# ============================================================
# CURRENT CHAT HISTORY
# ============================================================

for message in st.session_state.message_history:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


        if message["role"] == "assistant":

            code_snippet = (
                extract_code_blocks(
                    message["content"]
                )
            )


            if code_snippet:

                st.download_button(
                    "📥 Download Code",
                    data=code_snippet,
                    file_name="generated_code.txt",
                    mime="text/plain",
                    key=(
                        f"history_download_"
                        f"{hash(message['content'])}"
                    ),
                )


# ============================================================
# CHAT INPUT
# ============================================================

user_input = st.chat_input(
    (
        "Describe the image..."
        if ai_mode == "Image Generator"
        else "Message Gemini..."
    )
)


# ============================================================
# PROCESS USER INPUT
# ============================================================

if user_input:

    user_input = user_input.strip()


    if not user_input:

        st.warning(
            "Please enter a message."
        )

        st.stop()


    # ========================================================
    # IMAGE GENERATOR MODE
    # ========================================================

    if ai_mode == "Image Generator":

        # ----------------------------------------------------
        # User message
        # ----------------------------------------------------

        st.session_state.message_history.append(
            {
                "role": "user",
                "content": user_input,
            }
        )


        with st.chat_message(
            "user"
        ):

            st.markdown(
                user_input
            )


        # ----------------------------------------------------
        # Generate image
        # ----------------------------------------------------

        with st.chat_message(
            "assistant"
        ):

            try:

                with st.spinner(
                    "Creating your image..."
                ):

                    generated_image = (
                        generate_image(
                            user_input
                        )
                    )


                st.session_state.generated_image = (
                    generated_image
                )

                st.session_state.generated_image_prompt = (
                    user_input
                )


                st.image(
                    generated_image,
                    caption=user_input,
                    use_container_width=True,
                )

                image_buffer = BytesIO()

                generated_image.save(
                    image_buffer,
                    format="PNG",
                )
                
                st.download_button(
                     "📥 Download Image",
                    data=image_buffer.getvalue(),
                    file_name="generated_image.png",
                    mime="image/png",
                    key=(
                        "generated_image_download_"
                        + str(
                            len(
                                st.session_state.message_history
                            )
                        )
                    ),
                )

            except Exception as error:

                st.error(
                    f"Image generation failed:\n\n{error}"
                )


        # ----------------------------------------------------
        # Add text marker to current Streamlit history.
        #
        # The generated image itself is kept in session state.
        # It is not inserted into LangGraph as an AI message.
        # ----------------------------------------------------

        st.session_state.message_history.append(
            {
                "role": "assistant",
                "content": (
                    "🎨 **Image generated successfully.**\n\n"
                    f"Prompt: `{user_input}`"
                ),
            }
        )


    # ========================================================
    # GEMINI MODES
    # ========================================================

    else:

        prompt_text = user_input

        # ----------------------------------------------------
        # CODE FILE
        # ----------------------------------------------------

        if uploaded_code_file:

            if (
                uploaded_code_file.size
                > MAX_CODE_FILE_SIZE_MB
                * 1024
                * 1024
            ):

                st.error(
                    f"Code file exceeds "
                    f"{MAX_CODE_FILE_SIZE_MB} MB."
                )

                st.stop()


            if ai_mode != "Code Assistant":

                st.warning(
                    "A code file is attached, but "
                    "Code Assistant mode is not selected."
                )

            else:

                try:

                    file_bytes = (
                        uploaded_code_file.read()
                    )


                    try:

                        code_text = (
                            file_bytes.decode(
                                "utf-8"
                            )
                        )

                    except UnicodeDecodeError:

                        code_text = (
                            file_bytes.decode(
                                "latin-1"
                            )
                        )


                    prompt_text += (
                        "\n\n"
                        f"[Attached File: "
                        f"{uploaded_code_file.name}]"
                        "\n```"
                        "\n"
                        f"{code_text}"
                        "\n```"
                    )


                except Exception as error:

                    st.error(
                        f"Error reading attached file: {error}"
                    )

                    st.stop()


        # ----------------------------------------------------
        # IMAGE INPUT
        # ----------------------------------------------------

        if uploaded_image_file:

            if (
                uploaded_image_file.size
                > MAX_IMAGE_FILE_SIZE_MB
                * 1024
                * 1024
            ):

                st.error(
                    f"Image exceeds "
                    f"{MAX_IMAGE_FILE_SIZE_MB} MB."
                )

                st.stop()


            try:

                img_bytes = (
                    uploaded_image_file.read()
                )

                mime_type = (
                    uploaded_image_file.type
                    or "image/png"
                )

                base64_img = (
                    base64.b64encode(
                        img_bytes
                    ).decode(
                        "utf-8"
                    )
                )


                human_message_content = [

                    {
                        "type": "text",
                        "text": prompt_text,
                    },

                    {
                        "type": "image_url",
                        "image_url": {
                            "url": (
                                f"data:{mime_type};"
                                f"base64,{base64_img}"
                            )
                        },
                    },

                ]


            except Exception as error:

                st.error(
                    f"Error processing image: {error}"
                )

                st.stop()


        else:

            human_message_content = (
                prompt_text
            )


        # ----------------------------------------------------
        # Save user message
        # ----------------------------------------------------

        st.session_state.message_history.append(
            {
                "role": "user",
                "content": user_input,
            }
        )


        with st.chat_message(
            "user"
        ):

            st.markdown(
                user_input
            )


            if uploaded_code_file:

                st.caption(
                    f"📎 {uploaded_code_file.name}"
                )


            if uploaded_image_file:

                st.caption(
                    f"🖼️ {uploaded_image_file.name}"
                )


        # ----------------------------------------------------
        # Gemini configuration
        # ----------------------------------------------------

        config = {
            "configurable": {
                "thread_id": (
                    st.session_state.thread_id
                )
            }
        }


        # ----------------------------------------------------
        # Gemini response
        # ----------------------------------------------------

        with st.chat_message(
            "assistant"
        ):

            response_placeholder = st.empty()

            full_response = ""


            try:

                for (
                    message_chunk,
                    metadata,
                ) in chatbot.stream(

                    {
                        "messages": [
                            HumanMessage(
                                content=human_message_content
                            )
                        ],
                        "mode": ai_mode,
                    },

                    config=config,

                    stream_mode="messages",
                ):

                    content = (
                        message_chunk.content
                    )


                    if isinstance(
                        content,
                        list,
                    ):

                        text = ""


                        for item in content:

                            if isinstance(
                                item,
                                dict,
                            ):

                                text += str(
                                    item.get(
                                        "text",
                                        "",
                                    )
                                )

                            else:

                                text += str(
                                    item
                                )


                        content = text


                    else:

                        content = str(
                            content
                        )


                    full_response += content


                    response_placeholder.markdown(
                        full_response
                        + "▌"
                    )


                response_placeholder.markdown(
                    full_response
                )


                st.session_state.message_history.append(
                    {
                        "role": "assistant",
                        "content": full_response,
                    }
                )


                # ------------------------------------------------
                # Download code from response
                # ------------------------------------------------

                extracted_code = (
                    extract_code_blocks(
                        full_response
                    )
                )


                if extracted_code:

                    if uploaded_code_file:

                        original_name = (
                            uploaded_code_file.name
                        )


                        if "." in original_name:

                            stem, extension = (
                                original_name.rsplit(
                                    ".",
                                    1,
                                )
                            )

                            output_name = (
                                f"revised_{stem}."
                                f"{extension}"
                            )

                        else:

                            output_name = (
                                f"revised_"
                                f"{original_name}"
                            )

                    else:

                        output_name = (
                            "generated_code.txt"
                        )


                    st.download_button(
                        "📥 Download Code",
                        data=extracted_code,
                        file_name=output_name,
                        mime="text/plain",
                        key=(
                            "response_code_"
                            + str(
                                len(
                                    st.session_state
                                    .message_history
                                )
                            )
                        ),
                    )


            except Exception as error:

                response_placeholder.error(
                    f"Gemini API error: {error}"
                )