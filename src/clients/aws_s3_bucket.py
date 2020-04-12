import boto3
from boto3.s3.transfer import S3Transfer
from env_var_handler.env_var_loader import load_credentials, load_config
import os


class S3Bucket:
    """Class for AWS S3 Bucket.
    """

    def __init__(self):
        """Creates instance of the class with the client authorized by AWS env_var_handler.
        """
        # load credentials and configs as env variables
        load_credentials(), load_config()
        self.access_key = os.getenv("aws_s3_access_key")
        self.access_secret_key = os.getenv("aws_s3_access_secret_key")
        self.bucket_name = os.getenv("aws_s3_bucket_name")
        self.client = self._build_client()

    def _build_client(self):
        """Build S3 Bucket client.
        Return:
            S3 Client authenticated
        """
        return boto3.client('s3',
                            aws_access_key_id=self.access_key,
                            aws_secret_access_key=self.access_secret_key)

    def upload_file(self, file_path: str, s3_folder_name="financial/banking"):
        """Upload file to AWS S3 Bucket.
        Args:
            file_path: path where to find the file to be uploaded
            bucket_name: name of the bucket in S3. Defaults to ""
            s3_folder_name: name of directory structure in S3 where to find should be uploaded. Defaults to financial/banking
        """
        transfer = S3Transfer(self._build_client())

        transfer.upload_file(filename=file_path,
                             bucket=self.bucket_name,
                             key=s3_folder_name + "/" + file_path.split("/")[-1])
