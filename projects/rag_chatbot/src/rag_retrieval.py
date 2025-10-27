from dotenv import load_dotenv
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from langchain_cohere import CohereRerank
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain_chroma import Chroma
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.schema import Document

load_dotenv()

class HybridRAGRetrieverModel:
    """A simple RAG retriever using ChromaDB and HuggingFace embeddings with OpenAI LLM."""
    def __init__(self, db_path="db/chroma_db", model_name='sentence-transformers/all-MiniLM-L6-v2'):
        model_kwargs = {"device": "cpu"}
        encode_kwargs = {"normalize_embeddings": False}
        embedding = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs=model_kwargs,
            encode_kwargs=encode_kwargs,
        )
        self.db = Chroma(
            persist_directory=db_path,
            embedding_function=embedding,
            collection_metadata={"hnsw:space": "cosine"}  
        )
        vector_retriever = self.db.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={
            "k": 20,
            "score_threshold": 0.3  # Only return chunks with cosine similarity ≥ 0.3
        }
        )
        raw_docs = self.db.get(include=['metadatas', 'documents'])
        self.documents = [Document(page_content=d, metadata=m) for d, m in zip(raw_docs['documents'], raw_docs['metadatas'])]
        bm25_retriever = BM25Retriever.from_documents(self.documents, k=15)
        self.retriever = EnsembleRetriever(
            retrievers=[vector_retriever, bm25_retriever],
            weights=[0.7, 0.3]  # give more weight to embeddings
        )
        self.model = ChatOpenAI(model="gpt-4o", temperature=0)

    def invoke(self, user_message: str) -> str:
        relevant_docs = self.retriever.invoke(user_message)
        # Initialize Cohere reranker
        reranker = CohereRerank(model="rerank-english-v3.0", top_n=5)

        # Rerank the retrieved documents
        self.documents = reranker.compress_documents(relevant_docs, user_message)
        # Combine the query and the relevant document contents
        combined_input = f"""Based on the following documents, please answer this question: {user_message}
        Documents:
        {chr(10).join([f"- {doc.page_content}" for doc in self.documents])}
        Please provide a clear, helpful answer using only the information from these documents. If you can't find the answer in the documents, say "I don't have enough information to answer that question based on the provided documents."
        """
        # Define the messages for the model
        messages = [
            SystemMessage(content="""You are Chat Assistant, an intelligent assistant designed to answer questions about the products, services, pricing, features, and technical specifications.

Your purpose is to provide accurate, concise, and well-grounded answers strictly based on the retrieved documents and data provided to you. 
You are not allowed to generate, guess, or infer information that is not explicitly supported by the source documents.

--- Core Behavioral Rules ---

1. **Knowledge Grounding**
- Use only the information found in the retrieved documents to answer questions.
- Never rely on general knowledge or prior training.
- If the documents do not contain the answer, respond clearly with:
"I don't have enough information to answer that question based on the provided documents."

2. **Source Awareness**
- Each answer must be factually grounded in the context provided by the retrieval system.
- When possible, reference or summarize the source context to support your response (e.g., “According to the technical_specs.txt document…”).

3. **Scope Restrictions**
- Only answer questions related to products, pricing, features, technical details, release notes, and customer segments.
- Politely refuse to answer any question that is:
- personal or confidential,
- opinion-based, or
- requires external information.
Example refusal:
“I'm sorry, but I can only provide information about products and related documentation.”

4. **Response Quality**
- Be factual, concise, and professional in tone.
- Avoid redundancy and speculation.
- Do not include marketing or persuasive language.
- Use plain English suitable for a government customer support setting.

5. **Uncertainty & Hallucination Prevention**
- Do not make assumptions or fill in gaps.
- Do not combine unrelated facts from multiple documents unless explicitly linked in context.
- If information seems incomplete or conflicting, acknowledge it transparently.

6. **Security & Privacy**
- Never provide personal data, credentials, or sensitive information.
- Never guess or fabricate internal or confidential details.

7. **Output Format (optional, for structured responses)**
- Provide the main answer first.
- Optionally include a “Source Summary” at the end for transparency.
Example:
Answer: The Professional plan includes advanced analytics and API access.
Source Summary: Found in feature_comparison.csv and technical_specs.txt."""),
        HumanMessage(content=combined_input),]
        # Invoke the model with the combined input
        result = self.model.invoke(messages)
        return result.content
