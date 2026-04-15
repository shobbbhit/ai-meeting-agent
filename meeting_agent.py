import streamlit as st
from crewai import Agent, Task, Crew
from crewai.process import Process
from crewai_tools import SerperDevTool
from langchain_anthropic import ChatAnthropic
import os

# ------------------- UI SETUP -------------------
st.set_page_config(page_title="AI Meeting Agent 📝", layout="wide")
st.title("AI Meeting Preparation Agent 📝")

# ------------------- SIDEBAR -------------------
st.sidebar.header("API Keys")

anthropic_api_key = st.sidebar.text_input("Anthropic API Key", type="password")
serper_api_key = st.sidebar.text_input("Serper API Key", type="password")

# ------------------- MAIN LOGIC -------------------
if anthropic_api_key and serper_api_key:
    os.environ["ANTHROPIC_API_KEY"] = anthropic_api_key
    os.environ["SERPER_API_KEY"] = serper_api_key

    # ✅ ANTHROPIC LLM
    llm = ChatAnthropic(
        model="claude-3-5-sonnet-20241022",
        temperature=0.7,
        api_key=anthropic_api_key
    )

    # ✅ TOOL (MANDATORY FOR ALL AGENTS)
    search_tool = SerperDevTool()

    # ------------------- INPUTS -------------------
    company_name = st.text_input("Enter the company name:")
    meeting_objective = st.text_input("Enter the meeting objective:")
    attendees = st.text_area("Enter attendees and roles:")
    meeting_duration = st.number_input(
        "Meeting duration (minutes)",
        min_value=15,
        max_value=180,
        value=60,
        step=15
    )
    focus_areas = st.text_input("Focus areas or concerns:")

    # ------------------- AGENTS -------------------
    context_analyzer = Agent(
        role='Meeting Context Specialist',
        goal='Analyze meeting background',
        backstory='Expert in business analysis',
        verbose=True,
        allow_delegation=False,
        tools=[search_tool],
        llm=llm
    )

    industry_expert = Agent(
        role='Industry Expert',
        goal='Provide industry insights',
        backstory='Industry analyst',
        verbose=True,
        allow_delegation=False,
        tools=[search_tool],
        llm=llm
    )

    strategist = Agent(
        role='Meeting Strategist',
        goal='Create agenda and strategy',
        backstory='Expert planner',
        verbose=True,
        allow_delegation=False,
        tools=[search_tool],
        llm=llm
    )

    communicator = Agent(
        role='Communication Specialist',
        goal='Create executive brief',
        backstory='Expert communicator',
        verbose=True,
        allow_delegation=False,
        tools=[search_tool],
        llm=llm
    )

    # ------------------- TASKS -------------------
    task1 = Task(
        description=f"""
        Analyze {company_name} for meeting.
        Objective: {meeting_objective}
        Attendees: {attendees}
        Focus: {focus_areas}
        Include company research and insights.
        """,
        agent=context_analyzer,
        expected_output="Comprehensive company analysis"
    )

    task2 = Task(
        description=f"""
        Provide industry analysis for {company_name}.
        Include trends, competitors, and opportunities.
        """,
        agent=industry_expert,
        expected_output="Industry insights and analysis"
    )

    task3 = Task(
        description=f"""
        Create a structured meeting agenda for {meeting_duration} minutes.
        Include talking points and strategy.
        """,
        agent=strategist,
        expected_output="Detailed meeting agenda"
    )

    task4 = Task(
        description=f"""
        Create an executive briefing for {company_name}.
        Include summary, key points, Q&A, and recommendations.
        """,
        agent=communicator,
        expected_output="Executive briefing document"
    )

    # ------------------- CREW -------------------
    crew = Crew(
        agents=[context_analyzer, industry_expert, strategist, communicator],
        tasks=[task1, task2, task3, task4],
        verbose=True,
        process=Process.sequential
    )

    # ------------------- EXECUTION -------------------
    if st.button("Prepare Meeting"):
        with st.spinner("Preparing your meeting..."):
            result = crew.kickoff()
        st.markdown(result)

else:
    st.warning("Please enter Anthropic and Serper API keys.")
