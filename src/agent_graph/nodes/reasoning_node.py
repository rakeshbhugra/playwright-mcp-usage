from ..state import State
from utils.llm.litellm_calls import LLMCall
from utils.llm.llm_models import llm_models

async def reasoning_node(state: State) -> State:
    # This node is responsible for reasoning and planning.
    llm = LLMCall(model=llm_models.OpenAIModels.gpt_4_1_mini, just_text=True)
    
    return state