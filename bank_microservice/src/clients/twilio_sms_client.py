from twilio.rest import Client
from bank_microservice.hidden_info.hidden_info_loader import PersonalInfoLoader
from logs_microservice.logs import LogHandler


class TwilioClient:
    """Class to send SMS with Twilio.
    """

    def __init__(self):
        """Creates instance of Twilio.
        """

        log_handler = LogHandler()
        func_name, file_name = log_handler.func_name, log_handler.file_name

        print(f"Executing function: {func_name} in file: {file_name}")

        self.credentials = PersonalInfoLoader().load_credentials
        self.config = PersonalInfoLoader().load_config
        self.client = Client(self.credentials["twilio_credentials"]["account_sid"],
                             self.credentials["twilio_credentials"]["auth_token"])

    def send_sms(self, body_msg: str):
        """Send SMS.
        Args:
            body_msg: message to be sent in the SMS
        """

        log_handler = LogHandler()
        func_name, file_name = log_handler.func_name, log_handler.file_name

        print(f"Executing function: {func_name} in file: {file_name}")

        try:
            self.client.messages.create(
                                    body=f"{body_msg}",
                                    from_=self.config["sms_numbers"]["from"],
                                    to=self.config["sms_numbers"]["to"]
                                    )
            print("SMS sent successfully.")
        except Exception as e:
            print(f"Error trying to send sms.\nError args: {e.args}")
