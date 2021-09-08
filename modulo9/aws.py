#%%
import boto3
from botocore import exceptions
from botocore.exceptions import ClientError
import logging
from botocore.retries import bucket
from dotenv import load_dotenv
from os import getenv

# %%
load_dotenv("C:/Users/Distrito/_distrito/bootcamp/.env",encoding='utf8')

#%%
s3_client = boto3.client(
    's3',
    aws_access_key_id=getenv('AWS_ID'),
    aws_secret_access_key=getenv('AWS_KEY')
)

# %%
def criar_bucket(nome):
    try:
        s3_client.create_bucket(Bucket=nome)
    except ClientError as e:
        logging.error(e)
        return False
    return True

# %%
criar_bucket('vinicius-aws-teste-duke')

# %%
def deletar_bucket(nome):
    try:
        s3_client.delete_bucket(Bucket=nome)
    except ClientError as e:
        logging.error(e)
        return False
    return True

# %%
deletar_bucket('vinicius-aws-teste-duke')

# %%
