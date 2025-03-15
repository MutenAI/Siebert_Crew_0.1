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
