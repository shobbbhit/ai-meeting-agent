import streamlit as st
import requests

st.set_page_config(page_title="AI Meeting Agent 📝", layout="wide")
st.title("AI Meeting Preparation Agent 📝")

st.sidebar.header("API Key")
openrouter_api_key = st.sidebar.text_input("OpenRouter API Key (free at openrouter.ai)", type="password")

if openrouter_api_key:
    company_name = st.text_input("Enter the company name:")
    meeting_objective = st.text_input("Enter the meeting objective:")
    attendees = st.text_area("Enter attendees and roles:")
    meeting_duration = st.number_input("Meeting duration (minutes)", min_value=15, max_value=180, value=60, step=15)
    focus_areas = st.text_input("Focus areas or concerns:")

    if st.button("Prepare Meeting"):
        with st.spinner("Preparing your meeting..."):
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {openrouter_api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://ai-meeting-agent.streamlit.app",
                },
                json={
                    "model": "meta-llama/llama-3.3-70b-instruct:free",
                    "messages": [
                        {"role": "system", "content": "You are an expert meeting preparation assistant."},
                        {"role": "user", "content": f"""
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

Format everything clearly with markdown headings."""}
                    ],
                    "max_tokens": 4096
                }
            )
            result = response.json()
            if "choices" in result:
                st.markdown(result["choices"][0]["message"]["content"])
            else:
                st.error(f"API Error: {result}")
else:
    st.warning("Please enter your OpenRouter API key in the sidebar.")
