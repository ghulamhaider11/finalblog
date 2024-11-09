from crewai import Task
from typing import Dict
from crewai import Agent

def create_task(
    description: str,
    expected_output: str,
    agent: Agent
) -> Task:
    """Create a task with error handling."""
    try:
        return Task(
            description=description,
            expected_output=expected_output,
            agent=agent
        )
    except Exception as e:
        raise Exception(f"Error creating task: {str(e)}")

def initialize_tasks(agents: Dict[str, Agent]) -> Dict[str, Task]:
    """Initialize all tasks and return them in a dictionary."""
    try:
        return {
            'plan': create_task(
                description=(
                    "1. Research and analyze the latest trends and developments on {topic}\n"
                    "2. Identify the target audience and their key interests\n"
                    "3. Create a detailed content outline including:\n"
                    "   - Introduction\n"
                    "   - Key points to cover\n"
                    "   - Supporting data/examples\n"
                    "   - Conclusion\n"
                    "4. Suggest relevant SEO keywords"
                ),
                expected_output="A detailed content plan with outline, target audience analysis, and SEO strategy",
                agent=agents['planner']
            ),
            
            'write': create_task(
                description=(
                    "1. Follow the content plan to write a comprehensive blog post\n"
                    "2. Ensure natural integration of SEO keywords\n"
                    "3. Write engaging headers and subheaders\n"
                    "4. Include relevant examples and data\n"
                    "5. Craft a compelling introduction and conclusion\n"
                    "6. Add calls-to-action where appropriate"
                ),
                expected_output="A well-structured blog post in markdown format with proper sections and formatting",
                agent=agents['writer']
            ),
            
            'edit': create_task(
                description=(
                    "1. Review the content for grammar and style\n"
                    "2. Check for consistency in tone and messaging\n"
                    "3. Verify all facts and claims\n"
                    "4. Ensure proper formatting and structure\n"
                    "5. Optimize for readability and engagement"
                ),
                expected_output="A polished, publication-ready blog post that meets professional standards",
                agent=agents['editor']
            ),
            
            'analyze': create_task(
                description=(
                    "1. Conduct thorough industry analysis on {topic}\n"
                    "2. Identify key market trends and innovations\n"
                    "3. Analyze major competitors and their strategies\n"
                    "4. Provide relevant statistics and case studies\n"
                    "5. Offer strategic insights and recommendations"
                ),
                expected_output="A comprehensive industry analysis report with actionable insights",
                agent=agents['industry_analyst']
            ),
            
            'copywrite': create_task(
                description=(
                    "1. Create engaging copy for {topic} including:\n"
                    "   - Headline options (5-7 variations)\n"
                    "   - Social media posts (Twitter, LinkedIn, Facebook)\n"
                    "   - Email marketing copy\n"
                    "2. Ensure consistent brand voice\n"
                    "3. Include strong calls-to-action\n"
                    "4. Optimize for each platform's requirements"
                ),
                expected_output="A complete set of marketing copy assets optimized for different platforms",
                agent=agents['copywriter']
            ),
        }
    except Exception as e:
        raise Exception(f"Error initializing tasks: {str(e)}")