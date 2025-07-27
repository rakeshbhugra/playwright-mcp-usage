def AIMessage(content):
    return {'role': 'assistant', 'content': content}

def SystemMessage(content):
    return {'role': 'system', 'content': content}

def HumanMessage(content):
    return {'role': 'user', 'content': content}

def AnyMessage(content, role, **kwargs):
    return {'role': role, 'content': content, **kwargs}