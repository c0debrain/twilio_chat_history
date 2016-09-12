import re
from twilio.rest import TwilioRestClient

account_sid = ''
auth_token  = ''

client = TwilioRestClient(account_sid, auth_token)

from flask import Flask, render_template
app = Flask(__name__, template_folder='.')

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route("/chat/")
def all_zips():
    return "uh nothing to see here"

@app.route('/chat/<number>')
def show_upcoming_zip_time(number):
    # sanitize the zipcode, remove anything that's not a number
    number = re.sub('[^0-9]', '', number)
    if number[0] != '1':
        number = '1' + number
    number = '+' +  number
     
    user_messages = getSMS(number)
    if len(user_messages) == 0:
        return "Couldn't find any messages to/from that number"

    return render_template('main.html', messages=user_messages)

def getSMS(user_number):
    from_messages = client.messages.list(from_=user_number) # messages from them
    to_messages = client.messages.list(to=user_number) # messages to them
    all_messages = []
    for message in from_messages + to_messages:
        all_messages.append({
            'time': message.date_sent,
            'date_sent': message.date_sent.strftime("%b %d, %Y %H:%M"),
            'from_number': message.from_,
            'to_number': message.to,
            'message': message.body,
            'num_media': message.num_media,
            'from_them': message.from_== user_number
        })

    # sort all the messages by time
    # all_messages.sort(key=lambda x: x['time'], reverse=True)
    all_messages.sort(key=lambda x: x['time'], reverse=False)

    return all_messages

if __name__ == "__main__":
    app.debug= True
    app.run(host='127.0.0.1', port=8000)

