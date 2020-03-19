from pathlib import Path
from bank_microservice.src import S3Bucket

file_path = str(Path(__file__).resolve().parents[0]) + "/test.json"

s3_bucket = S3Bucket()
s3_bucket.upload_file(file_path=file_path)
