from ..state import State
from litellm import experimental_mcp_client

async def tool_use_node(state: State) -> State:

    # This node is responsible for using tools.
    call_result = await experimental_mcp_client.call_openai_tool(
        session=state.session,
        openai_tool=state.openai_tool
    )

    print("MCP Tool Call Result:", call_result)

    return state
