from ..state import State

async def tool_use_node(state: State) -> State:
    # This node is responsible for using tools.
    return state