from src.agent_graph.agent import PlaywrightAgent
import asyncio
import os
from dotenv import load_dotenv
load_dotenv()

workday_email = os.getenv("WORKDAY_EMAIL")
workday_pass = os.getenv("WORKDAY_PASS")

prompt = f'''
open google.com, search for nvidia workday jobs, search for nvidia jobs
login with my email: {workday_email} with password: {workday_pass}, and apply for a job.
go to wd5.myworkdayjobs only after searching
'''

async def main():
    agent = PlaywrightAgent()
    history_messages = [
        {"role": "system", "content": "You are a helpful assistant."},
    ]
    user_message = prompt

    await agent.run(history_messages, user_message)


if __name__ == "__main__":
    asyncio.run(main())
