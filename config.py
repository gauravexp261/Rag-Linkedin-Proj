from langchain_ollama import ChatOllama
from langchain_community.embeddings import HuggingFaceEmbeddings
import warnings
warnings.filterwarnings("ignore")

LLM_MODEL_ID = ChatOllama(
    model="llama3",
    temperature=0.2
)

EMBEDDING_MODEL_ID = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

MOCK_DATA_URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/ZRe59Y_NJyn3hZgnF1iFYA/linkedin-profile-data.json"
PROXYCURL_API_KEY = ""

CHUNK_SIZE = 150

INITIAL_FACTS_TEMPLATE = """
You are an AI assistant that provides detailed answers based on the provided context.

Context:
{context}

List 3 interesting facts about this person's career or education.
Use only the provided context.
"""

USER_QUESTION_TEMPLATE = """
You are an AI assistant that provides detailed answers based on the provided context.

Context:
{context}

Question:
{question}

If the answer is not in the context, say:
"I don't know. The information is not available."
"""
