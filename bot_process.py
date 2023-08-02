from transformers import pipeline

checkpoint = "MBZUAI/LaMini-T5-61M"

model = pipeline("text2text-generation", model=checkpoint)

input_file = open("prompts/chat-with-skit.txt", "r")
# input_prompt = input_file.read()
input_prompt = "Why did you call?"
generated_text = model(input_prompt, max_length=512, do_sample=True)[0][
    "generated_text"
]

print(generated_text)
