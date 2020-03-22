from bank_microservice.src import GmailClient

client = GmailClient()
client.login()
client.build_email_message(mail_objective="test", subject="test", body="python test")
client.send_email()
