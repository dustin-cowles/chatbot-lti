import logging
import time

from openai import OpenAI

from lib.config import ConfigFile

OPENAI_CONFIG_PATH = "config/openai_config.json"


class OpenAi():
    def __init__(self, user_cache):
        self.config = ConfigFile(OPENAI_CONFIG_PATH)
        self.user_cache = user_cache
        self.client = OpenAI(
            api_key=self.config.get("api_key"),
            organization=self.config.get("organization_id")
        )

    def send_message(self, message, data=None):
        thread_id = self.user_cache.get("thread_id")
        if thread_id is None:
            thread = self.client.beta.threads.create()
            self.user_cache.set("thread_id", thread.id)
            self.user_cache.save()
            thread_id = thread.id

        if data is not None:
            with OpenAiFile(data, self.client) as file:
                message = self.client.beta.threads.messages.create(
                    thread_id=thread_id,
                    role="user",
                    content=self.config.get("data_prompt"),
                    file_ids=[file.id]
                )
        else:
            self.client.beta.threads.messages.create(
                thread_id=thread_id,
                role="user",
                content=message
            )

        run_id = self.client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=self.config.get("assistant_id"),
            stream=False
        ).id

        while True:
            run = self.client.beta.threads.runs.retrieve(
                run_id=run_id, thread_id=thread_id)
            if run.status == "completed":
                break
            time.sleep(1)
        messages = self.client.beta.threads.messages.list(thread_id)

        return self.format_message_response(messages)

    def update_course_materials(self, course_materials):
        return self.send_message(
            self.config.get("data_prompt"),
            course_materials)

    def format_message_response(self, message_response):
        """
        Packages the messages for the client.

        :param message_response: The messages returned by the backend.

        :return: The messages formatted for the client.
        :rtype: list of dict
        """
        formatted_messages = []
        for message in message_response:
            role = message.role
            for content in message.content:
                if content.text.value == self.config.get("data_prompt"):
                    # We do not want to include the messages we sent
                    # to the assistant to update course materials.
                    continue
                formatted_messages.append({
                    "sender": role,
                    "content": content.text.value
                })
        formatted_messages.reverse()

        return formatted_messages


class OpenAiFile():
    def __init__(self, data, client):
        self.data = data
        self.client = client

    def __enter__(self):
        self.openai_file = self.client.files.create(
            file=self.data.encode('utf-8'),
            purpose="assistants"
        )

        return self.openai_file

    def __exit__(self, exc_type, exc_val, exc_tb):
        # TODO: Figure out how to handle file lifecycle
        # self.client.files.delete(self.openai_file.id)
        pass
