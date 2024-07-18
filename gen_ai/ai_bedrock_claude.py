import boto3, json

from common.logging_util import get_std_logger
from config_env import ConfigEnv

DEFAULT_SYSTEM_MESSAGE = "You are a helpful AI assistant. You strive to be factual and accurate."
ACCEPT = 'application/json'
CONTENT_TYPE = 'application/json'

class AIBedrockClaude:
    amazon_models = ['anthropic.claude-3-haiku-20240307-v1:0:48k',
                     'anthropic.claude-3-haiku-20240307-v1:0:200k',
                     'anthropic.claude-3-haiku-20240307-v1:0']

    def __init__(self):
        self.logger = get_std_logger()
        try:
            self.bedrock_client = boto3.client('bedrock-runtime', region_name=ConfigEnv.BEDROCK_REGION_NAME)
            self.logger.info("Connected to bedrock client")
        except Exception as e:
            self.logger.exception(e)
            raise Exception(f"Error connecting to Bedrock clients: {e}")

    def generate_text(self, model_id: str, prompt: str, system_msg: str = DEFAULT_SYSTEM_MESSAGE, 
                      max_tokens: int = 8000) -> str:
        if model_id not in self.amazon_models:
            raise ValueError(f"Model name {model_id} not found in list of available models")

        message = self.__generate_message(prompt)
        body = self.__create_body(message=message, system_msg=system_msg, max_tokens=max_tokens)

        try:
            response = self.bedrock_client.invoke_model(body=body, modelId=model_id, accept=ACCEPT, 
                                                        contentType=CONTENT_TYPE)
            output = self.__extract_response(response)
            return output
        except Exception as e:
            self.logger.exception(e)
            return f"Error occurred: {str(e)}"
        
    ##########
    # Private helper functions
    ##########

    def __create_body(self, message: str, system_msg: str, max_tokens: int) -> str:
        return json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "system": system_msg,
            "messages": message,
            "max_tokens": max_tokens,
            "temperature": 0.1,
            "top_p": 0.9,
        })

    def __generate_message(self, user_msg: str):
        return [{"role": "user", "content": [{"type": "text", "text": user_msg}]}]
    
    def __extract_response(self, result):
        try:
            json_result = json.loads(result.get('body').read())
            return json_result.get('content')[0].get('text')
        except Exception as e:
            self.logger.error(f"Failed to parse the results {e}")
            return None