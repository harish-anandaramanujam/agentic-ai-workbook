from tabnanny import verbose
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from pydantic import BaseModel, Field
from crewai_tools import SerperDevTool
from .tools.push_tool import PushNotificationTool
from crewai.memory import LongTermMemory, ShortTermMemory, EntityMemory
from crewai.memory.storage.rag_storage import RAGStorage
from crewai.memory.storage.ltm_sqlite_storage import LTMSQLiteStorage

class TrendingCompanies(BaseModel):
    """Tool to find trending companies"""
    name: str = Field(description="Company name")
    ticker: str = Field(description="Company stockticker")
    reason: str = Field(description="Reason for the company being trending")

class TrendingCompaniesList(BaseModel):
    """Tool to find trending companies"""
    companies: List[TrendingCompanies] = Field(description="List of trending companies")

class TrendingCompanyResearch(BaseModel):
    """ Detailed research on a company """
    name: str = Field(description="Company name")
    market_position: str = Field(description="Current market position and competitive analysis")
    future_outlook: str = Field(description="Future outlook and growth prospects")
    investment_potential: str = Field(description="Investment potential and suitability for investment")

class TrendingCompanyResearchList(BaseModel):
    """ A list of detailed research on all the companies """
    research_list: List[TrendingCompanyResearch] = Field(description="Comprehensive research on all trending companies")


@CrewBase
class StockPicker():
    """StockPicker crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def trending_company_finder(self)-> Agent:
        return Agent(config=self.agents_config['trending_company_finder'], tools=[SerperDevTool()], memory = True)

    @agent
    def financial_researcher(self)-> Agent:
        return Agent(config=self.agents_config['financial_researcher'], tools=[SerperDevTool()])

    @agent
    def stock_picker(self)-> Agent:
        return Agent(config=self.agents_config['stock_picker'], tools =[PushNotificationTool()], memory = True)
    
    @task
    def find_trending_companies(self) -> Task:
        return Task(
            config = self.tasks_config['find_trending_companies'],
            output_pydantic = TrendingCompaniesList
        )

    @task
    def research_trending_companies(self) -> Task:
        return Task(
            config = self.tasks_config['research_trending_companies'],
            output_pydantic = TrendingCompanyResearchList
        )

    @task
    def pick_best_company(self) -> Task:
        return Task(
            config = self.tasks_config['pick_best_company']
        )
    
    @crew
    def crew(self) -> Crew:
        manager = Agent(
            config = self.agents_config['manager'],
            allow_delegation = True
        )

        return Crew(
            agents = self.agents,
            tasks = self.tasks,
            process = Process.hierarchical,
            verbose= True,
            manager_agent = manager,
            memory=True,
            # Long-term memory for persistent storage across sessions
            long_term_memory = LongTermMemory(
                storage=LTMSQLiteStorage(
                    db_path="./memory/long_term_memory_storage.db"
                )
            ),
            # Short-term memory for current context using RAG
            short_term_memory = ShortTermMemory(
                storage = RAGStorage(
                        embedder_config={
                            "provider": "openai",
                            "config": {
                                "model": 'text-embedding-3-small'
                            }
                        },
                        type="short_term",
                        path="./memory/"
                    )
                ),            # Entity memory for tracking key information about entities
            entity_memory = EntityMemory(
                storage=RAGStorage(
                    embedder_config={
                        "provider": "openai",
                        "config": {
                            "model": 'text-embedding-3-small'
                        }
                    },
                    type="short_term",
                    path="./memory/"
                )
            ),
        )