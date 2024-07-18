import os
from dotenv import load_dotenv

load_dotenv()


class ConfigEnv:
    S3_INBOUND_PATH = os.getenv('S3_INBOUND_PATH')
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
    S3_REGION_NAME = os.getenv('S3_REGION_NAME')
    BEDROCK_REGION_NAME = os.getenv('BEDROCK_REGION_NAME')

    S3_HTML_CONTENT_PATH = os.getenv('S3_HTML_CONTENT_PATH')
    S3_HTML_METADATA_PATH = os.getenv('S3_HTML_METADATA_PATH')
    S3_HTML_IMAGES_PATH = os.getenv('S3_HTML_IMAGES_PATH')
    S3_HTML_PDF_PATH = os.getenv('S3_HTML_PDF_PATH')

    S3_OUTBOUND_PATH = os.getenv('S3_OUTBOUND_PATH')
    S3_STATUS_PATH = os.getenv('S3_STATUS_PATH')
    S3_OUTBOUND_REPORTS_PATH = os.getenv('S3_OUTBOUND_REPORTS_PATH')

    DATABASE_URL = os.getenv('DATABASE_URL')

    OPEN_AI_KEY = os.getenv('OPEN_AI_KEY')
    ANTHROPIC_AI_KEY = os.getenv('ANTHROPIC_AI_KEY')

    RAG_URL = os.getenv('RAG_URL')
    PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
    PINECONE_INDEX_NAME = os.getenv('PINECONE_INDEX_NAME')
    PINECONE_NAMESPACE = os.getenv('PINECONE_NAMESPACE')
    OPENAI_EMBEDDING_MODEL = os.getenv('OPENAI_EMBEDDING_MODEL')


        