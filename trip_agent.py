from crewai import Agent, Task, Crew
from langchain_groq import ChatGroq
import os

class TripAgent:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable not set.")
        
        # Explicitly specify the model supported by Groq
        self.llm = ChatGroq(
            model="llama3-70b-8192",  # Use a known Groq-supported model
            temperature=0.7,
            api_key=api_key
        )

    def city_selector_agent(self):
        return Agent(
            role="City Selection Expert",
            goal="Identify the best cities to visit based on user preferences.",
            backstory="An expert travel geographer with extensive knowledge.",
            llm=self.llm,
            verbose=True
        )

    def local_expert_agent(self):
        return Agent(
/hello            role="Local Destination Expert",
            goal="Provide detailed insights about selected cities.",
            backstory="A knowledgeable local guide.",
            llm=self.llm,
            verbose=True
        )

    def travel_planner_agent(self):
        return Agent(
            role="Professional Travel Planner",
            goal="Create detailed day-by-day itineraries.",
            backstory="An experienced travel coordinator.",
            llm=self.llm,
            verbose=True
        )

    def budget_manager_agent(self):
        return Agent(
            role="Travel Budget Specialist",
            goal="Optimize travel budgets.",
            backstory="A finance-savvy travel expert.",
            llm=self.llm,
            verbose=True
        )

class Triptasks:
    def city_selection_task(self, agent, inputs):
        return Task(
            description=f"Analyze preferences: Travel type: {inputs['travel_type']}, Interests: {inputs['interests']}, Season: {inputs['season']}. Provide 3 city options.",
            agent=agent,
            expected_output="Bullet-point list of 3 cities."
        )

    def local_expert_task(self, agent, selected_cities):
        return Task(
            description=f"Provide insights for {', '.join(selected_cities)}: attractions, customs, gems.",
            agent=agent,
            expected_output="Detailed guide for each city."
        )

    def travel_planner_task(self, agent, selected_city):
        return Task(
            description=f"Create a 5-day itinerary for {selected_city}.",
            agent=agent,
            expected_output="Detailed day-by-day plan."
        )

    def budget_manager_task(self, agent, selected_city, budget):
        return Task(
            description=f"Plan budget for {selected_city} within {budget} USD.",
            agent=agent,
            expected_output="Budget breakdown with tips."
        )

class TripCrew:
    def __init__(self, inputs):
        self.inputs = inputs
        self.agents = TripAgent()
        self.tasks = Triptasks()

    def create_crew(self, selected_city="Paris", budget=2000):
        city_selector = self.agents.city_selector_agent()
        local_expert = self.agents.local_expert_agent()
        travel_planner = self.agents.travel_planner_agent()
        budget_manager = self.agents.budget_manager_agent()
        city_selection_task = self.tasks.city_selection_task(city_selector, self.inputs)
        local_expert_task = self.tasks.local_expert_task(local_expert, ["Paris", "Tokyo", "Rome"])
        travel_planner_task = self.tasks.travel_planner_task(travel_planner, selected_city)
        budget_manager_task = self.tasks.budget_manager_task(budget_manager, selected_city, budget)
        return Crew(
            agents=[city_selector, local_expert, travel_planner, budget_manager],
            tasks=[city_selection_task, local_expert_task, travel_planner_task, budget_manager_task],
            verbose=True
        )