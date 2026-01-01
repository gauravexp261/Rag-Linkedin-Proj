"""
Main script for running the Icebreaker Bot (CLI version)
"""

import sys
import time
import logging
import argparse

from modules.data_extraction import extract_linkedin_profile
from modules.data_preprocessing import split_profile_data, create_retriever
from modules.query_engine import generate_initial_facts, answer_question
import config

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger(__name__)

def chatbot_interface(retriever):
    print("\nYou can now ask questions. Type 'exit' to quit.\n")

    while True:
        user_query = input("You: ")

        if user_query.lower() in ["exit", "quit", "bye"]:
            print("Bot: Goodbye!")
            break

        print("Bot is typing...", end="")
        sys.stdout.flush()
        time.sleep(1)
        print("\r", end="")

        response = answer_question(retriever, user_query)
        print(f"Bot: {response}\n")

def process_linkedin(linkedin_url, api_key=None, mock=False):
    try:
        profile_data = extract_linkedin_profile(
            linkedin_url,
            api_key=api_key,
            mock=mock
        )

        if not profile_data:
            logger.error("Failed to retrieve profile data")
            return

        chunks = split_profile_data(profile_data)
        retriever = create_retriever(chunks)

        print("\n--- 3 Interesting Facts ---")
        facts = generate_initial_facts(retriever)
        print(facts)

        chatbot_interface(retriever)

    except Exception as e:
        logger.error(f"Error occurred: {e}")

def main():
    parser = argparse.ArgumentParser(description="LinkedIn Icebreaker Bot")
    parser.add_argument("--url", type=str, help="LinkedIn profile URL")
    parser.add_argument("--api-key", type=str, help="ProxyCurl API key")
    parser.add_argument("--mock", action="store_true", help="Use mock data")

    args = parser.parse_args()

    linkedin_url = args.url or ""
    use_mock = args.mock or not linkedin_url
    api_key = args.api_key or config.PROXYCURL_API_KEY

    if use_mock and not linkedin_url:
        linkedin_url = "https://www.linkedin.com/in/dummy/"

    process_linkedin(
        linkedin_url=linkedin_url,
        api_key=api_key,
        mock=use_mock
    )

if __name__ == "__main__":
    main()
