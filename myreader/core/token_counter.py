import tiktoken

def count_string_tokens(string: str, model_name: str = "gpt-3.5-turbo-0301") -> int:
    
    encoding = tiktoken.encoding_for_model(model_name)
    return len(encoding.encode(string))
