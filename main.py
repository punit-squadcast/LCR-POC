from flask import Flask, request
from twilio.twiml.voice_response import Gather, VoiceResponse, Dial
from twilio.rest import Client

account_sid = 'SKfd175898a55da5c45632a0279ee14711'
auth_token = '3esU6LoBHdNW3CizWoDnScSwte8btjhU'
client = Client(account_sid, auth_token)

agents = {
    'sales': ['+919504683501'],
    'support': ['+919504683501']
}

def route_call(call_from, department):

    available_agents = agents.get(department, [])
    print(available_agents)
    
    if available_agents:
        response = VoiceResponse()
        dial = Dial(caller_id='+919504683501',action='/handleDialCallStatus', method='GET')
        dial.number('+919504683501')
        response.append(dial)
    else:
        response = VoiceResponse()
        response.say("All agents are busy. Please leave a voicemail after the tone.")
        response.record()
        response.hangup()
        
    return str(response)

app = Flask(__name__)

@app.route('/incoming-call', methods=['POST'])
def incoming_call():
    from_number = request.form.get('From')
    print(from_number,"hahaaha")
    department = 'sales' if from_number.startswith('+91') else 'support'
    
    response = VoiceResponse()
    print(response)
    with response.gather(numDigits=1, action='/handle-key', method='POST') as gather:
        gather.say("Welcome to our company. Press 1 for Sales or 2 for Support.")
    print(str(response))
    return str(response)

@app.route('/handle-key', methods=['POST'])
def handle_key():
    digit_pressed = request.form.get('Digits')
    
    if digit_pressed == '1':
        response = route_call(request.form.get('From'), 'sales')
    elif digit_pressed == '2':
        response = route_call(request.form.get('From'), 'support')
    else:
        response = VoiceResponse()
        response.say("Sorry, I don't understand that choice.")
        response.redirect('/incoming-call')
    print(response)
    return str(response)

@app.route('/handleDialCallStatus', methods=['GET', 'POST'])
def handle_dial_call_status():
    call_status = request.values.get('DialCallStatus')
    
    response = VoiceResponse()
    
    if call_status == 'completed':
        response.say("Call completed successfully")
    elif call_status == 'answered':
        response.say("The call was answered")
    elif call_status == 'busy':
        response.say("The call recipient was busy")
    elif call_status == 'no-answer':
        response.say("The call recipient didn't answer")
    elif call_status == 'failed':
        response.say("The call failed to connect")
    else:
        response.say("Unknown call status")
    
    return str(response)

if __name__ == '__main__':
    app.run(debug=True,port=5004)
