import os
import pandas as pd
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import TextLoader, DirectoryLoader, UnstructuredMarkdownLoader, UnstructuredHTMLLoader, CSVLoader, UnstructuredCSVLoader
from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from dotenv import load_dotenv

load_dotenv()
docs_path = "docs"
chroma_db_path = "db/chroma_db"
model_name = 'sentence-transformers/all-MiniLM-L6-v2'
model_kwargs = {"device": "cpu"}
encode_kwargs = {"normalize_embeddings": False}

embedding = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs,
)

def load_documents(docs_path=docs_path):
    """Load all text files from the docs directory"""
    print(f"Loading documents from {docs_path}...")
    
    # Check if docs directory exists
    if not os.path.exists(docs_path):
        raise FileNotFoundError(f"The folder {docs_path} does not exist. Please create it and add your source files.")
    
    documents = []

    # TXT files
    txt_loader = DirectoryLoader(path=docs_path, glob="*.txt", loader_cls=TextLoader)
    documents += txt_loader.load()

    # Markdown files
    md_loader = DirectoryLoader(path=docs_path, glob="*.md", loader_cls=UnstructuredMarkdownLoader)
    documents += md_loader.load()

    # HTML files
    html_loader = DirectoryLoader(path=docs_path, glob="*.html", loader_cls=UnstructuredHTMLLoader)
    documents += html_loader.load()

    # CSV files
    csv_loader = DirectoryLoader(path=docs_path, glob="*.csv", loader_cls=UnstructuredCSVLoader, loader_kwargs={"mode": "single"})
    csv_docs = csv_loader.load()
    for doc in csv_docs:
        doc.metadata["is_csv"] = True
    documents += csv_docs

    if len(documents) == 0:
        raise FileNotFoundError(f"No .txt files found in {docs_path}. Please add your source files.")
    
    for i, doc in enumerate(documents[:2]):  # Show first 2 documents
        print(f"\nDocument {i+1}:")
        print(f"  Source: {doc.metadata['source']}")
        print(f"  Content length: {len(doc.page_content)} characters")
        print(f"  Content preview: {doc.page_content[:100]}...")
        print(f"  metadata: {doc.metadata}")
        print(f"  is_csv: {doc.metadata.get("is_csv")}")

    return documents

def split_documents(documents, chunk_size=1000, chunk_overlap=100):
    """Split documents into smaller chunks with overlap"""
    print("Splitting documents into chunks...")
    
    recursive_splitter = RecursiveCharacterTextSplitter(
    separators=["\n\n", "\n", ". ", " ", ""],  # Multiple separators
    chunk_size=chunk_size,
    chunk_overlap=chunk_overlap
)
    non_csv_docs = [d for d in documents if not d.metadata.get("is_csv", False)]
    print("************non_csv_docs**************", non_csv_docs)
    csv_docs = [d for d in documents if d.metadata.get("is_csv", False)]

    chunks = recursive_splitter.split_documents(non_csv_docs)  
    all_docs = chunks + csv_docs
    print("chunks:", all_docs)
    return all_docs

def create_vector_store(chunks, chroma_db_path="../db/chroma_db"):
    """Create and persist ChromaDB vector store"""
    print("Creating embeddings and storing in ChromaDB...")
        
    # Create ChromaDB vector store
    print("--- Creating vector store ---")
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embedding,
        persist_directory=chroma_db_path, 
        collection_metadata={"hnsw:space": "cosine"}
    )
    print("--- Finished creating vector store ---")
    
    print(f"Vector store created and saved to {chroma_db_path}")
    return vectorstore

def main():
    """Data Ingestion Pipeline"""

    # Check if vector store already exists
    if os.path.exists(chroma_db_path):
        print("Vector store already exists. No need to re-process documents.")
        
        vectorstore = Chroma(
            persist_directory=chroma_db_path,
            embedding_function=embedding, 
            collection_metadata={"hnsw:space": "cosine"}
        )
        print(f"Loaded existing vector store with {vectorstore._collection.count()} chunks")
        return vectorstore
    
    print("Persistent directory does not exist. Initializing vector store...\n")
    
    # Step 1: Load documents
    documents = load_documents(docs_path)  

    # Step 2: Split into chunks
    chunks = split_documents(documents)
    
    # # Step 3: Create vector store
    vectorstore = create_vector_store(chunks, chroma_db_path)
    
    print("\n Ingestion complete! Your documents are now ready for RAG queries.")
    return vectorstore

if __name__ == "__main__":
    main()