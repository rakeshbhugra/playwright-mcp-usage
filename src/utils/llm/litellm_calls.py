from litellm import acompletion
import traceback
import asyncio

class LLMCall:
    '''
    A class to handle LLM (Large Language Model) API calls using LiteLLM.
    
    This class provides methods to make both regular and streaming completions to various LLM models
    supported by LiteLLM, including Ollama and OpenAI models.
    
    Attributes:
        model (str): The LLM model to use for completions (e.g., 'ollama/deepseek-r1:14b')
        just_text (bool): If True, returns only the text content of the response. If False, returns the full response object.
    
    Example:
        ```python
        # Initialize with a model and just_text flag
        llm = LLMCall(model=llm_models.OllamaModels.deepseek, just_text=True)
        
        # Make a regular completion call
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What is the capital of France?"}
        ]
        response = await llm.completion_call(messages)
        print(response)  # Prints: "The capital of France is Paris."
        
        # Make a streaming completion call
        async for chunk in await llm.completion_call(messages, stream=True):
            print(chunk, end='', flush=True)
        ```
    '''
    
    def __init__(self, model: str, just_text: bool) -> None:
        self.just_text = just_text
        self.model = model

    async def completion_call(
        self,
        messages,
        stream = False,
        temperature = 0,
        tools = None,
        response_format = None
    ):
        try:
            # if stream and self.just_text:
            #     raise ValueError("Stream and just text can't be passed together")

            for idx, message in enumerate(messages):
                if type(message) != dict:
                    messages[idx] = dict(message)

            completion_kwargs = {
                'model': self.model,
                'messages': messages,
                'stream': stream,
                'temperature': temperature
            }
            if tools is not None:
                completion_kwargs['tools'] = tools
            if response_format is not None:
                completion_kwargs['response_format'] = response_format
            
            response = await acompletion(**completion_kwargs)
            if response is None:
                raise Exception("No response received from the model")

            # if response.choices[0].finish_reason == "tool_calls":
            #     tool_calls = []
            #     for tool_call in response.choices[0].message.tool_calls:
            #         tool_calls.append(tool_call)
            #     return {'tool_calls': tool_calls}

            if self.just_text:
                if stream == False:
                    return response.choices[0].message.content
                
                async def stream_generator():
                    try:
                        async for chunk in response:
                            delta = chunk.choices[0].delta
                            try:
                                # Check if chunk has the expected structure
                                if getattr(delta, "tool_calls", None):
                                    yield delta.tool_calls[0]
                                elif getattr(delta, "content", None):
                                    yield delta
                                else:
                                    yield delta
                            except (AttributeError, IndexError) as e:
                                # Log and skip malformed chunks
                                print(f"Skipping malformed chunk: {e}")
                                continue
                    except asyncio.CancelledError:
                        # Handle graceful cancellation
                        print("Stream was cancelled")
                        return  # Exit the generator gracefully
                    except Exception as e:
                        # Handle other exceptions
                        print(f"Error in stream generator: {traceback.format_exc()}")
                        return  # Exit the generator
                
                return stream_generator()
                    
            return response
            
        except Exception as e:
            print(f"error occurred: {traceback.format_exc()}")
            raise e

    async def tool_call(
        self,
        system_prompt,
        user_prompt,
        stream=False
    ):
        messages = [
            {'content': system_prompt, 'role': 'system'},
            {'content': user_prompt, 'role': 'user'}
        ]
        
        response = await self.completion_call(messages, stream)
        return response