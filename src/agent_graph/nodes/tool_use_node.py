from ..state import State
from litellm import experimental_mcp_client
from src.utils.llm.message_helper import AnyMessage

async def tool_use_node(state: State) -> State:

    # This node is responsible for using tools.
    # Handle multiple tool calls if they exist
    if hasattr(state, 'openai_tools') and state.openai_tools:
        # Multiple tool calls
        for tool_call in state.openai_tools:
            call_result = await experimental_mcp_client.call_openai_tool(
                session=state.session,
                openai_tool=tool_call
            )
            
            state.messages.append(
                AnyMessage(
                    content=str(call_result.content[0].text),
                    role="tool",
                    tool_call_id=tool_call.id,
                )
            )
    else:
        # Single tool call (backward compatibility)
        call_result = await experimental_mcp_client.call_openai_tool(
            session=state.session,
            openai_tool=state.openai_tool
        )

        state.messages.append(
            AnyMessage(
                content=str(call_result.content[0].text),
                role="tool",
                tool_call_id=state.openai_tool.id,
            )
        )

    # print("MCP Tool Call Result:", call_result)

    return state
