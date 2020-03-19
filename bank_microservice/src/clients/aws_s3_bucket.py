import boto3
from boto3.s3.transfer import S3Transfer
from hidden_info.hidden_info_loader import PersonalInfoLoader
from logs_microservice.logs import LogHandler


class S3Bucket:
    """Class for AWS S3 Bucket.
    """

    def __init__(self):
        """Creates instance of the class with the client authorized by AWS credentials.
        """

        log_handler = LogHandler()
        func_name, file_name = log_handler.func_name, log_handler.file_name

        print(f"Executing function: {func_name} in file: {file_name}")

        self.credentials = PersonalInfoLoader().load_credentials
        self.config = PersonalInfoLoader().load_config
        self.client = boto3.client('s3',
                                   aws_access_key_id=self.credentials["aws"]["s3"]["access_key"],
                                   aws_secret_access_key=self.credentials["aws"]["s3"]["access_secret_key"])

    def upload_file(self, file_path: str, bucket_name="", s3_folder_name="financial/banking"):
        """Upload file to AWS S3 Bucket.
        Args:
            file_path: path where to find the file to be uploaded
            bucket_name: name of the bucket in S3. Defaults to ""
            s3_folder_name: name of directory structure in S3 where to find should be uploaded. Defaults to financial/banking
        """

        log_handler = LogHandler()
        func_name, file_name = log_handler.func_name, log_handler.file_name

        print(f"Executing function: {func_name} in file: {file_name}")

        transfer = S3Transfer(self.client)
        if bucket_name == "":
            bucket_name = self.config["aws"]["s3"]["bucket_name"]

        transfer.upload_file(filename=file_path,
                             bucket=bucket_name,
                             key=s3_folder_name + "/" + file_path.split("/")[-1])
