# RAG-Based Chatbot Development

## Project Overview

An intelligent chatbot that can answer questions about products and services. This is a Retrieval-Augmented Generation (RAG) chatbot system to provide intelligent customer support.

## Architecture
![View the architecture diagram](https://github.com/Thomas-K-John/generative-ai-projects/blob/main/projects/rag_chatbot/images/rag_chatbot_architecture.jpg)

## Key Objectives

• Build a production-ready RAG system that processes multi-format documents.

• Implement strict context grounding to prevent hallucination.

• Demonstrate scalable architecture suitable for government applications.

• Use RAGAs to evaluate system precision, recall, and truthfulness.


## Evaluations using MLFlow and RAGAS

Once the experiment runs, open the MLflow UI to visualize results:
http://localhost:5000/

## Steps to bringup the RAG system

- Run the rag_injestion.py file to load the documents and embed them into the ChromDB vector store.
  
- Go to the src/ folder and run the following command:
  `uvicorn main:app --reload`
  
- Once the application server startup is complete, go to the Swagger UI provided by FastAPI:
  
  `http://127.0.0.1:8000/docs`
  
  • `/health` (GET method): To quickly verify whether the service is up and running.
  
  • `/stats` (GET method): To provide system statistics. Here we are displaying the CPU count.
  
  • `/chat` (POST method): To provide the user query and to get the response from the LLM.
  

## Important Points regarding the system

  • Using a hybrid approach combining vector search and keyword search, followed by reranking the retrieved chunks.
  • MLflow and RAGAs are used to evaluate multiple experimental configurations based on precision, recall, and truthfulness metrics.

## Limitations:

  • The application is currently designed to run without containerization. Deployment via Docker or other container technologies is not provided.
  
  • Currently, the system relies on the OpenAI API, which, while easy to use and requiring no infrastructure management, incurs ongoing costs and exposes data externally, limiting privacy, cost control, performance, and offline/local customization that could be achieved by moving to Ollama.
