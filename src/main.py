import litellm

resepose = litellm.completion(
    model="gpt-4.1-mini",
    messages=[
        {'role': 'system', 'content': 'You are a helpful assistant.'},
        {'role': 'user', 'content': 'What is the capital of France?'}
    ]
)

print(resepose['choices'][0]['message']['content'])