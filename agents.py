from dataclasses import dataclass
from typing import Optional
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModelSettings, OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic import BaseModel, Field
import openai

from settings import Settings


settings = Settings()

# Cerebras Model Definition
cerebras_openai_settings = OpenAIModelSettings(
    temperature=0.7,
    top_p=0.95,
    frequency_penalty=0,
)

cerebras_model_name = "llama-3.3-70b"

cerebras_client = openai.AsyncOpenAI(api_key=settings.cerebras_api_key, base_url=settings.cerebras_base_url)

cerebras_model = OpenAIModel(
    model_name=cerebras_model_name,
    provider=OpenAIProvider(openai_client=cerebras_client),
)

class ArgumentOutcome(BaseModel):
    winner: str = Field(description="Who won the argument round: 'player' or 'enemy'.")
    reasoning: str = Field(description="Brief explanation for the decision.")
    damage_to_player: int = Field(description="How many hearts the player loses (0 if player won).")
    damage_to_enemy: int = Field(description="How many hearts the enemy loses (0 if enemy won).")
    special_effect_triggered: Optional[str] = Field(description="Description of any special mechanic triggered this round, if any.", default=None)

@dataclass
class Deps:
    pass


with open("prompts/judge_agent_prompt.txt", "r") as file:
    judge_agent_prompt = file.read()

with open("prompts/yapper_agent_prompt.txt", "r") as file:
    yapper_agent_prompt = file.read()

with open("prompts/kevin&karen_agent_prompt.txt", "r") as file:
    kevin_and_karen_agent_prompt = file.read()

with open("prompts/cynic_agent_prompt.txt", "r") as file:
    cynic_agent_prompt = file.read()

with open("prompts/nietzsche_agent_prompt.txt", "r") as file:
    nietzsche_agent_prompt = file.read()


judge_agent = Agent(
    model=cerebras_model,
    model_settings=cerebras_openai_settings,
    system_prompt=judge_agent_prompt,
    retries=3,
    result_type=ArgumentOutcome
)

yapper_agent = Agent(
    model=cerebras_model,
    model_settings=cerebras_openai_settings,
    system_prompt=yapper_agent_prompt,
    retries=3,
)

kevin_and_karen_agent = Agent(
    model=cerebras_model,
    model_settings=cerebras_openai_settings,
    system_prompt=kevin_and_karen_agent_prompt,
    retries=3,
)

cynic_agent = Agent(
    model=cerebras_model,
    model_settings=cerebras_openai_settings,
    system_prompt=cynic_agent_prompt,
    retries=3,
)

nietzsche_agent = Agent(
    model=cerebras_model,
    model_settings=cerebras_openai_settings,
    system_prompt=nietzsche_agent_prompt,
    retries=3,
)


if __name__ == "__main__":
    pass