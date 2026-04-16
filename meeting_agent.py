import streamlit as st
import google.generativeai as genai
import os

st.set_page_config(page_title="AI Meeting Agent 📝", layout="wide")
st.title("AI Meeting Preparation Agent 📝")

st.sidebar.header("API Keys")
gemini_api_key = st.sidebar.text_input("Google Gemini API Key", type="password")
serper_api_key = st.sidebar.text_input("Serper API Key", type="password")

if gemini_api_key and serper_api_key:
    os.environ["SERPER_API_KEY"] = serper_api_key
    genai.configure(api_key=gemini_api_key)

    company_name = st.text_input("Enter the company name:")
    meeting_objective = st.text_input("Enter the meeting objective:")
    attendees = st.text_area("Enter attendees and roles:")
    meeting_duration = st.number_input("Meeting duration (minutes)", min_value=15, max_value=180, value=60, step=15)
    focus_areas = st.text_input("Focus areas or concerns:")

    if st.button("Prepare Meeting"):
        with st.spinner("Preparing your meeting..."):
            model = genai.GenerativeModel("gemini-2.0-flash")
            prompt = f"""You are an expert meeting preparation assistant.
            
Company: {company_name}
Meeting Objective: {meeting_objective}
Attendees: {attendees}
Duration: {meeting_duration} minutes
Focus Areas: {focus_areas}

Provide a comprehensive meeting preparation package including:
1. Company background and context
2. Industry insights and trends
3. A detailed time-boxed meeting agenda
4. Executive briefing with talking points and Q&A prep
5. Strategic recommendations and next steps

Format everything clearly with markdown headings."""

            response = model.generate_content(prompt)
            st.markdown(response.text)

else:
    st.warning("Please enter your Gemini and Serper API keys.")
