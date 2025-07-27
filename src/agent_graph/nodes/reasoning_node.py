from ..state import State
from src.utils.llm.litellm_calls import LLMCall
from src.utils.llm.llm_models import llm_models
from litellm import experimental_mcp_client
import copy
import json
from .node_names import NodeNames
from src.utils.llm.message_helper import AIMessage

prompt = f'''
You are a helpful assistant that can answer questions and help with tasks. You can control chrome browser using playwright tools.
'''

async def reasoning_node(state: State) -> State:

    # writer = state.writer()
    llm = LLMCall(model=llm_models.OpenAIModels.gpt_4_1_mini, just_text=False)
    tools = await experimental_mcp_client.load_mcp_tools(session=state.session, format="openai")

    messages_copy = copy.deepcopy(state.messages)
    messages_copy[0]['content'] = prompt 

    llm_response = await llm.completion_call(
        messages=messages_copy, 
        tools=tools, 
    )

    # print("llm_response:", json.dumps(llm_response, indent=2, default=str))

    tool_calls = llm_response["choices"][0]["message"].get("tool_calls")
    
    if tool_calls and len(tool_calls) > 0:
        # Append the full assistant message with all tool calls
        state.messages.append(llm_response["choices"][0]["message"])
        
        # Pass all tool calls to the tool_use_node
        if len(tool_calls) > 1:
            state.openai_tools = tool_calls
            state.openai_tool = None  # Clear single tool for clarity
        else:
            state.openai_tool = tool_calls[0]
            state.openai_tools = None  # Clear multiple tools for clarity
            
        state.next_node = NodeNames.TOOL_USE_NODE
    else:
        content = llm_response["choices"][0]["message"]["content"]
        state.messages.append(AIMessage(content=content))
        state.openai_tool = None
        state.openai_tools = None
        state.next_node = NodeNames.END
        
        print('\n\nFinal response from LLM:', state.messages[-1]['content'])
        
    return state
