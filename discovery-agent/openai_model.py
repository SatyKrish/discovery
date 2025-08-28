import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, AzureChatOpenAI

load_dotenv()


def get_default_model():
    """Return an OpenAI-compatible chat model.

    If ``AZURE_OPENAI_ENDPOINT`` is set, use Azure OpenAI via ``AzureChatOpenAI``.
    Otherwise, default to ``ChatOpenAI`` with ``OPENAI_MODEL``/``OPENAI_API_KEY``.
    """

    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    if azure_endpoint:
        # Azure OpenAI configuration
        deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
        if not deployment:
            raise ValueError(
                "AZURE_OPENAI_ENDPOINT is set, but AZURE_OPENAI_DEPLOYMENT is missing."
            )
        api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-05-01-preview")
        # API key is optional if using keyless/AAD, but supported if provided
        # AZURE_OPENAI_API_KEY and AZURE_OPENAI_ENDPOINT are read from env by the SDK
        return AzureChatOpenAI(
            azure_deployment=deployment,
            api_version=api_version,
            # 'model' is used for tracing/token counting only in Azure context
            model=os.getenv("OPENAI_MODEL", None),
        )

    # Fallback: public OpenAI
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    return ChatOpenAI(model=model, api_key=os.getenv("OPENAI_API_KEY"))


# Convenient module-level instance
openai_model = get_default_model()

