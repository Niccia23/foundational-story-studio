import streamlit as st
import google.generativeai as genai
import io
import pdfplumber
import base64
from PIL import Image

# Page config
st.set_page_config(
    page_title="Foundational Story Elements Studio",
    page_icon="📘",
    layout="wide",
)

# 🔹 Function to encode image as base64
def get_base64(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Encode your background image
encoded_bg = get_base64("iceberg.png")

# Insert background CSS
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{encoded_bg}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    .stApp::before {{
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(255,255,255,0.92);
        backdrop-filter: blur(3px);
        z-index: -1;
    }}
    .main-content-wrapper {{
        padding: 20px 50px;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# 🔹 Google Fonts & custom styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Open+Sans&display=swap');

    html, body, [class*="css"] {
        font-family: 'Open Sans', sans-serif;
        color: #000 !important;
    }

    h1 {
        font-family: 'Playfair Display', serif;
        font-size: 2.4rem;
        color: #4a2e1f !important;
        margin-bottom: 0.3rem;
    }

    h2, h3 {
        font-family: 'Playfair Display', serif;
        color: #4a2e1f !important;
    }

    .stTextArea textarea {
        background-color: #fffdf7;
        border: 1px solid #d9cbb8;
        border-radius: 8px;
        color: #000;
    }

    .stButton>button {
        background-color: #795548;
        color: #fff;
        font-size: 1.05rem;
        border-radius: 6px;
        padding: 0.6rem 1rem;
        border: none;
    }

    .stButton>button:hover {
        background-color: #5d4037;
        color: #fff;
    }

    .highlight {
        background-color: #fffdf7;
        border-left: 5px solid #795548;
        padding: 1rem;
        border-radius: 6px;
        margin-top: 1rem;
        font-size: 1.05rem;
        line-height: 1.6;
        color: #000;
    }

    .token-info {
        font-size: 0.9rem;
        color: #555;
        margin-top: 0.5rem;
    }

    .footer {
        text-align: center;
        font-size: 0.9rem;
        margin-top: 3rem;
        color: #555;
    }

    /* Make file uploader label black */
    section[data-testid="stFileUploader"] label {
        color: #000 !important;
    }

    /* Style file uploader container */
    section[data-testid="stFileUploader"] {
        background-color: #fffdf7;
        border: 1px solid #d9cbb8;
        border-radius: 8px;
        padding: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# 🔹 Logo centered below title
logo_base64 = get_base64("gptlogo.png")
st.markdown(
    f"""
    <div style="text-align: center; margin: 1rem 0;">
        <img src="data:image/png;base64,{logo_base64}" style="width:150px;">
    </div>
    """,
    unsafe_allow_html=True
)

# 🔹 Start wrapper div
st.markdown('<div class="main-content-wrapper">', unsafe_allow_html=True)

# 🔹 Title and subtitle
st.markdown("<h1>🎬 Foundational Story Elements Studio</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='font-size:1.1rem; margin-top:0; color:#333;'>Evaluate the core strength of your story concept—powered by LingIQ AI Linguistic Agents.</p>",
    unsafe_allow_html=True
)

# 🔹 Sidebar with controls
with st.sidebar:
    st.markdown("## 📂 Upload and Configure")
    genai.configure(api_key=st.secrets["api"]["google_api_key"])

    uploaded_file = st.file_uploader(
        "Upload a .txt or .pdf manuscript excerpt:",
        type=["txt", "pdf"]
    )

    st.markdown(
        "<div style='font-size:0.9rem; color:#555;'>ℹ️ Tip: Short excerpts (1–3 pages) work best for evaluation.</div>",
        unsafe_allow_html=True
    )

    # Prompt customization
    # st.markdown("### ✏️ Prompt Template")
    # default_story_prompt = (
    #     "You are a literary concept evaluation assistant. Given a passage from a story, you will assess the foundational story elements.\n\n"
    #     "Concept: Does the basic story grab you immediately? Is it strong enough to build upon?\n\n"
    #     "Introducing the \"So What?\" Test: Before diving into specifics, you must access the fundamental compelling nature of the story as it unfolds from its premise. Many stories share basic setups. The \"So What?\" test is a way to push past that generic surface and determine if the narrative develops the premise in a way that creates truly engaging stakes, reveals character through meaningful choices, and answers the crucial question: Why should the audience care deeply about this particular story? It's less about finding a shocking twist in the premise itself, and more about identifying how the execution makes the story compelling.\n\n"
    #     "First, briefly summarize the premise.\n\n"
    #     "Then, critically evaluate whether the story passes the \"So What?\" test in 3–5 sentences.\n\n"
    #     "Passage:\n{literary_text}"
    # )
    default_story_prompt = (
    "You are a literary concept evaluation assistant. Given a passage from a story, you will produce a comprehensive report assessing the story's foundational elements for potential adaptation.\n\n"
    "Your assessment should address each of the following sections in detail:\n\n"
    "1. **Premise Summary:** Provide a clear 1–2 sentence logline that captures the essence, including any unique hooks.\n"
    "2. **So What? Test:** Evaluate whether the premise and execution transcend generic setups. Identify which of the following pathways are present:\n"
    "   - Plot/Stake Escalation\n"
    "   - Character Differentiation\n"
    "   - Compelling World/Setting\n"
    "3. **Originality & Freshness:** Analyze how the story compares to common genre conventions. Highlight any novel elements.\n"
    "4. **Inherent Conflict:** Describe the central conflict(s) and the stakes involved.\n"
    "5. **Narrative Engine:** Explain what drives the story forward.\n"
    "6. **Pacing & Momentum:** Comment on the pacing of the narrative. Are there sections that feel too slow or rushed?\n"
    "7. **Key Turning Points:** Identify major events that change the direction of the story, mapping them to common narrative structures (inciting incident, midpoint, climax, resolution).\n"
    "8. **Satisfying Trajectory:** Evaluate whether the story builds logically toward a resolution that feels earned and resonant.\n\n"
    "For each section, write 2–4 sentences of analysis.\n\n"
    "Passage:\n{literary_text}"
)


    custom_story_prompt = st.text_area(
        "Prompt Template",
        value=default_story_prompt,
        height=300,
        key="story_prompt"
    )

# 🔹 Initialize literary text variable
literary_text = ""

# 🔹 Process uploaded file
if uploaded_file is not None:
    try:
        if uploaded_file.type == "text/plain":
            literary_text = uploaded_file.read().decode("utf-8")
        elif uploaded_file.type == "application/pdf" or uploaded_file.name.endswith(".pdf"):
            file_bytes = io.BytesIO(uploaded_file.read())
            with pdfplumber.open(file_bytes) as pdf:
                pages_text = [page.extract_text() or "" for page in pdf.pages]
            literary_text = "\n".join(pages_text)
        else:
            st.warning("⚠️ Unsupported file type.")

        if literary_text:
            st.markdown("#### 📘 Uploaded Text Preview")
            st.text_area("", value=literary_text, height=300)

            approx_token_count = len(literary_text) // 4
            estimated_cost = (approx_token_count / 1000) * 0.000125

            st.markdown(
                f"<div class='token-info'>🔢 <strong>Estimated tokens:</strong> {approx_token_count} &nbsp;&nbsp;💰 <strong>Estimated cost:</strong> ${estimated_cost:.6f}</div>",
                unsafe_allow_html=True
            )
        else:
            st.error("❌ Could not extract text from the uploaded file.")

    except Exception as e:
        st.error(f"❌ Error processing file: {e}")

# 🔹 Generate evaluation
if st.button("📝 Run Evaluation") and literary_text:
    with st.spinner("Evaluating story concept..."):
        prompt_to_use_story = custom_story_prompt.format(literary_text=literary_text)
        try:
            model = genai.GenerativeModel("gemini-2.5-flash")
            response = model.generate_content(prompt_to_use_story)
            st.success("✅ Analysis complete!")
            st.markdown("### 🎯 Foundational Story Elements Evaluation")
            with st.expander("Click to view full report", expanded=True):
                st.markdown(
                f"<div class='highlight'>{response.text.strip()}</div>",
                unsafe_allow_html=True
            )
            st.download_button(
            label="📥 Download Evaluation Report",
            data=response.text.strip(),
            file_name="story_evaluation.txt",
            mime="text/plain"
    )
        except Exception as e:
            st.error(f"❌ Error generating story analysis: {str(e)}")


# 🔹 Footer
st.markdown(
    "<div class='footer'>🎥 Created for creative professionals—screenwriters, novelists, and storytellers.</div>",
    unsafe_allow_html=True
)

# 🔹 End wrapper div
st.markdown('</div>', unsafe_allow_html=True)
