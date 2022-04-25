import json
import threading


class Payload:
    def __init__(self, target_action, **params):
        self.target_action = target_action
        self.params = params

    def get_content(self):
        return json.dumps(self.__dict__)


def print_received_message(func):
    """
    It prints the received message

    Args:
      func: The function to be decorated.

    Returns:
      The function wrapper is being returned.
    """

    def wrapper(*args):
        received_message = args[1]
        message_type = received_message.get_type()
        sender_id = received_message.get_sender_id()

        if message_type == "text":
            print("User", sender_id, "sent a message :", received_message.get_text_content())
        elif message_type == "postback":
            print("User",
                  sender_id,
                  "sent a postback message :",
                  "\nText :",
                  received_message.get_text_content(),
                  "\nPayload :",
                  received_message.get_payload())
        elif message_type == "quick_reply":
            print("User",
                  sender_id,
                  "sent a quick reply :",
                  "\nText :",
                  received_message.get_text_content(),
                  "\nPayload :",
                  received_message.get_payload())
        elif message_type == "attachments":
            if len(received_message.get_attachments()) == 1:
                print("User",
                      sender_id,
                      "sent an attachment :",
                      "\nType :",
                      received_message.get_attachments()[0]["type"],
                      "\nPayload :",
                      received_message.get_attachments()[0]["payload"])
            else:
                print("User",
                      sender_id,
                      "sent a multiple attachments :")

                for index, attachment in enumerate(received_message.get_attachments()):
                    print(f"Attachment {index + 1}",
                          "Type : {}\nPayload : {}".format(
                              attachment["type"],
                              attachment["payload"]))
        return func(*args)
    return wrapper


def threaded(function):
    """This decorator is used to make a function threaded

	Args:
		function (function) : The function to be threaded.
	"""

    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=function, args=args, kwargs=kwargs)
        thread.start()
        return thread

    return wrapper
