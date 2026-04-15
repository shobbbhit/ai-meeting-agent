import streamlit as st
from anthropic import Anthropic
import os
import json

st.set_page_config(page_title="AI Meeting Agent 📝", layout="wide")
st.title("AI Meeting Preparation Agent 📝")

st.sidebar.header("API Keys")
anthropic_api_key = st.sidebar.text_input("Anthropic API Key", type="password")
serper_api_key = st.sidebar.text_input("Serper API Key", type="password")

if anthropic_api_key and serper_api_key:
    os.environ["ANTHROPIC_API_KEY"] = anthropic_api_key
    os.environ["SERPER_API_KEY"] = serper_api_key

    client = Anthropic(api_key=anthropic_api_key)

    company_name = st.text_input("Enter the company name:")
    meeting_objective = st.text_input("Enter the meeting objective:")
    attendees = st.text_area("Enter attendees and roles:")
    meeting_duration = st.number_input("Meeting duration (minutes)", min_value=15, max_value=180, value=60, step=15)
    focus_areas = st.text_input("Focus areas or concerns:")

    if st.button("Prepare Meeting"):
        with st.spinner("Preparing your meeting..."):
            system_prompt = """You are an expert meeting preparation assistant. 
            Analyze the following company and meeting details to provide:
            1. Company background and context
            2. Industry insights and trends
            3. A detailed meeting agenda
            4. Executive briefing with talking points and Q&A prep"""

            user_message = f"""
            Company: {company_name}
            Meeting Objective: {meeting_objective}
            Attendees: {attendees}
            Duration: {meeting_duration} minutes
            Focus Areas: {focus_areas}
            
            Please provide a comprehensive meeting preparation package."""

            response = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=4096,
                messages=[
                    {"role": "user", "content": user_message}
                ],
                system=system_prompt
            )
            
            result = response.content[0].text
            st.markdown(result)

else:
    st.warning("Please enter both Anthropic and Serper API keys.")
