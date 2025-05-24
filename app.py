import streamlit as st
from langchain.chains import create_history_aware_retriever,create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceHolder
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
import os
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFDirectoryLoader


from dotenv import load_dotenv
load_dotenv()

os.environ["HF_TOKEN"]=os.getenv("HF_TOKEN")
embeddings=HuggingFaceEmbeddings(model_name="google/gemma-3-27b-it")

## set up streamlit
st.title("Conversational RAG with pdf upload and chat history")
st.write("Upload pdf and chat with their content")

api_key=st.text_input("enter your groq api key",type="password")
if api_key:
   llm=ChatGroq(groq_api_key=api_key,model_name="gemma2-9b-it")
   session_id=st.text_input("Session id",value="default session")
   if 'store' not in st.session_state:
      st.session_state.store={}
   upload_file=st.fie_uploader("Choose a PDF file",type="pdf",accept_multiple_files=True)
   if upload_file:
      documents=[]
      for uploaded_files in upload_file:
         temppdf="C:/Users/shiva/Desktop/conversatioal_qa_chatbot_with_pdf/temp.pdf"
         with open(temppdf,"wb") as file:
            file.write(uploaded_file.get_value())
            loader=PyPDFDirectoryLoader(temppdf)
            docs=loader.load()
            documents.extend(docs)
      text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
      splits=text_splitter.split_documents(docs)
      vectorstore=Chroma.from_documents(documents=splits,embedding=embeddings)
      retriever=vectorstore.as_retriever()
   contextualize_q_system_prompt=(
       "Given a chat history and the latest uses question"
       "which might reference context in chat history"
       "formulate a standalone question which can be understood"
       "without the chat question.Do not answer the question,"
       "just reformulate if nededed otherwise return it as it is"
       )
   contextualize_q_prompt=ChatPromptTemplate.from_messages(
      [
         ("system",contextualize_q_system_prompt),
         MessagesPlaceHolder("chat_history"),
         ("human","{input}"),
      ]
   )
   question_answer_chain=create_stuff_documents_chain(llm,qa_prompt)
   history_aware_retriever=create_history_aware_retriever(llm,retriever,contextualize_q_prompt)
   rag_chain=create_retrieval_chain(history_aware_retriever,question_answer_chain)

   def get_session_history(session:str)->BaseChatMessageHistory():
      if session_id not in st.session_state.store:
         st.session_state.store[session_id]=ChatMessageHistory()
      return st.session_state.store[session_id]
   conversational_rag_chain=RunnableWithMessageHistory(
      rag_chain,get_session_history,
      input_message_key="input",
      history_message_key="chathistory",
      output_message_key="answer"
   )
   user_input=st.text_input("your question")
   if user_input:
      session_history=get_session_history(session_id)
      response=conversational_rag_chain.invoke(
         {"input":user_input},
         config={"configuirable":{"session_id":session_id}
         },
  )
      st.write(st.session_state.store)
      st.success("assistant",response["answer"])
      st.write("chat history",session_history.messages)
   else:
      st.warning("please enter groq api key")
      



   






         



