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
os.environ["GROQ_API_KEY"] = "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"

# Initialize LLM (Groq Mixtral)
llm = ChatGroq(model_name="deepseek-r1-distill-qwen-32b")

# Load embeddings
embeddings = HuggingFaceEmbeddings()

transcripts = [
    "Foundation Level (8 Courses | 32 Credits)",
    "Core Courses:",
    "English 1 & 2",
    "Math 1 & 2 (Linear Algebra, Calculus, Multivariable Calculus)",
    "Statistics 1 & 2 (Probability, Hypothesis Testing)",
    "Computational Thinking (Flowcharts, Pseudocode)",
    "Python (Basic Scripting, Jupyter Notebooks)",

    "Diploma Level",
    "A. Diploma in Programming (6 Courses + 2 Projects | 27 Credits):",
    "Database Management Systems (SQL/NoSQL)",
    "Programming Data Structures & Algorithms (Python)",
    "Modern Application Development 1/2 (HTML/CSS/JS, React, Node.js)",
    "Java Programming (Enterprise Applications)",
    "System Commands (Linux CLI)",

    "B. Diploma in Data Science (6 Courses + 2 Projects | 27 Credits):",
    "Machine Learning Foundations (Supervised/Unsupervised Learning)",
    "Business Analytics (Tableau, Power BI)",
    "Tools in Data Science (LLMs, GIS, D3.js)",
    "Machine Learning Practice/Technique (ANN, CNNs)",

    "Degree Level (Advanced Courses | 28 Credits)",
    "Core Courses:",
    "Operating Systems & Computer Architecture",
    "Software Testing & Engineering",
    "AI: Search Methods (A*, Minimax) & Deep Learning",
    "Electives: Computer Vision, Speech Technology, LLMs, Bioinformatics",

    "Total Credits:",
    "BSc Degree: 114 Credits",
    "BS Degree: 142 Credits",

    "Key Resources for Vector Store",
    "Study Materials",
    "Formula Sheets: Math/Stats formulas for qualifiers [opennotes.in]",
    "YouTube Playlists: Course tutorials & qualifier prep [IITM BS YouTube Channel]",
    "Previous Papers: Qualifier/End Term Exam papers [IITM Student Community]",
    "Tools: Python, SQL, TensorFlow, OpenCV [Course Page]",

    "Assessments",
    "Weekly: Online assignments (programming quizzes)",
    "Monthly: In-person exams (coding, ML vivas)",

    "Projects:",
    "MAD 1/2 (Full-stack apps)",
    "Deep Learning Capstone (PyTorch/CNNs)",

    "Tools & Frameworks",
    "Programming: Python, Java, PostgreSQL",
    "Data Science: Scikit-learn, PyTorch, OpenCV",
    "Business Analytics: Tableau, Power BI",
    "Web Development: React, Flask, Vue.js",

    "Program Flexibility & Support",
    "Exit Options: Foundation Certificate/Diploma/BSc Degree",
    "Term Structure: 3 terms/year (Jan/May/Sep)",
    "Scholarships: Fee waivers for learners < ₹5 LPA",
    "Community: WhatsApp/Telegram groups for peer support"
]


# Create initial vector store from transcripts
vectorstore = Chroma.from_texts(texts=transcripts, embedding=embeddings)

# Create a new vector store to store final answers for future context
answer_vectorstore = Chroma(embedding_function=embeddings)

# Define prompt template
prompt_template = PromptTemplate(
    input_variables=["topic"],
    template="Given the topic {topic}, recommend relevant learning resources from the IIT Madras BS Data Science program."
)

# Pydantic model for request body
class TopicRequest(BaseModel):
    topic: str

# Define a combined retriever function to use both vector stores for context
def combined_retriever(query: str) -> List[str]:
    # Retrieve context from original vectorstore
    original_context = vectorstore.similarity_search(query)
    
    # Retrieve context from answer vectorstore
    answer_context = answer_vectorstore.similarity_search(query)
    
    # Combine results from both retrievers
    combined_context = original_context + answer_context
    
    return combined_context

# Define the resource recommendation function with combined context integration
def get_resource_recommendations(topic: str) -> Dict[str, List[str]]:
    # Use prompt template to format the query
    query = prompt_template.format(topic=topic)
    
    # Retrieve combined context from both vector stores
    context_documents = combined_retriever(query)
    
    # Extract text from retrieved documents for use in QA chain
    context_texts = [doc.page_content for doc in context_documents]
    
    # Run the QA chain with combined context to get the answer
    qa_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=vectorstore.as_retriever())
    result = qa_chain.run(input_documents=context_texts, query=query)
    
    # Add the topic and result as a new entry to the answer vector store for future use
    answer_vectorstore.add_texts([f"Topic: {topic}\nAnswer: {result}"])
    
    return {"topic": topic, "recommended_resources": result}
