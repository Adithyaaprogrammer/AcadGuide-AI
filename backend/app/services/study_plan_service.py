import os
from typing import Dict
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_groq import ChatGroq
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate



# Set up API key for Groq
os.environ["GROQ_API_KEY"] = "your_groq_api_key_here"

# Initialize LLM (Groq Mixtral)
llm = ChatGroq(model_name="mixtral-8x7b-32768")

# Load embeddings
embeddings = HuggingFaceEmbeddings()

# Simulated course transcripts (RAG input)
course_transcripts = {
    101: "Course: Python for Data Science. Topics: Variables, Data Types, Loops, Functions, NumPy, Pandas, Data Visualization, Machine Learning Basics.",
    102: "Course: Machine Learning. Topics: Supervised Learning, Unsupervised Learning, Neural Networks, Regression, Classification, Clustering, Reinforcement Learning.",
    103: "Course: Database Management. Topics: SQL, Normalization, Indexing, Transactions, NoSQL, Distributed Databases.",
    104: "Course: Computer Vision. Topics: Image Processing, CNNs, Object Detection, Face Recognition, Deep Learning for Vision."
}

# Create a vector store from transcripts
vectorstore = Chroma.from_texts(
    texts=list(course_transcripts.values()), embedding=embeddings
)

# Create retriever
retriever = vectorstore.as_retriever()

# Create a RetrievalQA chain
qa_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)

# Define study plan prompt template
prompt_template = PromptTemplate(
    input_variables=["course", "student_id"],
    template=(
        "Given the course {course}, generate a structured study plan for student ID {student_id}. "
        "Include a weekly breakdown of topics, recommended resources, and assignments."
    )
)


# Function to generate a study plan
def get_study_plan(course_id: int, student_id: int) -> Dict[str, str]:
    if course_id not in course_transcripts:
        return {"error": "Invalid course ID"}

    query = prompt_template.format(course=course_transcripts[course_id], student_id=student_id)
    result = qa_chain.run(query)
    
    return {"student_id": student_id, "course_id": course_id, "study_plan": result}


