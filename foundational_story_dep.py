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

# Dark gradient background CSS
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 25%, #0f3460 50%, #533483 75%, #7209b7 100%);
        background-attachment: fixed;
        min-height: 100vh;
    }
    .main-content-wrapper {
        padding: 20px 50px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 🔹 Google Fonts & custom styling for dark theme
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Open+Sans&display=swap');

    html, body, [class*="css"] {
        font-family: 'Open Sans', sans-serif;
        color: #ffffff !important;
    }

    h1 {
        font-family: 'Playfair Display', serif;
        font-size: 2.4rem;
        color: #ffffff !important;
        margin-bottom: 0.3rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.5);
    }

    h2, h3 {
        font-family: 'Playfair Display', serif;
        color: #ffffff !important;
    }

    .stTextArea textarea {
        background-color: rgba(255,255,255,0.1);
        border: 1px solid rgba(255,255,255,0.3);
        border-radius: 8px;
        color: #ffffff !important;
        backdrop-filter: blur(10px);
    }

    /* Text input styling */
    .stTextInput input {
        background-color: rgba(255,255,255,0.1);
        border: 1px solid rgba(255,255,255,0.3);
        border-radius: 8px;
        color: #ffffff !important;
        backdrop-filter: blur(10px);
    }

    /* Text area for file preview */
    .stTextArea textarea[readonly] {
        background-color: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 8px;
        color: #ffffff !important;
        backdrop-filter: blur(10px);
    }

    .stButton>button {
        background: linear-gradient(45deg, #7209b7, #533483);
        color: #fff;
        font-size: 1.05rem;
        border-radius: 6px;
        padding: 0.6rem 1rem;
        border: none;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }

    .stButton>button:hover {
        background: linear-gradient(45deg, #533483, #7209b7);
        color: #fff;
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.4);
    }

    .highlight {
        background-color: rgba(255,255,255,0.1);
        border-left: 5px solid #7209b7;
        padding: 1rem;
        border-radius: 6px;
        margin-top: 1rem;
        font-size: 1.05rem;
        line-height: 1.6;
        color: #ffffff;
        backdrop-filter: blur(10px);
    }

    .token-info {
        font-size: 0.9rem;
        color: #cccccc;
        margin-top: 0.5rem;
    }

    .footer {
        text-align: center;
        font-size: 0.9rem;
        margin-top: 3rem;
        color: #cccccc;
    }

    /* Make file uploader label white */
    section[data-testid="stFileUploader"] label {
        color: #ffffff !important;
    }

    /* Style file uploader container */
    section[data-testid="stFileUploader"] {
        background-color: rgba(255,255,255,0.1);
        border: 1px solid rgba(255,255,255,0.3);
        border-radius: 8px;
        padding: 1rem;
        backdrop-filter: blur(10px);
    }

    /* Sidebar styling for dark theme */
    .css-1d391kg {
        background-color: rgba(0,0,0,0.3);
        backdrop-filter: blur(10px);
    }

    /* Expander styling */
    .streamlit-expanderHeader {
        color: #ffffff !important;
    }

    /* Text input and text area labels */
    .stTextInput label, .stTextArea label {
        color: #ffffff !important;
    }

    /* Subtitle styling */
    p {
        color: #ffffff !important;
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
    "<p style='font-size:1.1rem; margin-top:0; color:#ffffff;'>Evaluate the core strength of your story concept—powered by LingIQ AI Linguistic Agents.</p>",
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
        "<div style='font-size:0.9rem; color:#cccccc;'>ℹ️ Tip: Short excerpts (1–3 pages) work best for evaluation.</div>",
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

    default_adaptation_prompt = (
    "You are a literary adaptability assessment assistant. Given a passage from a story, you will produce an adaptation report assessing if the story is suitable for adaptation into a movie or TV series.\n\n"
    "Your assessment should address each of the following sections in detail:\n\n"
    "1. **Concept Evaluation:** How easily and effectively can this text be translated into a visual medium? Consider the inherent visual elements, character arcs, and narrative structure.\n"
    "2. **Visual Storytelling Potential:** Identify key scenes or sequences that would translate well to screen. Are there strong visual metaphors, action sequences, or emotional beats?\n"
    "3. **Source Material Fidelity:** Discuss how closely the adaptation should adhere to the original text. Evaluate for elements that must be preserved to retain the central themes, plot points, and character arcs.\n"
    "4. **Internal versus External Conflict:** Identify how much of the story occurs through observable action, dialogue, and environmental interaction versus internal monologue or exposition. How can internal conflicts be effectively externalized for visual storytelling?\n"
    "5. **Dialogue Potential:** Provide an example scene with source dialogue that encapculates the story's essence. How can this dialogue be adapted for screen? Consider pacing, subtext, and character voice.\n"
    "6. **Structural Suitability:** Based purely on the narrative structure, does the story lend itself to a feature film or episodic series? Quantify the amount of dialgoue required to convey the story effectively.\n"
    "7. **Addressing Unfilmable Aspects:** Does the work rely heavily on abstract concepts, complex narrative devices (e.g., unreliable narrators, non-linear timelines), unique literary styles, or sensory experiences that may not translate well to screen?\n\n"
    "Passage:\n{literary_text}"
    )

    custom_adaptation_prompt = st.text_area(
        "Adaptation Prompt Template",
        value=default_adaptation_prompt,
        height=300,
        key="adaptation_prompt"
    )


    default_thematic_core_prompt = (
    "You are a thematic core analysis assistant. Given a passage from a story, you will produce a report assessing the thematic core of the story.\n\n"
    "Your assessment should address each of the following sections in detail:\n\n"
    "1. **Identifiable Themes:** Identify the primary themes present in the story. What are the key messages or ideas that the author is trying to convey? Why do these themes matter?\n" \
    "2. **Relevance:** Analyze if the themes speak to a timeless human experience. Do they resonate with universal emotions or situations such as love, loss, etc.?\n" \
    "3. **Emotional Resonance:** Discuss the emotional impact of the story. How do the themes evoke feelings in the reader?\n" \
    "4. **Cultural and Social Context:** Consider the broader context in which the story was written. How do societal issues influence its themes?\n" \
    "5. **Subtext and Symbolism:** Identify any elements conveyed through subtext or symbolism that enhance the thematic depth of the story. How does this add to the sophistication of the story?\n" \
    "Passage:\n{literary_text}"
    )

    custom_thematic_prompt = st.text_area(
        "Thematic Core Prompt Template",
        value=default_thematic_core_prompt,
        height=300,
        key="thematic_prompt"
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
        prompt_to_use_adaptation = custom_adaptation_prompt.format(literary_text=literary_text)
        prompt_to_use_thematic = custom_thematic_prompt.format(literary_text=literary_text)

        model = genai.GenerativeModel("gemini-2.5-flash")
        
        # Generate story elements analysis
        try:
            response = model.generate_content(prompt_to_use_story)
            st.success("✅ Story elements analysis complete!")
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
            st.error(f"❌ Error generating story elements analysis: {str(e)}")

        # Generate adaptation analysis
        try:
            adaptation_response = model.generate_content(prompt_to_use_adaptation)
            st.success("✅ Adaptation analysis complete!")
            st.markdown("### 🎥 Adaptation Suitability Evaluation")
            with st.expander("Click to view full adaptation report", expanded=True):
                st.markdown(
                    f"<div class='highlight'>{adaptation_response.text.strip()}</div>",
                    unsafe_allow_html=True
                )
            st.download_button(
                label="📥 Download Adaptation Report",
                data=adaptation_response.text.strip(),
                file_name="adaptation_evaluation.txt",
                mime="text/plain"
            )
        except Exception as e:
            st.error(f"❌ Error generating adaptation analysis: {str(e)}")

        # Generate thematic core analysis
        st.info("🔄 Generating thematic core analysis...")
        try:
            thematic_core_response = model.generate_content(prompt_to_use_thematic)
            st.success("✅ Thematic core analysis complete!")
            st.markdown("### 🌟 Thematic Core Evaluation")
            with st.expander("Click to view full thematic core report", expanded=True):
                st.markdown(
                    f"<div class='highlight'>{thematic_core_response.text.strip()}</div>",
                    unsafe_allow_html=True
                )
            st.download_button(
                label="📥 Download Thematic Core Report",
                data=thematic_core_response.text.strip(),
                file_name="thematic_core_evaluation.txt",
                mime="text/plain"
            )
        except Exception as thematic_error:
            st.error(f"❌ Error generating thematic core analysis: {str(thematic_error)}")


# 🔹 Footer
st.markdown(
    "<div class='footer'>🎥 Created for creative professionals—screenwriters, novelists, and storytellers.</div>",
    unsafe_allow_html=True
)

# 🔹 End wrapper div
st.markdown('</div>', unsafe_allow_html=True)
