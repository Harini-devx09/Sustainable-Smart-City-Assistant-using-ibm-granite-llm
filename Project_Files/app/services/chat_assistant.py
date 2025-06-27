from app.services.granite_llm import ask_granite

def ask_city_assistant(prompt: str) -> str:
    """
    Wraps Watsonx Granite LLM call to handle prompt-based queries.
    """
    return ask_granite(prompt)
