from transformers import pipeline

input_file = open("prompts/chat-with-skit.txt", "r")


# input_prompt = input_file.read()
def get_response(input_prompt):
    checkpoint = "MBZUAI/LaMini-T5-61M"
    model = pipeline("text2text-generation", model=checkpoint)
    generated_text = model(input_prompt, max_length=512, do_sample=True)[0][
        "generated_text"
    ]
    return generated_text
