import argparse
from langchain_chroma import Chroma 
from langchain_openai import ChatOpenAI
from pydantic import SecretStr

from get_embedding_function import get_embedding_function
import os
from dotenv import load_dotenv
load_dotenv()

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""


def main():
    # Create CLI.
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text
    query_rag(query_text)

# def query_rag(query_text: str):
#     # Prepare the DB.
#     embedding_function = get_embedding_function()
#     db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

#     # Search the DB.
#     results = db.similarity_search_with_score(query_text, k=5)

#     context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
#     prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
#     prompt = prompt_template.format(context=context_text, question=query_text)
#     # Use OpenAI instead of Ollama
#     api_key = os.getenv("OPENAI_API_KEY")
#     model = ChatOpenAI(
#         model="gpt-3.5-turbo",
#         api_key=SecretStr(api_key) if api_key else None
#     )
    
#     response_text = model.invoke(prompt)

#     sources = [doc.metadata.get("id", None) for doc, _score in results]
#     formatted_response = f"Response: {response_text.content}\nSources: {sources}"
#     print(formatted_response)
#     return response_text.content

def query_rag(query_text: str):
    # Prepare the DB.
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_score(query_text, k=5)

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    #prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    
    # Modified prompt to get more human-like, concise responses
    human_prompt = f"""
    Based on this context: {context_text}
    
    Answer this question in 3 sentences or less, writing as if you're a knowledgeable person explaining to someone. 
    Use direct language (e.g., "ITMO does X" instead of "they do X").
    Make it sound natural and conversational, not AI-generated.
    
    Question: {query_text}
    """
    
    # Use OpenAI instead of Ollama
    api_key = os.getenv("OPENAI_API_KEY")
    model = ChatOpenAI(
        model="gpt-3.5-turbo",
        api_key=SecretStr(api_key) if api_key else None,
        temperature=0.7  # Add some variation to make it less robotic
    )
    
    response_text = model.invoke(human_prompt)

    sources = [doc.metadata.get("id", None) for doc, _score in results]
    formatted_response = f"Response: {response_text.content}\nSources: {sources}"
    print(formatted_response)
    return response_text.content

if __name__ == "__main__":
    main()
