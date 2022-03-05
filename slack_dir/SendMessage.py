import requests


token_1 = 'xoxb-3113764770950-3120486752259'
token_2 = '-pFRSwGsCZRbdt29ZtOETisDk'
token = token_1 + token_2

def post_message(text):
    response = requests.post("https://slack.com/api/chat.postMessage",
                                 headers={"Authorization": "Bearer " + token},
                                 data={"channel": '#alarm_system', "text": text}
                             )
    print(response.content)

def post_image(channel, text):
    uploadfile = "test.png"
    with open(uploadfile, 'rb') as f:
        response = requests.post("https://slack.com/api/files.upload",
                                     headers={"Authorization": "Bearer " + token},
                                     data={"channel": channel, "initial_comment": text},
                                     files = {'file': f}
                                 )
    print(response.content)
