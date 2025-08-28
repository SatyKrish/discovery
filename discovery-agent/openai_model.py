import os
from dotenv import load_dotenv, find_dotenv
from langchain_openai import AzureChatOpenAI

# Load environment variables from both .env and .env.local if present,
# searching from the current working directory upward.
env_path = find_dotenv(filename=".env", usecwd=True)
if env_path:
        load_dotenv(env_path, override=False)

env_local_path = find_dotenv(filename=".env.local", usecwd=True)
if env_local_path:
        # Allow .env.local to override values from .env
        load_dotenv(env_local_path, override=True)


def get_default_model():
        """Return an Azure OpenAI chat model (AzureChatOpenAI only).

        Requires:
            - AZURE_OPENAI_ENDPOINT
            - AZURE_OPENAI_DEPLOYMENT
        Optional:
            - AZURE_OPENAI_API_KEY (if not using AAD)
            - AZURE_OPENAI_API_VERSION (default 2024-05-01-preview)
        """

        endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
        if not endpoint or not deployment:
                raise ValueError(
                        "Azure OpenAI required: set AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_DEPLOYMENT"
                )
        api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-05-01-preview")
        return AzureChatOpenAI(
                azure_deployment=deployment,
                api_version=api_version,
        )


# Convenient module-level instance
openai_model = get_default_model()

