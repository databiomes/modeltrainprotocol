import os

import requests
from dotenv import load_dotenv

from model_train_protocol.common.pydantic.prototyping import PrototypeModel


def get_openai_response(prompt_id: str, version: str = "1") -> PrototypeModel:
    load_dotenv()
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("Error: OPENAI_API_KEY environment variable not set.")

    url = "https://api.openai.com/v1/responses"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}"
    }

    data = {
        "prompt": {
            "id": prompt_id,
            "version": version
        },
        "tools": [
            {
                "type": "function",
                "function": {
                    "name": "generate_mtp",
                    "arguments": {}
                }
            }
        ]

    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        response_json: dict = response.json()
        return PrototypeModel(**response_json)

    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error {response.status_code}: {e}")
        print(f"Response body: {response.text}")
        raise e
    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the request: {e}")
        raise e