import uuid

import boto3

from common.logging_util import get_std_logger
from config_env import ConfigEnv


class S3Connector:
    def __init__(self):
        self.logger = get_std_logger()
        try:
            self.s3_client = boto3.client(service_name='s3',
                                          region_name=ConfigEnv.S3_REGION_NAME,
                                          aws_access_key_id=ConfigEnv.AWS_ACCESS_KEY_ID,
                                          aws_secret_access_key=ConfigEnv.AWS_SECRET_ACCESS_KEY)
            self.logger.info("Connected to S3 successfully!")
        except Exception as e:
            self.logger.exception(e)
            raise Exception(f"Error connecting to S3: {e}")

    def read_file_contents(self, bucket_name: str, file_key: str) -> str:
        if self.s3_client:
            try:
                response = self.s3_client.get_object(Bucket=bucket_name, Key=file_key)
                file_content = response['Body'].read().decode('utf-8')
                return file_content
            except Exception as e:
                self.logger.exception(e)
                raise Exception(f"Error reading file from S3: {e}\n  Bucket: {bucket_name}, Key: {file_key}")
        else:
            self.logger.error("Not connected to S3. Call 'connect()' method first.")
            raise Exception("Not connected to S3. Call 'connect()' method first.")

    def download_file(self, bucket_name: str, file_key: str, filename: str) -> bool:
        if self.s3_client:
            try:
                self.logger.info(f"Downloading the file : {bucket_name}/{file_key}/{filename}")
                response = self.s3_client.get_object(Bucket=bucket_name, Key=f"{file_key}/{filename}")
                with open(filename, 'wb') as f:
                    f.write(response['Body'].read())
                self.logger.info("File writing completed")
                return True
            except Exception as e:
                self.logger.exception(e)
                raise Exception(
                    f"Error reading file from S3: {e}\n Bucket: {bucket_name}, Key: {file_key}, Filename: {filename}")
        else:
            self.logger.error("Not connected to S3. Call 'connect()' method first.")
            raise Exception("Not connected to S3. Call 'connect()' method first.")

    def read_pdf_file(self, bucket_name: str, file_path: str) -> bytes:
        if self.s3_client:
            try:
                pdf_file = self.s3_client.get_object(Bucket=bucket_name, Key=file_path)['Body'].read()
                return pdf_file
            except Exception as e:
                self.logger.exception(e)
                raise Exception(f"Error reading file from S3: {e}\n Bucket: {bucket_name}, Key: {file_path}")
        else:
            self.logger.error("Not connected to S3. Call 'connect()' method first.")
            raise Exception("Not connected to S3. Call 'connect()' method first.")

    def upload_file_to_s3(self, file_path: str, bucket_name: str, object_name: str) -> bool:
        if self.s3_client:
            try:
                # Upload the file
                self.s3_client.upload_file(Filename=file_path, Bucket=bucket_name, Key=object_name)
                self.logger.info("File uploaded successfully.")
                return True
            except Exception as e:
                self.logger.error(f"Error uploading file to S3: {e}")
                raise Exception(f"Error uploading file to S3: {e}")
        else:
            self.logger.error("Not connected to S3.")

    def upload_file_to_s3_public_bucket(self, file_path: str, bucket_name: str) -> str:
        bucket_name = 'reports-agalya-test'
        if self.s3_client:
            # Generate a unique filename using UUID
            unique_filename = str(uuid.uuid4()) + ".pdf"
            try:
                # Upload the file to S3 with public-read ACL
                self.s3_client.upload_file(
                    file_path,
                    bucket_name,
                    unique_filename,
                    ExtraArgs={'ACL': 'public-read'}
                )

                # Generate the public URL for the uploaded file
                s3_url = f"https://{bucket_name}.s3.amazonaws.com/{unique_filename}"
                print(f"s3_url = {s3_url}")
                return s3_url
            except Exception as e:
                print(f"Error uploading file: {e}")
                return None
        else:
            self.logger.error("Not connected to S3.")

    def upload_file_to_s3_and_create_presigned_url(self, file_path: str, bucket_name: str, object_name: str) -> str:
        if self.s3_client:
            # Upload the file and Generate a presigned URL for the S3 object
            try:
                # Upload the file
                self.s3_client.upload_file(Filename=file_path, Bucket=bucket_name, Key=object_name)
                self.logger.info("File uploaded successfully.")
                return self.create_presigned_url(bucket_name=bucket_name, object_name=object_name)
            except Exception as e:
                print(f"Error uploading file: {e}")
                return None
        else:
            self.logger.error("Not connected to S3.")

    def create_presigned_url(self, bucket_name: str, object_name: str) -> str:
        if self.s3_client:
            # 6 hrs in seconds, url valid for 6 hrs
            expiration_in_seconds = 21600

            # Generate a presigned URL for the S3 object
            try:
                # note that we are passing get_object as the operation to perform
                response = self.s3_client.generate_presigned_url('get_object',
                                                                 Params={
                                                                     'Bucket': bucket_name,
                                                                     'Key': object_name
                                                                 },
                                                                 ExpiresIn=expiration_in_seconds)
                self.logger.info("Generate presigned url - Completed")
                return response
            except Exception as e:
                print(f"Error create_presigned_url: {e}")
                return None
        else:
            self.logger.error("Not connected to S3.")

    def list_objects(self, s3_bucket_name: str, s3_inbound_path: str) -> dict:
        if self.s3_client:
            try:
                response = self.s3_client.list_objects(Bucket=s3_bucket_name, Prefix=s3_inbound_path)
                self.logger.info("list objects successful.")
                return response
            except Exception as e:
                self.logger.error(f"Error list_objects in S3: {e}")
                raise Exception(f"Error list_objects in S3: {e}")
        else:
            self.logger.error("Not connected to S3.")

    def get_object(self, s3_bucket_name: str, file_key: str):
        if self.s3_client:
            try:
                response = self.s3_client.get_object(Bucket=s3_bucket_name, Key=file_key)
                self.logger.info("get s3 object successful.")
                return response
            except Exception as e:
                self.logger.error(f"Error get_object in S3: {e}")
                raise Exception(f"Error get_object in S3: {e}")
        else:
            self.logger.error("Not connected to S3.")

    def put_object(self, s3_bucket_name: str, new_file_key: str, processed_data: str):
        if self.s3_client:
            try:
                response = self.s3_client.put_object(Bucket=s3_bucket_name, Key=new_file_key, Body=processed_data)
                self.logger.info("put s3 object successful.")
                return response
            except Exception as e:
                self.logger.error(f"Error put_object in S3: {e}")
                raise Exception(f"Error put_object in S3: {e}")
        else:
            self.logger.error("Not connected to S3.")

    def delete_object(self, s3_bucket_name: str, file_key: str):
        if self.s3_client:
            try:
                response = self.s3_client.delete_object(Bucket=s3_bucket_name, Key=file_key)
                self.logger.info("delete s3 object successful.")
                return response
            except Exception as e:
                self.logger.error(f"Error delete_object in S3: {e}")
                raise Exception(f"Error delete_object in S3: {e}")
        else:
            self.logger.error("Not connected to S3.")
