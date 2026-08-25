import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

# =========================================================
# LOAD ENVIRONMENT
# =========================================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
MODEL_NAME = "gemini-2.5-flash"


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="CareerPilot AI",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# GEMINI CLIENT
# =========================================================

@st.cache_resource
def get_gemini_client(api_key):
    if not api_key:
        return None

    try:
        return genai.Client(api_key=api_key)
    except Exception:
        return None


client = get_gemini_client(API_KEY)


# =========================================================
# SESSION STATE
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = ""


# =========================================================
# PROMPTS
# =========================================================

from prompts import get_task_prompt


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
<style>

    /* =====================================================
       GLOBAL
       ===================================================== */

    .stApp {
        background: #f5f7fb;
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    .main .block-container {
        max-width: 1350px;
        padding-top: 2rem;
        padding-bottom: 6rem;
    }


    /* =====================================================
       SIDEBAR
       ===================================================== */

    section[data-testid="stSidebar"] {
        background: #101827;
    }

    section[data-testid="stSidebar"] > div {
        padding: 1.5rem 1rem;
    }

    .sidebar-brand {
        padding: 10px 5px 20px 5px;
    }

    .sidebar-logo {
        font-size: 2rem;
        margin-bottom: 8px;
    }

    .sidebar-title {
        color: #ffffff;
        font-size: 1.45rem;
        font-weight: 800;
        margin-bottom: 8px;
    }

    .sidebar-description {
        color: #aeb9ca;
        font-size: 0.9rem;
        line-height: 1.6;
    }

    .sidebar-heading {
        color: #ffffff;
        font-size: 1rem;
        font-weight: 800;
        margin: 1.5rem 0 0.7rem 0;
    }


    /* =====================================================
       SIDEBAR BUTTONS
       ===================================================== */

    section[data-testid="stSidebar"] .stButton > button {
        width: 100%;
        min-height: 45px;
        border-radius: 10px;
        border: none;
        background: #ffffff;
        color: #263247;
        font-weight: 600;
        margin: 4px 0;
        transition: all 0.2s ease;
    }

    section[data-testid="stSidebar"] .stButton > button:hover {
        background: #e9eef7;
        color: #16233d;
        transform: translateY(-1px);
    }


    /* =====================================================
       STATUS
       ===================================================== */

    .online-box {
        margin-top: 18px;
        padding: 11px 14px;
        border-radius: 10px;
        background: #103b35;
        color: #d7fff5;
        font-size: 0.85rem;
        font-weight: 700;
        text-align: center;
    }

    .offline-box {
        margin-top: 18px;
        padding: 11px 14px;
        border-radius: 10px;
        background: #4a2024;
        color: #ffe4e6;
        font-size: 0.85rem;
        font-weight: 700;
        text-align: center;
    }


    /* =====================================================
       HERO
       ===================================================== */

    .hero {
        background: linear-gradient(
            135deg,
            #17223d 0%,
            #29377f 100%
        );

        border-radius: 22px;
        padding: 38px 42px;
        color: white;
        margin-bottom: 28px;
        box-shadow: 0 15px 40px rgba(28, 42, 85, 0.15);
    }

    .hero-badge {
        display: inline-block;
        padding: 7px 13px;
        border-radius: 999px;
        background: rgba(255,255,255,0.12);
        border: 1px solid rgba(255,255,255,0.18);
        color: #ffffff;
        font-size: 0.82rem;
        font-weight: 700;
        margin-bottom: 16px;
    }

    .hero-title {
        font-size: 2.6rem;
        font-weight: 850;
        line-height: 1.15;
        margin-bottom: 12px;
    }

    .hero-text {
        max-width: 850px;
        color: #e5eaf5;
        font-size: 1rem;
        line-height: 1.7;
    }

    .hero-status {
        display: inline-block;
        margin-top: 20px;
        padding: 8px 14px;
        border-radius: 999px;
        background: rgba(20,184,166,0.18);
        color: #d8fff6;
        font-size: 0.85rem;
        font-weight: 700;
    }


    /* =====================================================
       SECTION HEADINGS
       ===================================================== */

    .section-title {
        color: #16213a;
        font-size: 1.75rem;
        font-weight: 850;
        margin-top: 22px;
        margin-bottom: 5px;
    }

    .section-description {
        color: #66748a;
        font-size: 0.95rem;
        line-height: 1.6;
        margin-bottom: 18px;
    }


    /* =====================================================
       FEATURE CARDS
       ===================================================== */

    .feature-card {
        background: #ffffff;
        border: 1px solid #e2e7ef;
        border-radius: 17px;
        padding: 23px;
        min-height: 205px;
        margin-bottom: 8px;
        box-shadow: 0 6px 22px rgba(28, 40, 70, 0.05);
        transition: all 0.2s ease;
        box-sizing: border-box;
    }

    .feature-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 30px rgba(28, 40, 70, 0.09);
        border-color: #d4dced;
    }

    .feature-icon {
        font-size: 2rem;
        margin-bottom: 14px;
    }

    .feature-title {
        color: #17233d;
        font-size: 1.08rem;
        font-weight: 800;
        margin-bottom: 9px;
    }

    .feature-description {
        color: #66748a;
        font-size: 0.9rem;
        line-height: 1.6;
    }


    /* =====================================================
       QUICK ACTION BUTTONS
       ===================================================== */

    .quick-label {
        color: #17233d;
        font-size: 0.85rem;
        font-weight: 700;
        margin-bottom: 6px;
    }

    .stButton > button {
        border-radius: 10px;
        min-height: 42px;
    }


    /* =====================================================
       CHAT
       ===================================================== */

    [data-testid="stChatMessage"] {
        border-radius: 15px;
    }

    [data-testid="stChatInput"] {
        border-radius: 14px;
    }


    /* =====================================================
       FOOTER
       ===================================================== */

    .footer {
        text-align: center;
        color: #8b96a8;
        font-size: 0.82rem;
        padding: 30px 0 10px 0;
    }


    /* =====================================================
       MOBILE
       ===================================================== */

    @media (max-width: 900px) {

        .main .block-container {
            padding: 1rem 1rem 5rem 1rem;
        }

        .hero {
            padding: 28px 24px;
        }

        .hero-title {
            font-size: 2rem;
        }

        .feature-card {
            min-height: auto;
        }
    }

