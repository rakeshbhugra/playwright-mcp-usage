from langgraph.graph import StateGraph, END
from .state import State
from .nodes import (
    reasoning_node,
    tool_use_node
) 
from typing import Optional
from src.utils.llm.message_helper import SystemMessage, HumanMessage
from langgraph.config import get_stream_writer
    
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
                "tool_use_node": "tool_use",
                END: END
            }
        )
        graph.add_edge("tool_use", "reasoning")

        return graph
        
        
    def _route_to_next_node(self, state: State) -> str:
        # Logic to determine the next node based on the state.
        if hasattr(state, 'next_node') and state.next_node:
            return state.next_node
        return END

    async def ainvoke(self, initial_state: State, **kwargs):
        """
        Invoke the graph and return the final state.
        
        Args:
            initial_state: The initial state to start with
            **kwargs: Additional arguments passed to graph.ainvoke
        """
        return await self.compiled_graph.ainvoke(initial_state, **kwargs)

    async def astream(self, initial_state: State, **kwargs):
        """
        Stream the graph execution.
        
        Args:
            initial_state: The initial state to start with
            **kwargs: Additional arguments passed to graph.astream
        """
        async for chunk in self.compiled_graph.astream(initial_state, **kwargs):
            yield chunk

    async def run_query(self, query: str, system_message: Optional[str] = None) -> State:
        """
        Convenience method to run a single query.
        
        Args:
            query: The user query
            system_message: Optional system message (defaults to standard assistant message)
        
        Returns:
            Final state after processing
        """
        system_msg = system_message or 'You are a helpful assistant that can answer questions and help with tasks.'
        messages = [
            SystemMessage(content=system_msg),
            HumanMessage(content=query)
        ]
        
        writer = get_stream_writer
        initial_state = State(messages=messages, writer=writer)
        
        return await self.ainvoke(initial_state)

playwright_graph = PlaywrightGraph()