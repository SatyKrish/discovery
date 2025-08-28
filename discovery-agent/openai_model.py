import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI

load_dotenv()


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

