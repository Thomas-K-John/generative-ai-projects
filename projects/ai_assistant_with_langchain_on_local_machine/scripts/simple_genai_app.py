import os
from dotenv import load_dotenv
load_dotenv()

## Langsmith Tracking
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_PROJECT"]=os.getenv("LANGCHAIN_PROJECT")

from langchain_ollama import OllamaLLM
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

## Prompt Template
prompt=ChatPromptTemplate.from_messages(
    [
        ("system", "You are an intelligent helpful assistant. Please respond to the quesions asked."),
        ("user", "Question:{question}")
    ]
)

## Streamlit Framework
st.title("Langchain Experiment with Gemma2")
input_text=st.text_input("How may I help you!")

## Ollama gemma2:2b model
llm=OllamaLLM(model="gemma2:2b")
output_parser=StrOutputParser()
chain=prompt|llm|output_parser

if input_text:
    st.write(chain.invoke({"question":input_text}))
