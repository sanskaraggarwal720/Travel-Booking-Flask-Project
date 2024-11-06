from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
# print(api_key)

genai.configure(api_key=api_key)

def ChatWIthLLM(question):
    with open("data.txt") as f:
        data = f.readlines()  # Reads all lines into a list

    # question = str(input("What is the question: "))

    prompt = f"""
    System: You are an AI assistant tasked with giving me output based on the context i provide. if it isn't present
    in context, say `i dont know` and if the question is of small talk type like `hi`,`how are you`, `thankyou` then you should reply appropriately instead of saying `I don't know`. They answer should be based on facts shared in <context> tag while question is
    shared in <question> tag. 

    Human: 
    <context>
    {data}
    </context>

    <question>
    {question}
    </question>

    Ensure that response is based upon the context

    Response:
    """
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    print(response.text)
    return response.text