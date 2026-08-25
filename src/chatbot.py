from config import client, MODEL_NAME
from prompts import SYSTEM_PROMPT


class JobSearchChatbot:
    def __init__(self):
        self.chat = client.chats.create(
            model=MODEL_NAME,
            config={
                "system_instruction": SYSTEM_PROMPT
            }
        )

    def send_message(self, user_message):
        response = self.chat.send_message(user_message)
        return response.text