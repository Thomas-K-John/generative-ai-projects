# Project 3: Agentic AI Text-to-Speech Assistant (Bedrock, Polly, Strands Agents)

## Project Overview
- __Less Code (15 lines), More Logic in English (30 lines):__ This project demonstrates how agentic models and advances in Large Language Models (LLMs) are transforming traditional programming. Instead of writing scripts using programming languages, you can now describe tasks in natural language, and intelligent agents orchestrate the execution.

- __Tool-Oriented Programming:__ By connecting agents with tools like file_read, file_write, and speak, you can orchestrate workflows where the system decides the execution sequence.

- __Focus on Business Logic, Not Boilerplate:__ Agents abstract away file management, summarization, and speech synthesis. Developers focus on designing workflows in natural language, rather than micromanaging syntax.

## Summary
In this project, we use Strands Agents + AWS Polly to:
 #### Input to the Agent
 - Read text files from the input/ folder
#### Output from the Agent
- Generate Markdown versions → output/md_file/
- Convert content to audio → output/audio/ 
- Generate summary text → output/summarized_text/
- Generate summary audio → output/summarized_audio/
#### Agents Response 
- agentic_response.txt -> This is a step-by-step execution log of the strands agent. It shows the agent’s internal reasoning and tool usage as it processes the files in the input/ directory.
## Technologies Used
- [Strands Agents](https://strandsagents.com/)
- AWS Bedrock's  Amazon Nova Premier LLM
- AWS Polly for speech synthesis

