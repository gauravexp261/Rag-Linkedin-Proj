import logging
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

import config
from modules.llm_interface import create_llm

logger = logging.getLogger(__name__)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def answer_question(retriever, user_query: str):
    docs = retriever.invoke(user_query)
    context = format_docs(docs)

    chain = (
        PromptTemplate.from_template(config.USER_QUESTION_TEMPLATE)
        | create_llm()
        | StrOutputParser()
    )

    return chain.invoke({
        "context": context,
        "question": user_query
    })

def generate_initial_facts(retriever):
    docs = retriever.invoke(
        "Provide three interesting facts about this person's career or education"
    )
    context = format_docs(docs)

    chain = (
        PromptTemplate.from_template(config.INITIAL_FACTS_TEMPLATE)
        | create_llm()
        | StrOutputParser()
    )

    return chain.invoke({"context": context})
