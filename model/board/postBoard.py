import uuid
import boto3
from botocore.exceptions import ClientError
import logging
from model.StatusModel import Status
import os

def post_board(myDB,content,file):
    # 產生序號
    uid = uuid.uuid4().hex
    # aws s3 設置
    s3_client = boto3.client('s3')
    # 指定 s3 bucket
    bucket = "tdt-bucket"
    # 上傳檔案
    try:
        response = s3_client.upload_fileobj(file.file, bucket, uid)
        print(response)
    except ClientError as e:
        print(e)
        logging.error(e)
        return Status(status_code=1)
    # 更新資料庫
    sql="INSERT INTO board (message,image) VALUES (%s,%s)"
    val=(content,uid)
    result = myDB.insert(sql,val)
    if result == 1:
        return Status(status_code=0)
    else:
        return Status(status_code=2)