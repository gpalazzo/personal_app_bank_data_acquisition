import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from bank_microservice.hidden_info.hidden_info_loader import PersonalInfoLoader
from logs_microservice.logs import LogHandler


class GmailClient:
    """Class to send email with Gmail.
    """

    def __init__(self, smtp_server: str = "smtp.gmail.com", mime_obj_subtype: str = "alternative"):
        """Creates instance of Gmail.
        Args:
            smtp_server: protocol for email transmission. Defaults to smtp.gmail.com
            mime_obj_subtype: subtype for MIMEMultipart
        """

        log_handler = LogHandler()
        func_name, file_name = log_handler.func_name, log_handler.file_name

        print(f"Executing function: {func_name} in file: {file_name}")

        self.smtp_server = smtp_server
        self.credentials = PersonalInfoLoader().load_credentials
        self.server = smtplib.SMTP_SSL(self.smtp_server)
        self.email_sender = self.credentials["gmail_credentials"]["username"]
        self.msg = MIMEMultipart(mime_obj_subtype)

    def login(self, username: str = "", password: str = ""):
        """Login into Gmail, i.e., Gmail credentials.
        Args:
            username: email from Gmail. Defaults to ""
            password: password from Gmail. Defaults to ""
        """

        log_handler = LogHandler()
        func_name, file_name = log_handler.func_name, log_handler.file_name

        print(f"Executing function: {func_name} in file: {file_name}")

        if username == "" or password == "":
            self.server.login(self.email_sender,
                              self.credentials["gmail_credentials"]["password"])
        else:
            self.server.login(username, password)

    def build_email_message(self, mail_objective: str, subject: str, body: str):
        """Build the HTML email message to be sent with subject, sender and receiver.
        Args:
            mail_objective: email's objective (purpose). It helps identifying the email receiver
            subject: subject of the email
            body: body message of the email
        """

        log_handler = LogHandler()
        func_name, file_name = log_handler.func_name, log_handler.file_name

        print(f"Executing function: {func_name} in file: {file_name}")

        if mail_objective == "rdc":
            self.msg["To"] = self.credentials["bank_mailing"]["rdc"]
            self.msg["Cc"] = self.credentials["bank_mailing"]["rdc_cc"]
        elif mail_objective == "test":
            self.msg["To"] = self.email_sender
        else:
            self.msg["To"] = ""

        self.msg["Subject"] = subject
        self.msg["From"] = self.email_sender

        html = f"<html><body><p>{body}</p></body></html>"
        mail_body_html = MIMEText(html, "html")

        self.msg.attach(mail_body_html)

    def send_email(self):
        """Send the email.
        """

        log_handler = LogHandler()
        func_name, file_name = log_handler.func_name, log_handler.file_name

        print(f"Executing function: {func_name} in file: {file_name}")

        self.server.sendmail(self.email_sender, self.msg["To"], self.msg.as_string())
        self.server.quit()

