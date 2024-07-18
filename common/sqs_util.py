import boto3

from common.logging_util import get_std_logger


class SQSHandler:
    def __init__(self):
        self.logger = get_std_logger()
        try:
            self.sqs_client = boto3.client(service_name='sqs')
            self.logger.info("Connected to SQS successfully!")
        except Exception as e:
            self.logger.exception(e)
            raise Exception(f"Error connecting to SQS: {e}")

    def send_sqs_message(self, queue_url: str, msg: str, msg_group_id: str, msg_dededupe_id: str) -> str:
        try:
            response = self.sqs_client.send_message(QueueUrl=queue_url,
                                                    MessageBody=msg,
                                                    MessageGroupId=msg_group_id,
                                                    MessageDeduplicationId=msg_dededupe_id)
            return response['MessageId']
        except Exception as e:
            self.logger.exception(e)
            raise Exception(f"Error during send_sqs_message for queue - {queue_url}: {e}")
