import smtplib
import ssl
from email.message import EmailMessage
import slack
import requests
from twilio.rest import Client

# Preferred option
def send_text_twilio(recieve_number, text_to_send):
   
    account_sid = "YOUR_ACC_SID" # os.environ(YOUR_KEY_NAME)
    auth_token = "YOUR_AUTH_TOKEN" # os.environ(YOUR_KEY_NAME)
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=text_to_send,
        from_='YOUR_TWILIO_NUMBER',
        to=recieve_number
    )

# Send text via Textbelt (free but limit of 1 text per day)
def send_text_textbelt(recieve_number, text_to_send):

  resp = requests.post('https://textbelt.com/text', {
  'phone': recieve_number,
  'message': text_to_send,
  'key': 'textbelt',
  })

  return resp


# Send text via Gmail (free, unlimited, sends text AND email)
def send_text_python(recieve_number, text_to_send):

  port = 465  # For SSL
  smtp_server = "smtp.gmail.com"
  sender_email = 'YOUR_EMAIL'
  receiver_email = recieve_number
  password = 'YOUR_PASSWORD'
  message = text_to_send

  context = ssl.create_default_context()
  with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
      server.login(sender_email, password)
      server.sendmail(sender_email, receiver_email, message.encode('utf-8'))

# Sending Snipp to a specific channel or member of your Slack workspace
def send_slack_message(message):

  SLACK_BOT_TOKEN = 'YOUR_TOKEN'
  client = slack.WebClient(SLACK_BOT_TOKEN)

  users = client.users_list()["members"]
  client.chat_postMessage(channel='YOUR_CHANNEL_OR_NAME', text=message)