import os
from typing import List, Dict
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

os.environ["GROQ_API_KEY"] = "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"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

llm = ChatGroq(model_name="llama-3.3-70b-versatile")

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

course_data = [
    "Foundation Level: English 1, Math 1, Statistics 1, Computational Thinking, English 2, Math 2, Statistics 2, Python",
    "Diploma in Programming: Database Management Systems, Programming Data Structures & Algorithms using Python, Modern Application Development 1, Modern Application Development 2, Programming Concepts Using Java, System Commands",
    "Diploma in Data Science: Machine Learning Foundations, Machine Learning Technique, Machine Learning Practice, Business Data Management, Business Analytics, Tools in Data Science",
    "BSc Degree Level: Core 1 - Operating Systems & Computer Architecture, Core 2 - Software Testing & Software Engineering, Core 3 - AI: Search Methods for Problem Solving & Deep Learning, Design Thinking, Speech Technology, Deep Learning in Practice, Thematic Ideas in Data Science, Special topics in Machine Learning, Computer Vision"
]

vectorstore = Chroma.from_texts(texts=course_data, embedding=embeddings)

retriever = vectorstore.as_retriever()
qa_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)

prompt_template = PromptTemplate(
    input_variables=["level", "completed_courses"],
    template="Given the {level} in the IIT Madras BS Data Science program and the completed courses: {completed_courses}, provide a structured path for selecting upcoming courses. Include course names and a recommended order."
)


def get_course_recommendations(level: str, completed_courses: List[str]) -> Dict[str, List[str]]:
    query = prompt_template.format(level=level, completed_courses=", ".join(completed_courses))
    result = qa_chain.invoke(query).get("result")
    return result


level = "Diploma in Programming"
completed_courses = ["Database Management Systems", "Programming Data Structures & Algorithms using Python"]
recommendations = get_course_recommendations(level, completed_courses)

print("Recommended Courses:", recommendations)
