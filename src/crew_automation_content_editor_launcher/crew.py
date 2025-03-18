from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from .tools.web_search_tool import WebSearchTool
from .tools.csv_search_tool import CSVSearchTool
from crew_automation_content_editor_launcher.utils.logger import logger

@CrewBase
class CrewAutomationContentEditorLauncherCrew():
    """CrewAutomationContentEditorLauncher crew"""

    @agent
    def leader(self) -> Agent:
        return Agent(
            config=self.agents_config['leader'],
            tools=[CSVSearchTool()],
        )

    @agent
    def web_searcher(self) -> Agent:
        return Agent(
            config=self.agents_config['web_searcher'],
            tools=[WebSearchTool()],
        )

    @agent
    def copywriter(self) -> Agent:
        return Agent(
            config=self.agents_config['copywriter'],
            tools=[CSVSearchTool()],
        )

    @agent
    def editor(self) -> Agent:
        return Agent(
            config=self.agents_config['editor'],
            tools=[CSVSearchTool()],
        )


    @task
    def initialization_task(self) -> Task:
        return Task(
            config=self.tasks_config['initialization_task'],
            tools=[CSVSearchTool()],
        )

    @task
    def brief_dispatch_task(self) -> Task:
        return Task(
            config=self.tasks_config['brief_dispatch_task'],
            tools=[],
        )

    @task
    def web_research_task(self) -> Task:
        return Task(
            config=self.tasks_config['web_research_task'],
            tools=[WebSearchTool()],
        )

    @task
    def content_creation_task(self) -> Task:
        return Task(
            config=self.tasks_config['content_creation_task'],
            tools=[CSVSearchTool()],
        )

    @task
    def revision_task(self) -> Task:
        return Task(
            config=self.tasks_config['revision_task'],
            tools=[CSVSearchTool()],
        )

    @task
    def finalization_task(self) -> Task:
        return Task(
            config=self.tasks_config['finalization_task'],
            tools=[],
        )


    @crew
    def crew(self) -> Crew:
        """Creates the CrewAutomationContentEditorLauncher crew"""
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )

# Web Searcher Agent
web_searcher = Agent(
    role='Trending Content Researcher',
    goal='Find engaging, viral content patterns from social/digital platforms',
    backstory="""Expert in identifying emerging trends and high-engagement content
    formats across platforms like TikTok, Instagram, and YouTube.""",
    tools=[WebSearchTool()],
    verbose=True
)

# Copywriter Agent
copywriter = Agent(
    role='Creative Content Architect',
    goal='Craft compelling narratives using storytelling techniques',
    backstory="""Specialist in transforming information into engaging stories
    through humor, analogies, and interactive elements.""",
    tools=[CSVSearchTool()],
    verbose=True
)

# Editor Agent
editor = Agent(
    role='Engagement Optimizer',
    goal='Enhance content appeal without compromising message clarity',
    backstory="""Expert in refining content flow, adding visual storytelling
    elements, and ensuring audience connection.""",
    tools=[CSVSearchTool()],
    verbose=True
)
