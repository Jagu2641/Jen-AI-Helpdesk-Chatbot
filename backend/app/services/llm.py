import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_answer(question: str, chnks: list[str]) -> str:
    context = "\n\n".join(chnks)

    prompt = f"""You are a helpful AI helpdesk assistant.
Answer the user's question using only the provided context.
If the answer is not in the context, say you could not find it in the uploaded documents.

Context:    
{context}

Question: 
{question}
"""
    
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You answer questions from uploaded helpdesk documents only."},
            {"role": "user", "content": prompt}
        ],
        temperature=0,
    )
    
    return response.choices[0].message.content

