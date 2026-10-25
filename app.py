import streamlit as st
from google import genai

MODEL = "gemini-3.8-flash"  # replace with the current free model name from AI Studio

st.set_page_config(page_title="Feedback Analyzer", page_icon="📊")
st.title("📊 Customer Feedback Analyzer")
st.write("Paste customer comments (one per line) or upload a .txt file.")

client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

focus = st.selectbox(
    "What should the analysis focus on?",
    ["General overview", "Product problems", "Customer service", "Pricing"],
)

pasted = st.text_area("Customer feedback", height=250)
uploaded = st.file_uploader("...or upload a .txt file", type="txt")

feedback = pasted
if uploaded:
    feedback = uploaded.read().decode("utf-8")

if st.button("Analyze"):
    if not feedback.strip():
        st.warning("Please add some feedback first.")
    else:
        prompt = f"""You are a customer insights analyst.
Focus area: {focus}.
Analyze the customer feedback below and give me:
1. Overall sentiment (positive / mixed / negative) with a one-line reason
2. Top 3 recurring themes, each with a short example
3. Top 3 recommended actions, ranked by likely business impact
Keep it concise and written for a busy manager.

FEEDBACK:
{feedback}"""
        with st.spinner("Analyzing..."):
            try:
                result = client.models.generate_content(model=MODEL, contents=prompt)
                st.markdown(result.text)
            except Exception as e:
                st.error(f"Something went wrong: {e}")
