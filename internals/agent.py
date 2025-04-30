import asyncio
import os

from dotenv import load_dotenv
from openai import AsyncOpenAI
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

from .utils import Response

load_dotenv()

TOKEN = os.environ["GITHUB_TOKEN"]
ENDPOINT = os.environ["ENDPOINT"]
MODEL_NAME = os.environ["MODEL_NAME"]


client = AsyncOpenAI(api_key=os.environ["GITHUB_TOKEN"], base_url=ENDPOINT)
model = OpenAIModel(MODEL_NAME, provider=OpenAIProvider(openai_client=client))


def init_agent(schema, tools):
    agent = Agent(
        model,
        system_prompt=f"""You are an AI agent whose job is to write the correct SQL for my analysis. return only SQL and nothing else.
        
        Example:
        User: What is the average temperature in Seattle?
        AI: SELECT AVG(temperature) FROM weather WHERE city = 'Seattle';

        HERE IS THE SCHEMA:
        {schema}
        """,
        tools=tools,
        output_type=Response,
    )

    return agent
