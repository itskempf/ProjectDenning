"""
The Core Agent Class for Project Denning, using Hugging Face API.
"""
import yaml
import requests
import logging
import os
import sys
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.vector_db import VectorDB

load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Agent:
    """The main agent class for Project Denning, using Hugging Face API."""

    def __init__(self, config_path='config.yaml'):
        self._set_state("Initializing")
        try:
            with open(config_path, 'r') as f:
                self.config = yaml.safe_load(f)

            self.api_key = os.getenv("HUGGINGFACE_API_KEY")
            if not self.api_key:
                raise ValueError("HUGGINGFACE_API_KEY not found in .env file.")

            self.api_url = self.config.get("huggingface_api_url")
            self.headers = {"Authorization": f"Bearer {self.api_key}"}
            self.prompt_template = self.config.get('prompt_template', '')
            self.retrieval_results = self.config.get('retrieval_results', 5)

            if not self.prompt_template:
                raise ValueError("Prompt template is missing or invalid in config.yaml")

            self.vector_db = VectorDB(config_path)
            self._set_state("Idle")
        except Exception as e:
            logging.error(f"Failed to initialize Agent: {e}")
            self._set_state(f"Failed - {e}")
            raise

    def _set_state(self, new_state: str):
        self.state = new_state
        logging.info(f"Agent state: {self.state}")

    def get_status(self) -> str:
        return self.state

    def handle_query(self, user_question: str) -> str:
        if not user_question.strip():
            return "Please provide a valid question."

        self._set_state("Querying Database")
        retrieved_context = self.vector_db.query(user_question, n_results=self.retrieval_results)
        
        if not retrieved_context:
            self._set_state("Idle")
            return "I could not find relevant information in the legal database to answer your question."

        self._set_state("Constructing Prompt")
        context_str = "\n\n---\n\n".join(retrieved_context)
        
        try:
            formatted_prompt = self.prompt_template.format(context=context_str, question=user_question)
        except KeyError as e:
            self._set_state("Idle")
            logging.error(f"Prompt template in config.yaml is missing a key: {e}.")
            return "Error: The prompt template is misconfigured."

        self._set_state("Synthesizing Answer with LLM")
        try:
            response = requests.post(self.api_url, headers=self.headers, json={"inputs": formatted_prompt, "parameters": {"max_new_tokens": 512}})
            response.raise_for_status()
            
            result = response.json()
            full_answer = result[0].get('generated_text', '').strip()
            
            # The API returns the prompt AND the answer, so we trim the prompt off the start.
            final_answer = full_answer.replace(formatted_prompt, "").strip()

            if not final_answer:
                return "The language model returned an empty response."
            return final_answer
        except requests.RequestException as e:
            logging.error(f"Hugging Face API request error: {e}")
            return "Error: Could not connect to the Hugging Face API. Please check your connection and API key."
        except Exception as e:
            logging.error(f"Unexpected error during LLM communication: {e}")
            return "An unexpected error occurred while communicating with the language model."
        finally:
            self._set_state("Idle")
