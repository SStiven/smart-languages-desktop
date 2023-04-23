import openai
import json

openai_key = "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"


class OpenAIChatClient:
    def __init__(self, system_instructions, model="gpt-3.5-turbo"):
        self.messages = []
        openai.api_key = openai_key
        self.add_text_to_messages(system_instructions, "system")
        self.gpt_model = model

    def add_text_to_messages(self, text, role):
        new_message = {"role": role, "content": text}
        self.messages.append(new_message)

    def send_request(self, text):
        user_text = text

        self.add_text_to_messages(user_text, "user")

        openai_response = openai.ChatCompletion.create(
            model=self.gpt_model,
            messages=self.messages,
            temperature=0.2,
            max_tokens=1000,
            top_p=1,
            frequency_penalty=0.2,
            presence_penalty=0.2,
            stop=[" Human:", " AI:"],
        )

        return openai_response

    def print_as_json(self, data):
        response_json = json.dumps(data)
        response_obj = json.loads(response_json)
        print(json.dumps(response_obj, indent=4))

    def chat(self, new_message):
        openai_response = self.send_request(new_message)
        # self.print_as_json(openai_response)
        return openai_response

    def print_messages(self, messages):
        for m in messages:
            print(f"{m['role']}: {m['content']}")
