from src.agent_graph.agent import PlaywrightAgent
import asyncio
from src.utils.read_resume import ResumeReader
from src.utils.get_prompt_with_resume_details import get_prompt

async def main():
    agent = PlaywrightAgent()
    history_messages = [
        {"role": "system", "content": "You are a helpful assistant."},
    ]

    resume_path = "data_files/resumes/Lin Mei_Experiened Level Software.pdf"
    resume_text = ResumeReader(resume_path).read_resume("pymupdf")

    user_message = get_prompt(resume_text)

    await agent.run(history_messages, user_message)


if __name__ == "__main__":
    asyncio.run(main())
