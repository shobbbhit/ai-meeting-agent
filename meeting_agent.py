import streamlit as st
from crewai import Agent, Task, Crew
from crewai.process import Process
from crewai_tools import SerperDevTool
import google.generativeai as genai
import os

# Streamlit app setup
st.set_page_config(page_title="AI Meeting Agent 📝", layout="wide")
st.title("AI Meeting Preparation Agent 📝")

# Sidebar for API keys
st.sidebar.header("API Keys")
gemini_api_key = st.sidebar.text_input("Google Gemini API Key", type="password")
serper_api_key = st.sidebar.text_input("Serper API Key", type="password")

# Check if all API keys are set
if gemini_api_key and serper_api_key:
    os.environ["GEMINI_API_KEY"] = gemini_api_key
    os.environ["SERPER_API_KEY"] = serper_api_key

    # Configure Gemini (for future use if needed)
    genai.configure(api_key=gemini_api_key)

    search_tool = SerperDevTool()

    # Input fields
    company_name = st.text_input("Enter the company name:")
    meeting_objective = st.text_input("Enter the meeting objective:")
    attendees = st.text_area("Enter the attendees and their roles (one per line):")
    meeting_duration = st.number_input(
        "Enter the meeting duration (in minutes):",
        min_value=15,
        max_value=180,
        value=60,
        step=15
    )
    focus_areas = st.text_input("Enter any specific areas of focus or concerns:")

    # Define Agents (NO LLM here)
    context_analyzer = Agent(
        role='Meeting Context Specialist',
        goal='Analyze and summarize key background information for the meeting',
        backstory='Expert at understanding business context quickly.',
        verbose=True,
        allow_delegation=False,
        tools=[search_tool]
    )

    industry_insights_generator = Agent(
        role='Industry Expert',
        goal='Provide industry analysis and trends',
        backstory='Seasoned analyst with deep industry knowledge.',
        verbose=True,
        allow_delegation=False,
        tools=[search_tool]
    )

    strategy_formulator = Agent(
        role='Meeting Strategist',
        goal='Create meeting strategy and agenda',
        backstory='Expert meeting planner.',
        verbose=True,
        allow_delegation=False,
    )

    executive_briefing_creator = Agent(
        role='Communication Specialist',
        goal='Create concise executive briefings',
        backstory='Expert communicator.',
        verbose=True,
        allow_delegation=False,
    )

    # Tasks
    context_analysis_task = Task(
        description=f"""
        Analyze the meeting with {company_name}.
        Objective: {meeting_objective}
        Attendees: {attendees}
        Duration: {meeting_duration} minutes
        Focus: {focus_areas}

        Include company research, news, competitors.
        """,
        agent=context_analyzer
    )

    industry_analysis_task = Task(
        description=f"""
        Provide industry analysis for {company_name}.
        Include trends, competition, opportunities.
        """,
        agent=industry_insights_generator
    )

    strategy_task = Task(
        description=f"""
        Create a detailed meeting agenda for {meeting_duration} minutes.
        Include talking points and strategy.
        """,
        agent=strategy_formulator
    )

    brief_task = Task(
        description=f"""
        Create executive brief for meeting with {company_name}.
        Include summary, talking points, Q&A, recommendations.
        """,
        agent=executive_briefing_creator
    )

    # Crew
    crew = Crew(
        agents=[
            context_analyzer,
            industry_insights_generator,
            strategy_formulator,
            executive_briefing_creator
        ],
        tasks=[
            context_analysis_task,
            industry_analysis_task,
            strategy_task,
            brief_task
        ],
        verbose=True,
        process=Process.sequential
    )

    # Run
    if st.button("Prepare Meeting"):
        with st.spinner("Preparing your meeting..."):
            result = crew.kickoff()
        st.markdown(result)

else:
    st.warning("Please enter both API keys to continue.")
