import requests
from config import config

class N8nClient:
    """
    A client to interact with the n8n webhook.
    """
    def __init__(self, webhook_url: str):
        if not webhook_url:
            raise ValueError("Webhook URL cannot be empty.")
        self.webhook_url = webhook_url

    def send_prompt(self, prompt: str, author_id: int, author_name: str) -> dict:
        """
        Sends a prompt to the n8n workflow and returns the response.
        """
        payload = {
            'prompt': prompt,
            'author_id': author_id,
            'author_name': author_name
        }
        
        try:
            response = requests.post(self.webhook_url, json=payload, timeout=300)
            response.raise_for_status()
            
            try:
                return response.json()
            except requests.exceptions.JSONDecodeError:
                return {'response': "Received a non-JSON response from the workflow."}

        except requests.exceptions.RequestException as e:
            print(f'Error connecting to n8n webhook: {e}')
            return {'response': 'Sorry, I couldn\'t connect to the AI workflow. Please try again later.'}

# Create a single instance of the N8nClient.
n8n_client = N8nClient(webhook_url=config.N8N_WEBHOOK_URL)
