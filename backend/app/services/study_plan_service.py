import os
from typing import List, Dict
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_groq import ChatGroq
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# Set up API key for Groq
os.environ["GROQ_API_KEY"] = "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"

# Initialize LLM (Groq Mixtral)
llm = ChatGroq(model_name="llama-3.3-70b-versatile")

# Load embeddings
embeddings = HuggingFaceEmbeddings()

# Course transcripts and answer storage
course_transcripts = {
    101: "Course: Python for Data Science. Topics: Variables, Data Types, Loops, Functions, NumPy, Pandas, Data Visualization, Machine Learning Basics.",
    102: "Course: Machine Learning. Topics: Supervised Learning, Unsupervised Learning, Neural Networks, Regression, Classification, Clustering, Reinforcement Learning.",
    103: "Course: Database Management. Topics: SQL, Normalization, Indexing, Transactions, NoSQL, Distributed Databases.",
    104: "Course: Computer Vision. Topics: Image Processing, CNNs, Object Detection, Face Recognition, Deep Learning for Vision."
}

# Create vector stores
vectorstore = Chroma.from_texts(
    texts=list(course_transcripts.values()), 
    embedding=embeddings
)
answer_vectorstore = Chroma(embedding_function=embeddings)

# Combined retriever function
def combined_retriever(query: str):
    original = vectorstore.similarity_search(query)
    answers = answer_vectorstore.similarity_search(query)
    return original + answers

# QA Chain setup
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever()
)

# Prompt template
prompt_template = PromptTemplate(
    input_variables=["course", "student_id"],
    template="Given {course}, create a study plan for student {student_id} with weekly topics, resources, and assignments."
)

# Function to generate a study plan
def get_study_plan(course_id: int, student_id: int) -> Dict[str, str]:
    # Check if course ID is valid
    if course_id not in course_transcripts:
        return {"error": "Invalid course ID"}
    
    # Format the query using the prompt template
    query = prompt_template.format(
        course=course_transcripts[course_id],
        student_id=student_id
    )
    
    # Retrieve context from both vector stores
    context = combined_retriever(query)
    context_texts = [doc.page_content for doc in context]
    
    # Generate the study plan using the QA chain
    result = qa_chain.run(input_documents=context_texts, query=query)
    
    # Store the result in the answer vector store for future use
    answer_vectorstore.add_texts([f"Course {course_id} Plan: {result}"])
    
    return {
        "student_id": student_id,
        "course_id": course_id,
        "study_plan": result
    }