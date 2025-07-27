from langgraph.graph import StateGraph, END
from .state import State
from .nodes import (
    reasoning_node,
    tool_use_node
) 
    
class PlaywrightGraph:
    
    def __init__(self):
        self.graph = self._build_graph()
        self.compiled_graph = self.graph.compile()


    def _build_graph(self):
        graph = StateGraph(State)

        # Add nodes
        graph.add_node("reasoning", reasoning_node)
        graph.add_node("tool_use", tool_use_node)

        # Set entry point
        graph.set_entry_point("reasoning")
        
        # Add edges
        graph.add_conditional_edges(
            "reasoning",
            self._route_to_next_node,
            {
                "tool_use": "tool_use",
                END: END
            }
        )
        graph.add_edge("tool_use", "reasoning")
        
        
    async def _route_to_next_node(state: State) -> str:
        # Logic to determine the next node based on the state.
        # TODO: will implement this later.
        # This node routes to the next appropriate node based on the state.
        next_node = END
        return next_node

    async def ainvoke(self, initial_state: State, **kwargs):
        """
        Invoke the graph and return the final state.
        
        Args:
            initial_state: The initial state to start with
            **kwargs: Additional arguments passed to graph.ainvoke
        """
        return await self.compiled_graph.ainvoke(initial_state, **kwargs)