</style>
""",
    unsafe_allow_html=True,
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        """
        <div class="sidebar-brand">
            <div class="sidebar-logo">💼</div>
            <div class="sidebar-title">CareerPilot AI</div>
            <div class="sidebar-description">
                Your intelligent assistant for jobs,
                resumes, interviews and career planning.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="sidebar-heading">
            🚀 Career Tools
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button(
        "🎯  Job Recommendations",
        use_container_width=True,
        key="sidebar_jobs",
    ):
        st.session_state.pending_prompt = (
            "What jobs can I apply for as a fresher? "
            "Please suggest realistic entry-level roles based on "
            "education, skills and experience."
        )

    if st.button(
        "📄  Resume Guidance",
        use_container_width=True,
        key="sidebar_resume",
    ):
        st.session_state.pending_prompt = (
            "How can I improve my resume? "
            "Give me practical ATS-friendly recommendations."
        )

    if st.button(
        "🎤  Interview Preparation",
        use_container_width=True,
        key="sidebar_interview",
    ):
        st.session_state.pending_prompt = (
            "Give me realistic interview questions and natural sample "
            "answers for an entry-level job."
        )

    if st.button(
        "🧠  Skill Gap Analysis",
        use_container_width=True,
        key="sidebar_skills",
    ):
        st.session_state.pending_prompt = (
            "Analyze the skills I should learn for my target career "
            "and create a practical skill-gap plan."
        )

    if st.button(
        "🗺️  Career Roadmap",
        use_container_width=True,
        key="sidebar_roadmap",
    ):
        st.session_state.pending_prompt = (
            "Create a practical step-by-step career roadmap "
            "for getting an entry-level job."
        )

    st.markdown("---")

    if st.button(
        "🗑️  Clear Chat",
        use_container_width=True,
        key="clear_chat",
    ):
        st.session_state.messages = []
        st.session_state.pending_prompt = ""
        st.rerun()

    if client:
        st.markdown(
            """
            <div class="online-box">
                🟢 Gemini AI Connected
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div class="offline-box">
                🔴 Gemini API Not Connected
            </div>
            """,
            unsafe_allow_html=True,
        )


