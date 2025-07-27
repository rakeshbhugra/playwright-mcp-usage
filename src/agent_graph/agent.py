from .graph import playwright_graph
from src.utils.llm.message_helper import AnyMessage, HumanMessage
from .state import State
from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession
import asyncio

mcp_server_url = "http://localhost:8931/mcp"

class PlaywrightAgent:
    
    def __init__(self):
        return None

    async def run(self, history_messages: list[AnyMessage], user_message, **kwargs):
        try:
            async with streamablehttp_client(f"{mcp_server_url}") as (
                    read_stream,
                    write_stream,
                    _,
                ):

                async with ClientSession(read_stream, write_stream) as session:
                    
                    await session.initialize()

                    all_messages = history_messages + [HumanMessage(content=user_message)]
                    
                    init_state = State(messages=all_messages, writer=None, session=session)
                    response = playwright_graph.astream(init_state)

                    async for chunk in response:
                        # print(chunk)
                        pass

        except asyncio.CancelledError:
            print("Operation was cancelled.")
        except Exception as eg:
            print(f"TaskGroup exception occurred:")
            for exc in eg.exceptions:
                print(f"  {type(exc).__name__}: {exc}")
                import traceback
                traceback.print_exception(type(exc), exc, exc.__traceback__)
        except Exception as e:
            print(f"An error occurred: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    agent = PlaywrightAgent()
    history_messages = [
        {"role": "system", "content": "You are a helpful assistant."},
    ]
    user_message = "Open chrome and check weather in San Francisco today."
    
    asyncio.run(agent.run(history_messages, user_message)) 
