from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from crewai_tools import SerperDevTool

@CrewBase
class FinancialAnalyst():
    """FinancialAnalyst crew"""

    agents: List[BaseAgent]
    tasks: List[Task]
  
    @agent
    def researcher(self) -> Agent:
        """Researcher agent"""
        return Agent(config=self.agents_config['researcher'], verbose=True, tools=[SerperDevTool()])
    
    @agent
    def analyst(self) -> Agent:
        """Analyst agent"""
        return Agent(config=self.agents_config['analyst'], verbose=True)
    
    @task
    def research_task(self) -> Task:
        """Research task"""
        return Task(config=self.tasks_config['research_task'], verbose=True)
    
    @task
    def analysis_task(self) -> Task:
        """Analysis task"""
        return Task(config=self.tasks_config['analysis_task'], verbose=True)
    
    @crew
    def crew(self) -> Crew:
        """Crew"""
        return Crew(
            agents = self.agents,
            tasks = self.tasks,
            process = Process.sequential,
            verbose = True,
        )
    