import logging
 
import os
import shutil
import uuid
import re
from datetime import datetime
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import trim_messages
from langchain_openai import OpenAIEmbeddings

#from langchain_community.callbacks.manager import get_openai_callback
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
 
from ai.prompt import main_prompt
from ai.log import LoggerConfig
import os

load_dotenv()
logger_config = LoggerConfig()
logger = logger_config.get_logger(__name__)


openai_api_key = os.getenv('OPENAI_API_KEY')

conversational_rag_chain = None
#MAX_TOKENS = 1000
session_id = str(uuid.uuid4())
store = {}

from ai.modules.file_loaders import FileLoader
from ai.modules.text_chunkers import Chunker
from ai.modules.create_vectors import Chromadb

chroma=Chromadb()

# def create_db(file):
#     try:
#         content=FileLoader.load_file(file)
#         chunks=Chunker.split_chunking(content)
#         for item in Chunker.batch(chunks):
#             chroma.add_text(item) 
            
#         logger.info("Database Created", exc_info=True)
#         return "Database created successfully"
#     except Exception as e:
#         logger.error(f"Error in creating database: {e}", exc_info=True)
#         return f"Error creating database: {e}"

"""#ir"""
def create_db(file):
    try:
       
        content=FileLoader.load_file(file)
        document=Chunker.split_chunking(content)
        logger.info(f"Created chunks: {document}", exc_info=True)
        for documents in Chunker.batch(document):
            chroma.add_docs(documents)
            logger.info("Batches being processed")

        logger.info("Database Created", exc_info=True)
        return "created successfully"
    except Exception as e:
        logger.error(f"Error in creating database: {e}", exc_info=True)
        return f"Error creating database: {e}"

def format_conversation(conversation_string):
    try:
        messages = re.findall(r'(Human:|AI:)(.+?)(?=Human:|AI:|$)', conversation_string, re.DOTALL)
        formatted_history = [SystemMessage(content="you are a good therapist")]
        for speaker, content in messages:
            content = content.strip()
            if speaker == "Human:":
                formatted_history.append(HumanMessage(content=content))
            elif speaker == "AI:":
                formatted_history.append(AIMessage(content=content))
        return formatted_history
    except Exception as e:
        logger.error(f"Error in format_conversation: {e}", exc_info=True)
        return []

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    try:
        llm = ChatOpenAI(model=os.getenv("OPENAI_MODEL"))
        if session_id not in store:
            store[session_id] = ChatMessageHistory()
        history = store[session_id]
        if not history.messages:
            return history
        trimmer_larger = trim_messages(
            max_tokens=500,
            strategy="last",
            token_counter=llm,
            include_system=True,
            allow_partial=True,
            start_on="human"
        )
        trimmed_messages = trimmer_larger.invoke(history.messages)
        new_history = ChatMessageHistory()
        for message in trimmed_messages:
            new_history.add_message(message)
        store[session_id] = new_history
        return new_history
    except Exception as e:
        logger.error(f"Error in get_session_history: {e}", exc_info=True)
        return ChatMessageHistory()

def process_file():
    global conversational_rag_chain
    try:
        llm = ChatOpenAI(model=os.getenv("OPENAI_MODEL"))
        #vectorstore = setup_chroma()
        # embeddings = OpenAIEmbeddings(model=os.getenv("OPENAI_EMBEDDING_MODEL"))
        # vectorstore = Chroma(persist_directory="./vectorstore/chroma_db", embedding_function=embeddings) #vectorstore
        # retriever = vectorstore.as_retriever(search_type="mmr", search_kwargs={"k": 5})
        
        retriever = chroma.search()
        
        message = main_prompt()
        context_system_prompt = """ Given a chat history and the latest user question
                which might reference context in the chat history, 
                formulate a standalone question which can be understood 
                without the chat history. Do NOT answer the question, 
                just reformulate it if needed and otherwise return it as is."""
        
        contextualise_q_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", context_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}")
            ]
        )
        history_aware_retr = create_history_aware_retriever(llm, retriever, contextualise_q_prompt)
        current_date = datetime.now().strftime("%B %d, %Y")
        qa_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", message.format(current_date=current_date)),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )
        question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
        rag_chain = create_retrieval_chain(history_aware_retr, question_answer_chain)
        conversational_rag_chain = RunnableWithMessageHistory(
            rag_chain, get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer"
        )
        return conversational_rag_chain #"File processed successfully. You can now ask questions about the document."
    except Exception as e:
        logger.error(f"Error in process_file: {e}", exc_info=True)
        return "Failed to process file."
    
if (__name__ == "__main__"):
    process_file()
