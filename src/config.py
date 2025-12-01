import os
from cerebras.cloud.sdk import Cerebras
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_client():
    """Initialize and return the Cerebras client."""
    api_key = os.environ.get("CEREBRAS_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "CEREBRAS_API_KEY not set. Please check your .env file."
        )
    return Cerebras(api_key=api_key)

# Default model to use
DEFAULT_MODEL = "llama-3.3-70b"
