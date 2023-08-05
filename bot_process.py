from transformers import pipeline
import os
import openai
from dotenv import load_dotenv

load_dotenv()
input_file = open("prompts/chat-with-skit.txt", "r")


def get_response(input_prompt):
    checkpoint = "MBZUAI/LaMini-Neo-125M"
    model = pipeline("text-generation", model=checkpoint)
    generated_text = model(input_prompt, max_length=512, do_sample=True)[0][
        "generated_text"
    ]
    return generated_text


system = """Transcript of a dialog, where the Customer interacts with a Marketing Employee named AI, who works at Skit.
            AI is supposed to convince the Customer to renew the subscription to a service. Start the conversation by convincing the Customer to renew the subscription.
            """


def get_response_gpt(input_prompt):
    openai.api_key = os.getenv("OPENAI_API_KEY")

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": input_prompt},
        ],
    )

    return completion.choices[0].message
