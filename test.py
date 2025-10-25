import base64
import httpx
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

template = """Question: {question}

Answer: Let's think step by step."""

model = ChatOllama(model="qwen2.5vl:7b")



# Fetch image data
image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"
image_data = base64.b64encode(httpx.get(image_url).content).decode("utf-8")
message = [{
    "role": "user",
    "content": [
        {
            "type": "text",
            "text": "Describe the weather in this image:",
        },
    ],
}]

for chunk in model.stream(message):
    print(chunk.text, end=" ", flush=True)



