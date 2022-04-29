# from datetime import datetime
import json

import config
from chatbot.core import recognizer, fetcher, exceptions
from chatbot.messenger import SEND_API
from chatbot.model import Model
from chatbot.utils import print_received_message, threaded


class Bot:
    def __init__(self):
        # Initial configuration
        self.INTENTS = fetcher.fetch_intents(fetcher.fetch_intents_modules(config.PACKAGES))
        self.MODEL = Model(config)

        # print(datetime.now().strftime("[%Y-%m-%d %H:%M:%S]"), "Bot", id(self), "is ready")

    @threaded
    @print_received_message
    def receive_message(self, message):
        user_id = message.get_sender_id()
        SEND_API.mark_seen_message(user_id)

        user = self.MODEL.get_user(user_id)
        if user is None:
            print(f"Adding user {user_id} in the database")
            self.MODEL.add_user(user_id)
        else:
            self.MODEL.update_user(user_id)

        self.respond_message(message)

    @threaded
    def respond_message(self, message):
        user_id = message.get_sender_id()
        message_type = message.get_type()

        if message_type in ("postback", "quick_reply"):
            query = self.MODEL.get_query(user_id)
            if query is not None:
                self.MODEL.remove_query(user_id)

            payload = json.loads(message.get_payload())
            target_action = payload.get("target_action")
            action_params = payload.get("params")
            user_intent = recognizer.search_for_intent(self.INTENTS, target_action)

            self.respond_from_user_intent(user_intent, **action_params, recipient_id=user_id)  # avec params

        elif message_type in ("text", "attachments"):
            query = self.MODEL.get_query(user_id)

            if query is None:
                user_intent, extracted_data = recognizer.extract_user_intent(self.INTENTS, message)
                if user_intent.get("type") == "fallback":
                    self.respond_from_user_intent(user_intent, recipient_id=user_id)
                else:
                    self.respond_from_user_intent(user_intent, **extracted_data, recipient_id=user_id)
            else:
                user_intent = recognizer.search_for_intent(self.INTENTS, query.get("action"))
                query_params = {} if query.get("params") is None else query.get("params")

                if user_intent is not None:
                    param = None
                    if message_type == "text":
                        param = message.get_text_content()
                    elif message_type == "attachments":
                        param = message.get_attachments()[0].get("payload").get("url")
                    self.respond_from_user_intent(user_intent, param, **query_params, recipient_id=user_id)
                    self.MODEL.remove_query(user_id)
                else:
                    self.MODEL.remove_query(user_id)
                    raise exceptions.UnableToRespondError(
                        "Failed to extract user's intent.\n" +
                        f"There is no intent that matches the action '{query.get('action')}', " +
                        "maybe you forgot to add the corresponding intent to that action ?")

    def respond_from_user_intent(self, user_intent, *params, **keyword_params):
        """Execute the action (function) that corresponds to the user's intent.

		Args:
			user_intent (dict): The user's intent.

		Raises:
			exceptions.IntentExecutionError: If this method failed to execute the function.
			exceptions.UnableToRespondError: If the param user_intent is None.
		"""
        if user_intent is not None:
            SEND_API.typing_on_message(keyword_params.get("recipient_id"))
            try:
                self.execute_action(
                    user_intent.get("action"),
                    *params,
                    **keyword_params,
                )
            except Exception as error:
                raise exceptions.IntentExecutionError(
                    f"Failed to execute user's intent , caused by {type(error).__name__}: {error}\n" +
                    "Maybe there is an error in the action code ?" +
                    "See the exception message above this exception to know the origin of the error.")
        else:
            raise exceptions.UnableToRespondError(
                "Failed to extract user's intent, maybe you forgot to add the corresponding intent to the action ?")

    @staticmethod
    def execute_action(action, *args, **kwargs):
        action(*args, **kwargs)
