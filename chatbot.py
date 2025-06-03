import os
import asyncio
from agents import Agent, Runner, OpenAIChatCompletionsModel
import chainlit as cl
from openai import AsyncOpenAI
from dotenv import load_dotenv
from agents.run import RunConfig
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
gemini_api_url = os.getenv("GEMINI_API_URL")
gemini_api_model = os.getenv("GEMINI_API_MODEL")


if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set.")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url=gemini_api_url,
)

model = OpenAIChatCompletionsModel(
    openai_client=external_client,
    model='gemini-2.0-flash',
    
)


config =  RunConfig(
    model=model,
    tracing_disabled=True,
) 


ag: Agent = Agent(
    name="Metalog AI",
    instructions="An Agent who is a helpful assistant.",
    model=model,
      
)

@cl.on_chat_start
async def on_chat_start():
    await cl.Message(
        content="Hello Friend!  Metalog is here to assist you. Ask me anything"
    ).send()

@cl.on_message
async def main(message: cl.Message):
    result = Runner.run_sync(
        ag,
        input=message.content,
        run_config=config,
    )

    msg = cl.Message(content="")
    await msg.send()

    for char in result.final_output:
        msg.content += char
        await msg.update()
        await asyncio.sleep(0.02)  # Adjust the speed of typing effect
                     
