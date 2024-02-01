import requests

def send_line_notify(notification_message, token):
    """
    發送訊息到 LINE Notify
    """
    headers = {
        'Authorization': 'Bearer ' + token,
    }

    data = {
        'message': notification_message
    }

    response = requests.post('https://notify-api.line.me/api/notify', headers=headers, data=data)
    return response.status_code
