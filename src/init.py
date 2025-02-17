import boto3, os
from botocore.exceptions import ClientError
from dotenv import load_dotenv


load_dotenv()


s3_client = boto3.client("s3")
s3_bucket = os.getenv("s3_bucket")
s3_key = os.getenv("s3_key")


try:
    env_vars = s3_client.get_object(
        Bucket=s3_bucket, Key="env_vars.json"
    )
    last_extract = env_vars["Body"].read().decode("utf-8")
    # log_message(__name__, 20, f"Extract function last ran at {last_extract}")
except s3_client.exceptions.NoSuchKey:
    last_extract = None
    # log_message(__name__, 20, "Extract function running for the first time")

s3_client.put_object(Bucket=s3_bucket, Key=s3_key, Body="extracted_json")
