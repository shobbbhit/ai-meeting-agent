import streamlit as st
from crewai import Agent, Task, Crew
from crewai.process import Process
from crewai_tools import SerperDevTool
from langchain_openai import ChatOpenAI
import os

# Streamlit setup
st.set_page_config(page_title="AI Meeting Agent 📝", layout="wide")
st.title("AI Meeting Preparation Agent 📝")

# Sidebar API Keys
st.sidebar.header("API Keys")

openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
serper_api_key = st.sidebar.text_input("Serper API Key", type="password")

# Check keys
if openai_api_key and serper_api_key:
    os.environ["OPENAI_API_KEY"] = openai_api_key
    os.environ["SERPER_API_KEY"] = serper_api_key

    # LLM
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.7
    )

    search_tool = SerperDevTool()

    # Inputs
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

    # Agents
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
        tools=[],   # ✅ FIX HERE
        llm=llm
    )

    communicator = Agent(
        role='Communication Specialist',
        goal='Create executive brief',
        backstory='Expert communicator',
        verbose=True,
        allow_delegation=False,
        tools=[],   # ✅ FIX HERE
        llm=llm
    )

    # Tasks
    task1 = Task(
        description=f"""
        Analyze {company_name} for meeting.
        Objective: {meeting_objective}
        Attendees: {attendees}
        Focus: {focus_areas}
        """,
        agent=context_analyzer
    )

    task2 = Task(
        description=f"""
        Provide industry analysis for {company_name}.
        Include trends and competitors.
        """,
        agent=industry_expert
    )

    task3 = Task(
        description=f"""
        Create meeting agenda for {meeting_duration} minutes.
        Include talking points and strategy.
        """,
        agent=strategist
    )

    task4 = Task(
        description=f"""
        Create executive brief for {company_name}.
        Include summary, Q&A, recommendations.
        """,
        agent=communicator
    )

    # Crew
    crew = Crew(
        agents=[context_analyzer, industry_expert, strategist, communicator],
        tasks=[task1, task2, task3, task4],
        verbose=True,
        process=Process.sequential
    )

    # Run
    if st.button("Prepare Meeting"):
        with st.spinner("Preparing your meeting..."):
            result = crew.kickoff()
        st.markdown(result)

else:
    st.warning("Please enter OpenAI and Serper API keys.")
