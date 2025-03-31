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
from langchain_core.documents import Document
from collections import Counter
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import normalize

app = FastAPI()

# Initialize vector store with embedding function
embeddings = HuggingFaceEmbeddings()
# Create a Document store instead of direct text storage
faq_store = Chroma(
    collection_name="faq_documents",
    embedding_function=embeddings,
    persist_directory="faq_db"
)
def create_vector_db(folders: List[str]):

    embeddings = HuggingFaceEmbeddings()
    persist_directory = 'db'  # Directory to store the vector database
    all_docs = []
    base_path = r"C:\Users\rchan\Downloads\GitHub\soft-engg-project-jan-2025-se-Jan-15\backend\app\services\Content"
    for week_num, folder in enumerate(folders, 1):
        folder_path = os.path.join(base_path, folder)
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
folders = ['Week 3']
create_vector_db(folders)

# Set up LLM
os.environ["GROQ_API_KEY"] = "groq_key"
llm = ChatGroq(model_name="llama-3.3-70b-versatile")

def answer_question(question: str):
    prompt_template = PromptTemplate(
        input_variables=["question"],
        template="Based on the context give hints and the lectures/resources to follow up in order to get the answer for the question:{question} instead of directly giving the solution"
    )
    vector_db = Chroma(persist_directory='db', embedding_function=embeddings)
    retriever = vector_db.as_retriever()
    qa_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)
    result = qa_chain.run(prompt_template.format(question=question))
    
    # Store as Document objects instead of strings
    faq_store.add_documents([
        Document(
            page_content=f"{question}\n{result}",
            metadata={"question": question, "answer": result}
        )
    ])
    
    return {"question": question, "answer": result}

def debugging_tips(code: str):
    prompt_template = PromptTemplate(
        input_variables=["code"],
        template="Analyze the following code snippet and provide step-by-step debugging tips, along with resources or techniques that can help resolve potential issues:\n\nCode:\n{code}"
    )
    vector_db = Chroma(persist_directory='db', embedding_function=embeddings)
    retriever = vector_db.as_retriever()
    qa_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)
    result = qa_chain.run(prompt_template.format(code=code))
  
    return {"question": code, "tips": result}


def common_errors_faqs(similarity_threshold: float = 0.8):
    try:
        # Get all documents from the FAQ store
        retriever = faq_store.as_retriever(search_kwargs={"k": 100})
        documents = retriever.get_relevant_documents("")
        
        if not documents:
            return {"top_5_faqs": []}
        
        # Extract questions from documents
        questions = []
        docs_with_embeddings = []
        
        # Get embeddings for each document
        for doc in documents:
            if doc.metadata and "question" in doc.metadata:
                questions.append(doc.metadata["question"])
                # Store document for later use
                docs_with_embeddings.append(doc)
        
        if not questions:
            return {"top_5_faqs": []}
            
        # Get embeddings for all questions
        question_embeddings = embeddings.embed_documents(questions)
        
        # Normalize and cluster similar questions
        norm_embeddings = normalize(np.array(question_embeddings))
        clustering = DBSCAN(
            eps=1-similarity_threshold,
            min_samples=1, 
            metric='cosine'
        ).fit(norm_embeddings)
        
        # Group questions by cluster
        cluster_groups = {}
        for idx, label in enumerate(clustering.labels_):
            if label not in cluster_groups:
                cluster_groups[label] = []
            cluster_groups[label].append((questions[idx], idx))
        
        # Find the most frequent clusters
        cluster_sizes = [(len(qs), cluster_id) for cluster_id, qs in cluster_groups.items()]
        cluster_sizes.sort(reverse=True)
        
        # Get top 5 FAQs (or fewer if there are less than 5 clusters)
        top_5_faqs = []
        for _, cluster_id in cluster_sizes[:5]:
            cluster_data = cluster_groups[cluster_id]
            # Get the most representative question from each cluster
            if cluster_data:
                # Use the first question in each cluster
                representative_q, idx = cluster_data[0]
                representative_doc = docs_with_embeddings[idx]
                faq_entry = {
                    "question": representative_q,
                    "answer": representative_doc.metadata.get("answer", "")
                }
                top_5_faqs.append(faq_entry)
        
        return {"top_5_faqs": top_5_faqs}
    
    except Exception as e:
        return {"error": str(e)}

def portal_assistance(issue: str):
    return {"issue": issue, "solution": "Try clearing cache and restarting the system."}

def student_progress_updates(student_id: int):
    return {"student_id": student_id, "progress": "Student is on track with coursework."}


def assignment_reminders(student_id: int, assignment: str):
    return {"student_id": student_id, "assignment": assignment, "status": "Reminder sent"}

def engagement_notifications(student_id: int):
    return {"student_id": student_id, "notification": "Engagement notification sent"}

answer = common_errors_faqs()
print(answer["top_5_faqs"])