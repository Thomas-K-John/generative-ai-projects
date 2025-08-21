# Project 1: Streamlit-Powered Generative AI Assistant with LangChain on Local Machine
## Summary
* This project demonstrates the integration of the LangChain framework with Gemma2 Large Language model locally hosted using Ollama, wrapped within a Streamlit application for an interactive user experience.
* It serves as a practical showcase of building and deploying an AI-driven web application for Q&A systems using LangChain and Streamlit, enhancing both the development and user experience.

### Command to run the app: `streamlit run scripts/simple_genai_app.py`
  
## Key elements include:
* Langsmith Tracking: Enables tracking and monitoring of LangChain processes for debugging and performance insights.
* Prompt Engineering: Implements a structured prompt template designed for a conversational AI system to respond intelligently to user queries.
* Streamlit Interface: Provides a simple and interactive UI where users can input their questions and receive real-time answers.
* Model Integration: Leverages OllamaLLM with Gemma2:2b (a compact, open-source AI model from Google DeepMind that can perform tasks like text generation, translation, and answering questions)

## Prerequisites
1. Python Environment : Ensure Python 3.10 or higher is installed on your system.
   
   Reference : https://anaconda.org/anaconda/python
   
2. Ollama : Ollama is an open-source tool that lets users run large language models (LLMs) on their local machine.
   
   Reference : https://ollama.com/download
   
3. LangSmith and Langchain :
      * Langsmith is a framework designed to simplify the development and deployment of applications utilizing language models.
      * LangChain is a framework specifically tailored for building applications that use large language models (LLMs). It focuses on the concept of chains, which are sequences of components that process inputs and outputs in a structured way. This framework helps developers create complex workflows involving language models by providing a modular approach.
   NOTE: Signup to LangSmith and get the API key.
   
   Reference : https://smith.langchain.com

## Tips:
1. List of commonly used conda commands to manage the environment:
      * Create a New Environment: `conda create -n <env_name> python=<python_version>` Eg: `conda create -n genai_env python=3.10`
      * Activate an Environment: `conda activate <env_name>`
      * Deactivate the Current Environment: `conda deactivate`
      * Remove an Environment: `conda remove -n <env_name> --all`
      * List All Environments: `conda env list`
            
2. List of Ollama commands to manage the LLM on local machine:
      * List Available Models: `ollama list`
      * Pull a Model: `ollama pull <model_name>` Eg: To pull Google gemma2:2b model:  `ollama pull gemma2:2b`
      * Run a Model: `ollama run <model_name>`
      * Remove a Model: `ollama remove <model_name>`
        
NOTE: There is always the option to use --help to learn more about the conda and ollama commands. 

Eg: `ollama --help` or `ollama <command> --help`



