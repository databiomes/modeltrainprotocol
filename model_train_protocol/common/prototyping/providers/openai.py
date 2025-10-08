import json
import os

import requests
from dotenv import load_dotenv

from model_train_protocol.common.prototyping.utils import add_token_attributes
from model_train_protocol.common.pydantic.prototyping import GenerateMTPPrototypeModel, GENERATE_MTP_TOOL


def generate_mtp_prototype_file(prompt_id: str, openai_api_key: str | None = None) -> GenerateMTPPrototypeModel:
    """
    Calls the OpenAI API to run the generate_mtp tool based on the provided prompt ID.
    :return: The parsed function output as a GenerateMTPPrototypeModel object, which can be converted into a ProtocolFile.
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

    print("Generating MTP prototype via OpenAI...")
    response = requests.post("https://api.openai.com/v1/responses", headers=headers, json=data)

    try:
        response.raise_for_status()
        response_json: dict = response.json()

        try:
            # prototype_mtp: GenerateMTPPrototypeModel = GenerateMTPPrototypeModel(
            #     **json.loads(response_json['output'][1]['arguments'])
            # )
            prototype_model_json: dict = json.loads(response_json['output'][1]['arguments'])

            # Add key and special fields to tokens
            prototype_model_json: dict = add_token_attributes(prototype_model_json=prototype_model_json)

            return GenerateMTPPrototypeModel(**prototype_model_json)

        except (KeyError, IndexError, json.JSONDecodeError) as e:
            raise ValueError("Failed to parse function output from response.") from e

    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error {response.status_code}: {e}")
        print(f"Response body: {response.text}")
        raise e
    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the request: {e}")
        raise e
