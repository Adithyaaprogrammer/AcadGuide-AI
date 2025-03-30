import os
from typing import List, Dict
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_groq import ChatGroq
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter

app = FastAPI()
def create_vector_db(folders: List[str]):

    embeddings = HuggingFaceEmbeddings()
    persist_directory = 'db'  # Directory to store the vector database
    all_docs = []

    for week_num, folder in enumerate(folders, 1):
        folder_path = os.path.join('/content', folder)
        for filename in os.listdir(folder_path):
            if filename.endswith('.pdf'):
                filepath = os.path.join(folder_path, filename)

                loader = PyPDFLoader(filepath)
                documents = loader.load()

                # Add metadata to each document (lecture number, week)
                for i, doc in enumerate(documents):
                    doc.metadata['lecture_no'] = i + 1
                    doc.metadata['week'] = week_num

                all_docs.extend(documents)

    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(all_docs)

    vector_db = Chroma.from_documents(
        documents=texts,
        embedding=embeddings,
        persist_directory=persist_directory
    )

    vector_db.persist()
    print(f"Vector database created and saved to: {persist_directory}")

# Example usage:
folders = ['week1','week2','week3', 'week4']
create_vector_db(folders)

os.environ["GROQ_API_KEY"] = "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"
llm = ChatGroq(model_name="llama-3.3-70b-versatile")
def answer_question(question: str):
  prompt_template = PromptTemplate(
    input_variables=["question"],
    template="Based on the context give hints and the lectures/resources to follow up in order to get the answer for the  question:{question} instead of directly giving the solution"
)
  vector_db = Chroma(persist_directory='db', embedding_function=HuggingFaceEmbeddings())
  retriever = vector_db.as_retriever()
  qa_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)
  result = qa_chain.run(prompt_template.format(question=question))
  
  return {"question": question, "answer": result}



def assignment_reminders(student_id: int, assignment: str):
    return {"student_id": student_id, "assignment": assignment, "status": "Reminder sent"}

def engagement_notifications(student_id: int):
    return {"student_id": student_id, "notification": "Engagement notification sent"}

def debugging_tips(code: str):
    prompt_template = PromptTemplate(
    input_variables=["code"],
    template="Analyze the following code snippet and provide step-by-step debugging tips, along with resources or techniques that can help resolve potential issues:\n\nCode:\n{code}"
)
    vector_db = Chroma(persist_directory='db', embedding_function=HuggingFaceEmbeddings())
    retriever = vector_db.as_retriever()
    qa_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)
    result = qa_chain.run(prompt_template.format(code=code))
  
    return {"question":code, "tips": result}

def common_errors_faqs():
    return {"FAQs": ["Common Syntax Errors", "How to debug loops?", "Why does my code crash?"]}

def portal_assistance(issue: str):
    return {"issue": issue, "solution": "Try clearing cache and restarting the system."}

def student_progress_updates(student_id: int):
    return {"student_id": student_id, "progress": "Student is on track with coursework."}
