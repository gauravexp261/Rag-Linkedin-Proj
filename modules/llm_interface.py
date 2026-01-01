import logging
from typing import Dict, Any, Optional

import config
logger = logging.getLogger(__name__)


def create_embedding() -> config.HuggingFaceEmbeddings:
    embedding = config.EMBEDDING_MODEL_ID
    logger.info(f'Crrated hugging face embedding: {embedding}')
    return embedding

def create_llm() -> config.ChatOllama:
    llm = config.LLM_MODEL_ID
    logger.info(f'Crrated llama model: {llm}')
    return llm




    