from fastapi import HTTPException
from botocore.exceptions import ClientError
from config import AWS_S3_BUCKET, AWS_S3_KEY, AWS_S3_SECRET, AWS_S3_ZONE
import boto3

KB = 1024
MB = 1024 * KB
AWS_BUCKET = AWS_S3_BUCKET

session = boto3.Session(
    aws_access_key_id=AWS_S3_KEY,
    aws_secret_access_key=AWS_S3_SECRET,
)

s3 = session.resource('s3')

bucket = s3.Bucket(AWS_BUCKET)

client = boto3.client(
    's3',    
    aws_access_key_id=AWS_S3_KEY,
    aws_secret_access_key=AWS_S3_SECRET,
    region_name=AWS_S3_ZONE
)


async def s3_upload(contents: bytes, key: str, Content_Type:str = 'application/pdf'):
    #bucket.put_object(Key=key, Body=contents)
    bucket.put_object(Key=key, Body=contents, ACL='public-read', ContentDisposition='inline', ContentType=Content_Type)

def s3_download(key: str):
    try:
        url = client.generate_presigned_url(
        'get_object',
        Params = {'Bucket': f'{AWS_BUCKET}', 'Key': key},
        ExpiresIn = 3600
        )
        #return s3.Object(bucket_name=AWS_BUCKET, key=key).get()['Body'].read()
        return url
    except ClientError as err:
        raise HTTPException(status_code=502, detail=str(err))

def s3_delete(key:str):
    client.delete_object(Bucket = AWS_BUCKET, Key = key)