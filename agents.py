from crewai import Agent
from langchain_groq import ChatGroq
from typing import Optional

# Default API key configuration
DEFAULT_GROQ_API_KEY = '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'

def create_llm(api_key: str = None, model_name: str = "llama3-70b-8192", temperature: float = 0) -> ChatGroq:
    """Create LLM instance with error handling."""
    try:
        # Use provided API key or fall back to default
        key_to_use = api_key if api_key else DEFAULT_GROQ_API_KEY
        return ChatGroq(
            temperature=temperature,
            model_name=model_name,
            api_key=key_to_use
        )
    except Exception as e:
        raise Exception(f"Error initializing LLM: {str(e)}")

def create_agent(
    llm: ChatGroq,
    role: str,
    goal: str,
    backstory: str,
    verbose: bool = True,
    allow_delegation: bool = False
) -> Agent:
    """Create an agent with error handling."""
    try:
        return Agent(
            llm=llm,
            role=role,
            goal=goal,
            backstory=backstory,
            verbose=verbose,
            allow_delegation=allow_delegation
        )
    except Exception as e:
        raise Exception(f"Error creating {role} agent: {str(e)}")

def initialize_agents(api_key: Optional[str] = None) -> dict:
    """Initialize all agents and return them in a dictionary."""
    try:
        llm = create_llm(api_key)
        
        agents = {
            'planner': create_agent(
                llm=llm,
                role="Content Planner",
                goal="Plan engaging and factually accurate content on {topic}",
                backstory="You're working on planning a blog article about the topic: {topic}. "
                         "You collect information that helps the audience learn something and "
                         "make informed decisions."
            ),
            
            'writer': create_agent(
                llm=llm,
                role="Content Writer",
                goal="Write insightful and factually accurate opinion piece about the topic: {topic}",
                backstory="You're working on writing a new opinion piece about the topic: {topic}. "
                         "You base your writing on the work of the Content Planner. "
                         "You provide objective and impartial insights."
            ),
            
            'editor': create_agent(
                llm=llm,
                role="Editor",
                goal="Edit a given blog post to align with the writing style of the organization",
                backstory="You are an editor who ensures content follows journalistic best practices "
                         "and provides balanced viewpoints."
            ),
            
            'industry_analyst': create_agent(
                llm=llm,
                role="Industry Analyst",
                goal="Provide the latest industry insights and trends on {topic}",
                backstory="You're an industry analyst focusing on {topic}, providing latest trends "
                         "and well-rounded insights."
            ),
            
            'copywriter': create_agent(
                llm=llm,
                role="Copywriter",
                goal="Generate captivating and persuasive copy on {topic}",
                backstory="You are a skilled copywriter creating impactful copy for various formats "
                         "including headlines, social media, and promotional material."
            )
        }
        
        return agents
        
    except Exception as e:
        raise Exception(f"Error initializing agents: {str(e)}")