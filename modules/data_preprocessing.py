import json
import logging
from typing import Dict, List, Any

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_classic.schema import Document
from langchain_community.vectorstores import Chroma

from modules.llm_interface import create_embedding

logger = logging.getLogger(__name__)

def split_profile_data(profile_data: Dict[str, Any]) -> List[Document]:
    try:
        profile_json = json.dumps(profile_data)
        document = Document(page_content=profile_json)

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=150,
            chunk_overlap=20
        )

        chunks = splitter.split_documents([document])
        logger.info(f"Created {len(chunks)} chunks")
        return chunks

    except Exception as e:
        logger.error(e)
        return []

def create_retriever(chunks: List[Document]):
    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=create_embedding()
    )
    return vectordb.as_retriever(search_kwargs={"k": 5})
