__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import sqlite3


import streamlit as st
from crewai import Crew
from typing import List, Dict
import os
from agents import initialize_agents, DEFAULT_GROQ_API_KEY
from tasks import initialize_tasks

def create_crew(agents: List, tasks: List, verbose: int = 2) -> Crew:
    """Create a crew with error handling."""
    try:
        return Crew(
            agents=agents,
            tasks=tasks,
            verbose=verbose
        )
    except Exception as e:
        raise Exception(f"Error creating crew: {str(e)}")

def initialize_session_state():
    """Initialize session state variables."""
    if 'use_custom_key' not in st.session_state:
        st.session_state.use_custom_key = False
    if 'api_key' not in st.session_state:
        st.session_state.api_key = None

def main():
    st.set_page_config(page_title="AI Content Creation Crew", layout="wide")
    
    st.title("Multi-Agent Content Creation Workflow")
    
    # Initialize session state
    initialize_session_state()
    
    # API Key Selection
    st.sidebar.header("API Key Configuration")
    use_custom_key = st.sidebar.checkbox("Use Custom GROQ-API Key", value=st.session_state.use_custom_key)
    
    if use_custom_key:
        custom_key = st.sidebar.text_input(
            "Enter your Groq API Key",
            type="password",
            help="Enter your custom Groq API key"
        )
        if custom_key:
            st.session_state.api_key = custom_key
        else:
            st.sidebar.warning("Please enter your API key")
            return
    else:
        st.session_state.api_key = DEFAULT_GROQ_API_KEY
        st.sidebar.info("Using default API key")
    
    try:
        # Initialize agents and tasks with the selected API key
        agents = initialize_agents(st.session_state.api_key)
        tasks = initialize_tasks(agents)
        
        # Topic input
        topic = st.text_input(
            "Enter your content topic",
            help="What would you like the AI crew to write about?"
        )
        
        if not topic:
            st.info("Please enter a topic to generate content.")
            return
            
        # Content type selection
        content_type = st.radio(
            "Select content type:",
            ["Blog Post", "Industry Analysis", "Marketing Copy"]
        )
        
        if st.button("Generate Content", type="primary"):
            with st.spinner('Generating content...'):
                try:
                    # Select appropriate agents and tasks based on content type
                    if content_type == "Blog Post":
                        selected_agents = [agents['planner'], agents['writer'], agents['editor']]
                        selected_tasks = [tasks['plan'], tasks['write'], tasks['edit']]
                    elif content_type == "Industry Analysis":
                        selected_agents = [agents['industry_analyst']]
                        selected_tasks = [tasks['analyze']]
                    else:  # Marketing Copy
                        selected_agents = [agents['copywriter']]
                        selected_tasks = [tasks['copywrite']]
                    
                    # Create and run crew
                    crew = create_crew(selected_agents, selected_tasks)
                    result = crew.kickoff(inputs={"topic": topic})
                    
                    # Display results
                    st.success("Content generated successfully!")
                    st.markdown(result)
                    
                except Exception as e:
                    st.error(f"Error generating content: {str(e)}")
                    st.info("Please try again with different parameters or check your API key.")
    
    except Exception as e:
        st.error(f"Initialization error: {str(e)}")

if __name__ == "__main__":
    main()