import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()


def get_default_model() -> ChatOpenAI:
    """Return a ChatOpenAI instance for DeepAgent."""
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    return ChatOpenAI(model=model, api_key=os.getenv("OPENAI_API_KEY"))


# Convenient module-level instance
openai_model = get_default_model()

