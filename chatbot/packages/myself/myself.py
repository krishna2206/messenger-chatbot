from chatbot.messenger import SEND_API


def hello(recipient_id):
    SEND_API.send_text_message("Hello World !", recipient_id)