# =========================================================
# MAIN HERO
# =========================================================

status = (
    "🟢 AI Assistant Online"
    if client
    else "🔴 Gemini API Key Required"
)

st.markdown(
    f"""
    <div class="hero">

        <div class="hero-badge">
            ✨ AI-Powered Career Guidance
        </div>

        <div class="hero-title">
            💼 CareerPilot AI
        </div>

        <div class="hero-text">
            Your intelligent job-search and career assistant.
            Find better roles, improve your resume,
            prepare for interviews and build your career.
        </div>

        <div class="hero-status">
            {status}
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# WELCOME
# =========================================================

st.markdown(
    """
    <div class="section-title">
        👋 Welcome to CareerPilot AI
    </div>

    <div class="section-description">
        Finding the right job can be confusing.
        CareerPilot AI helps you identify suitable roles,
        improve your resume, prepare for interviews,
        identify skill gaps and build a practical career plan.
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# FEATURES
# =========================================================

st.markdown(
    """
    <div class="section-title">
        🚀 What can I help with?
    </div>

    <div class="section-description">
        Choose a career service or ask the AI directly.
    </div>
    """,
    unsafe_allow_html=True,
)


features = [
    (
        "🎯",
        "Find Suitable Jobs",
        "Discover realistic job roles based on your education, skills and experience.",
        "What jobs can I apply for as a fresher?",
    ),
    (
        "📄",
        "Improve Your Resume",
        "Get practical ATS-friendly recommendations to make your resume stronger.",
        "How can I improve my resume?",
    ),
    (
        "🎤",
        "Prepare for Interviews",
        "Practice HR, technical and role-specific interview questions.",
        "Give me interview questions and sample answers.",
    ),
    (
        "🧠",
        "Skill Gap Analysis",
        "Identify the skills you need to learn for your target career.",
        "What skills should I learn for my target career?",
    ),
    (
        "🗺️",
        "Career Roadmap",
        "Build a practical step-by-step plan toward your target job.",
        "Create a practical career roadmap for me.",
    ),
    (
        "💡",
        "Career Questions",
        "Ask questions about jobs, skills, interviews, resumes and career growth.",
        "Give me useful career advice.",
    ),
]


# IMPORTANT:
# Use st.html() for the cards.
# This prevents Streamlit from displaying the HTML
# as a code block.

for row_start in range(0, len(features), 3):

    row_features = features[row_start:row_start + 3]

    columns = st.columns(3, gap="medium")

    for column, feature in zip(columns, row_features):

        icon, title, description, prompt_text = feature

        with column:

            st.html(
                f"""
                <div class="feature-card">
                    <div class="feature-icon">{icon}</div>

                    <div class="feature-title">
                        {title}
                    </div>

                    <div class="feature-description">
                        {description}
                    </div>
                </div>
                """
            )

            if st.button(
                f"Ask about {title.lower()}",
                use_container_width=True,
                key=f"feature_{row_start}_{title}",
            ):
                st.session_state.pending_prompt = prompt_text


# =========================================================
# TRY ASKING
# =========================================================

st.markdown(
    """
    <div class="section-title">
        💡 Try asking
    </div>

    <div class="section-description">
        Start with one of these questions or type your own below.
    </div>
    """,
    unsafe_allow_html=True,
)


quick_questions = [
    "What jobs can I apply for as a fresher?",
    "How can I improve my resume?",
    "Give me interview questions.",
    "What skills should I learn?",
]


quick_columns = st.columns(4, gap="small")

for i, question in enumerate(quick_questions):

    with quick_columns[i]:

        if st.button(
            question,
            use_container_width=True,
            key=f"quick_question_{i}",
        ):
            st.session_state.pending_prompt = question


# =========================================================
# CHAT HISTORY
# =========================================================

if st.session_state.messages:

    st.markdown(
        """
        <div class="section-title">
            💬 Career Assistant
        </div>
        """,
        unsafe_allow_html=True,
    )

    for message in st.session_state.messages:

        role = message["role"]
        content = message["content"]

        if role == "user":

            with st.chat_message("user", avatar="👤"):
                st.markdown(content)

        else:

            with st.chat_message("assistant", avatar="💼"):
                st.markdown(content)


# =========================================================
# CHAT INPUT
# =========================================================

user_input = st.chat_input(
    "Ask about jobs, resumes, interviews, skills or careers..."
)


# =========================================================
# DETERMINE CURRENT PROMPT
# =========================================================

prompt = user_input

if not prompt and st.session_state.pending_prompt:
    prompt = st.session_state.pending_prompt
    st.session_state.pending_prompt = ""


# =========================================================
# GENERATE GEMINI RESPONSE
# =========================================================

if prompt:

    # -----------------------------------------------------
    # API KEY CHECK
    # -----------------------------------------------------

    if not API_KEY or client is None:

        st.error(
            "Gemini API key is not configured. "
            "Make sure GEMINI_API_KEY is present in your .env file "
            "and restart Streamlit."
        )

    else:

        # -------------------------------------------------
        # SAVE USER MESSAGE
        # -------------------------------------------------

        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        # -------------------------------------------------
        # BUILD GEMINI CONVERSATION
        # -------------------------------------------------

        conversation = []

        for message in st.session_state.messages:

            role = (
                "user"
                if message["role"] == "user"
                else "model"
            )

            conversation.append(
                types.Content(
                    role=role,
                    parts=[
                        types.Part.from_text(
                            text=message["content"]
                        )
                    ],
                )
            )

        # -------------------------------------------------
        # CALL GEMINI
        # -------------------------------------------------

        try:

            with st.spinner("CareerPilot AI is thinking..."):

                response = client.models.generate_content(
                    model=MODEL_NAME,
                    contents=conversation,
                    config=types.GenerateContentConfig(
                        system_instruction=get_task_prompt(prompt),
                        temperature=0.4,
                        max_output_tokens=1800,
                    ),
                )

            answer = response.text

            if not answer:
                answer = (
                    "I couldn't generate a response right now. "
                    "Please try again."
                )

        except Exception as error:

            error_text = str(error)

            if "401" in error_text or "403" in error_text:

                answer = (
                    "⚠️ **Gemini API authentication failed.**\n\n"
                    "Please check that your `GEMINI_API_KEY` "
                    "is correct and active."
                )

            elif "404" in error_text or "NOT_FOUND" in error_text:

                answer = (
                    "⚠️ **Gemini model not found.**\n\n"
                    f"The application is currently using `{MODEL_NAME}`."
                )

            elif "429" in error_text:

                answer = (
                    "⚠️ **Gemini rate limit reached.**\n\n"
                    "Please wait a moment and try again."
                )

            else:

                answer = (
                    "⚠️ **Gemini request failed.**\n\n"
                    f"`{error_text}`"
                )

        # -------------------------------------------------
        # SAVE AI RESPONSE
        # -------------------------------------------------

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer,
            }
        )

        # -------------------------------------------------
        # REFRESH PAGE
        # -------------------------------------------------

        st.rerun()


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        💼 CareerPilot AI &nbsp;•&nbsp; Powered by Google Gemini
    </div>
    """,
    unsafe_allow_html=True,
)