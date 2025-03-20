import os
from typing import List, Dict
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_groq import ChatGroq
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# Initialize FastAPI app
app = FastAPI()

# Set up API key for Groq
os.environ["GROQ_API_KEY"] = "your_groq_api_key_here"

# Initialize LLM (Groq Mixtral)
llm = ChatGroq(model_name="mixtral-8x7b-32768")

# Load embeddings
embeddings = HuggingFaceEmbeddings()

# Transcripts or course materials (RAG input)
transcripts = [
    "Foundation Level: English 1, Math 1, Statistics 1, Computational Thinking, English 2, Math 2, Statistics 2, Python",
    "Diploma in Programming: Database Management Systems, Programming Data Structures & Algorithms using Python, Modern Application Development 1, Modern Application Development 2, Programming Concepts Using Java, System Commands",
    "Diploma in Data Science: Machine Learning Foundations, Machine Learning Technique, Machine Learning Practice, Business Data Management, Business Analytics, Tools in Data Science",
    "BSc Degree Level: Core 1 - Operating Systems & Computer Architecture, Core 2 - Software Testing & Software Engineering, Core 3 - AI: Search Methods for Problem Solving & Deep Learning, Design Thinking, Speech Technology, Deep Learning in Practice, Thematic Ideas in Data Science, Special topics in Machine Learning, Computer Vision"
]

# Create vector store from transcripts
vectorstore = Chroma.from_texts(texts=transcripts, embedding=embeddings)

# Set up retriever
retriever = vectorstore.as_retriever()

# Create a RetrievalQA chain
qa_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)

# Define prompt template
prompt_template = PromptTemplate(
    input_variables=["topic"],
    template="Given the topic {topic}, recommend relevant learning resources and structured course paths from the IIT Madras BS Data Science program."
)

# Pydantic model for request body
class TopicRequest(BaseModel):
    topic: str

# Define the resource recommendation function
def get_resource_recommendations(topic: str) -> Dict[str, List[str]]:
    query = prompt_template.format(topic=topic)
    result = qa_chain.run(query)
    
    # Process result into structured output
    lines = result.split("\n")
    recommendations = {"Recommended Resources": []}
    
    for line in lines:
        if line.startswith("- "):  # Identify course/resource names
            recommendations["Recommended Resources"].append(line[2:])
    
    return recommendations


