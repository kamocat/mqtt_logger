from mailjet_rest import Client
import credentials
import os
mailjet = Client(auth=(credentials.api_key, credentials.api_secret), version='v3.1')
data = {
  "From": {
    "Email": "mhece.api@gmail.com",
    "Name": "Marshal"
  },
  "To": [
  ],
  "Subject": "MQTT Alert",
  "TextPart": "My first Mailjet email",
}

def send(msg, recepients):
    data['TextPart'] = msg
    for email in recepients:
        data['To'].append({'Email':email, 'Name':'Marshal'})
    result = mailjet.send.create(data={'Messages': [data]})
    print(result.status_code)
    print(result.json() )
