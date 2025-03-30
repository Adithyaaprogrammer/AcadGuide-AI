import os
from typing import List, Dict
from langchain_groq import ChatGroq
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# Initialize components
os.environ["GROQ_API_KEY"] = "your_groq_api_key_here"
llm = ChatGroq(model_name="mixtral-8x7b-32768")
embeddings = HuggingFaceEmbeddings()

# Course data and vector stores
course_data = [
    "Foundation Level: English 1, Math 1, Statistics 1, Computational Thinking, English 2, Math 2, Statistics 2, Python",
    "Diploma in Programming: Database Management Systems, Programming Data Structures & Algorithms using Python, Modern Application Development 1, Modern Application Development 2, Programming Concepts Using Java, System Commands",
    "Diploma in Data Science: Machine Learning Foundations, Machine Learning Technique, Machine Learning Practice, Business Data Management, Business Analytics, Tools in Data Science",
    "BSc Degree Level: Core 1 - Operating Systems & Computer Architecture, Core 2 - Software Testing & Software Engineering, Core 3 - AI: Search Methods for Problem Solving & Deep Learning, Design Thinking, Speech Technology, Deep Learning in Practice, Thematic Ideas in Data Science, Special topics in Machine Learning, Computer Vision"
]

vectorstore = Chroma.from_texts(texts=course_data, embedding=embeddings)
answer_vectorstore = Chroma(embedding_function=embeddings)

# Combined retrieval function
def combined_retriever(query: str):
    course_context = vectorstore.similarity_search(query)
    answer_context = answer_vectorstore.similarity_search(query)
    return course_context + answer_context

# QA chain setup
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever()
)

# Prompt template
prompt_template = PromptTemplate(
    input_variables=["level", "completed_courses"],
    template="Given the {level} in the IIT Madras BS Data Science program and completed courses: {completed_courses}, provide a structured path for selecting upcoming courses with names and recommended order."
)

def get_course_recommendations(level: str, completed_courses: List[str]) -> Dict[str, List[str]]:
    # Validate input level
    valid_levels = ["Foundation Level", "Diploma in Programming", 
                   "Diploma in Data Science", "BSc Degree Level"]
    if level not in valid_levels:
        return {"error": "Invalid program level specified"}
    
    # Format query
    query = prompt_template.format(
        level=level,
        completed_courses=", ".join(completed_courses)
    )
    
    # Retrieve combined context
    context = combined_retriever(query)
    context_texts = [doc.page_content for doc in context]
    
    # Generate recommendation
    result = qa_chain.run(input_documents=context_texts, query=query)
    
    # Store result for future reference
    answer_vectorstore.add_texts([f"{level} Recommendation: {result}"])
    
    return {
        "program_level": level,
        "completed_courses": completed_courses,
        "recommended_path": result
    }
