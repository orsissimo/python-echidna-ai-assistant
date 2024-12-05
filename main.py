import os
from dotenv import load_dotenv
import anthropic
from ui import create_ui

def main():
    # Load environment variables from .env file
    load_dotenv()

    # Get API key from environment
    claude_api_key = os.getenv('CLAUDE_API_KEY')
    if not claude_api_key:
        raise ValueError("Claude API key is not set in the environment")

    # Initialize Claude client
    client = anthropic.Anthropic(api_key=claude_api_key)

    # Create output directory
    output_dir = "sandbox"
    os.makedirs(output_dir, exist_ok=True)

    # Launch UI
    demo = create_ui(client, output_dir)
    demo.launch(share=True)

if __name__ == "__main__":
    main()