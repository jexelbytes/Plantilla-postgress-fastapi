from dotenv import load_dotenv
import os
import json

load_dotenv()

# SERVER
host = os.getenv("HOST")
port = int(os.getenv("PORT"))
dev_key = os.getenv("DEV_KEY")

# DATABASE
db_name = os.getenv("DATABASE_NAME")
db_type = os.getenv("DATABASE_TYPE")
db_user = os.getenv("DATABASE_USER")
db_pass = os.getenv("DATABASE_PASS")
db_host = os.getenv("DBHOST")
db_port = os.getenv("DBPORT")

# SWAGGER
SWAGGER_USER=os.getenv('SWAGGER_USER')
SWAGGER_PASS=os.getenv('SWAGGER_PASS')

is_develop = (str(os.getenv("IS_DEVELOP")).lower() in ('true', '1'))

summary = """Basic openapi schema."""
title = "FastAPI - Postgres"
description = """
### Simple FastAPI API?
"""

swagger_config = {
    "syntaxHighlight.theme": "nord",
    "persistAuthorization": True,
    "tryItOutEnabled":True,
    "docExpansion": "none",
    "displayRequestDuration":True,
    "filter":True,
}

# GOOGLE CREDENTIALS
GOOGLE_OAUTH2_CLIENT_SECRET = os.getenv("GOOGLE_OAUTH2_CLIENT_SECRET")
GOOGLE_OAUTH2_CLIENT_ID = os.getenv("GOOGLE_OAUTH2_CLIENT_ID")
REDIRECT_URI = os.getenv("REDIRECT_URI")

# AWS CREDENTIALS
AWS_S3_BUCKET = os.getenv('AWS_S3_BUCKET')
AWS_S3_KEY = os.getenv('AWS_S3_KEY')
AWS_S3_SECRET = os.getenv('AWS_S3_SECRET')
AWS_S3_ZONE = os.getenv('AWS_S3_ZONE')

# EMAIL CREDENTIALS
EMAIL = os.getenv("EMAIL")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_PORT = int(os.getenv("EMAIL_PORT"))
EMAIL_HOST = os.getenv("EMAIL_HOST")

# JWT
JWT_SECRET = os.getenv('JWT_SECRET')
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM')
JWT_EXPIRE_TIME = float(os.getenv('JWT_EXPIRE_TIME'))
JWT_REFRESH_EXPIRE_TIME = float(os.getenv('JWT_REFRESH_EXPIRE_TIME'))