class LLMModels:
    class OllamaModels:
        dolphin = 'ollama/dolphin3:latest'
        deepseek = 'ollama/deepseek-r1:14b'
        deepseek_uncensored = 'ollama/huihui_ai/deepseek-r1-abliterated'
        qwen3 = 'ollama/qwen3'
        gemma3 = 'ollama/gemma3'
        llama3 = 'ollama/llama3'
        gemma2_2b = 'ollama/gemma2:2b'
        llama3_function_support = 'ollama/smangrul/llama-3-8b-instruct-function-calling'

    class OpenAIModels:
        gpt4 = 'gpt-4'
        gpt35 = 'gpt-3.5-turbo'
        gpt35_16k = 'gpt-3.5-turbo-16k'
        gpt_4_1_mini = 'gpt-4.1-mini'


llm_models = LLMModels()
