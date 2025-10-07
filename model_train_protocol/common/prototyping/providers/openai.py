import json
import os

import requests
from dotenv import load_dotenv

from model_train_protocol.common.pydantic.prototyping import GenerateMTPResultModel, GENERATE_MTP_TOOL

def get_generate_mtp(prompt_id: str, openai_api_key: str | None = None) -> GenerateMTPResultModel:
    """
    Calls the OpenAI API to run the generate_mtp tool based on the provided prompt ID.
    :return: The parsed function input as a GenerateMTPFunctionInput object.
    """
    if not openai_api_key:
        load_dotenv()
        openai_api_key = os.environ.get("OPENAI_API_KEY")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}"
    }

    data = {
        "prompt": {
            "id": prompt_id
        },
        "input": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": "run generate_mtp()"
                    }
                ]
            }
        ],
        "tools": [GENERATE_MTP_TOOL]
    }

    response = requests.post("https://api.openai.com/v1/responses", headers=headers, json=data)

    try:
        response.raise_for_status()
        response_json: dict = response.json()

        try:
            prototype_mtp: GenerateMTPResultModel = GenerateMTPResultModel(
                **json.loads(response_json['output'][1]['arguments'])
            )

        except (KeyError, IndexError, json.JSONDecodeError) as e:
            raise ValueError("Failed to parse function output from response.") from e
        return prototype_mtp

    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error {response.status_code}: {e}")
        print(f"Response body: {response.text}")
        raise e
    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the request: {e}")
        raise e
