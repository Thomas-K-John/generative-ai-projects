import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import mlflow
import pandas as pd
from langchain_chroma import Chroma
from langchain.schema import Document
from ragas import evaluate
from ragas.metrics import (context_precision, context_recall, faithfulness)
from datasets import Dataset
from src.rag_injestion import load_documents, split_documents
from src.rag_injestion import main as rag_injestion_main
from src.rag_retrieval import HybridRAGRetrieverModel

mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000"))
mlflow.set_experiment(os.getenv("MLFLOW_EXPERIMENT_NAME", "test_rag_1"))
mlflow.langchain.autolog(log_traces=True)

def main_execution():
    print("Running 'rag_injestion' from test...")
    rag_injestion_main()

@mlflow.trace(name="test_q1")
def test_q1(rag_retriever: HybridRAGRetrieverModel):
    """Evaluate Q1"""
    
    question = """Question 1"""
    generated_answer = rag_retriever.invoke(question)
    retrieved_documents = [doc.page_content for doc in rag_retriever.documents]
    correct_answer = """Ground truth answer for question 1""" 
    evaluation_data = {"question": [question],
                    "contexts": [retrieved_documents],
                    "answer":[generated_answer],
                    "reference": [correct_answer] }
    dataset = Dataset.from_dict(evaluation_data)
    scores = evaluate(dataset, metrics=[context_precision, context_recall, faithfulness])
    mlflow.update_current_trace(
    tags={
        "user_query": question,
        "llm_response": generated_answer,
        "context_precision": f"{scores['context_precision'][0]:.4f}",
        "context_recall": f"{scores['context_recall'][0]:.4f}",
        "faithfulness": f"{scores['faithfulness'][0]:.4f}"
    }
    )
    return scores

@mlflow.trace(name="test_q2")
def test_q2(rag_retriever: HybridRAGRetrieverModel):
    """Evaluate Q2"""
    
    question = """Question 2"""
    generated_answer = rag_retriever.invoke(question)
    retrieved_documents = [doc.page_content for doc in rag_retriever.documents]
    correct_answer = """Ground truth answer for question 2""" 
    evaluation_data = {"question": [question],
                    "contexts": [retrieved_documents],
                    "answer":[generated_answer],
                    "reference": [correct_answer] }
    dataset = Dataset.from_dict(evaluation_data)
    scores = evaluate(dataset, metrics=[context_precision, context_recall, faithfulness])
    mlflow.update_current_trace(
    tags={
        "user_query": question,
        "llm_response": generated_answer,
        "context_precision": f"{scores['context_precision'][0]:.4f}",
        "context_recall": f"{scores['context_recall'][0]:.4f}",
        "faithfulness": f"{scores['faithfulness'][0]:.4f}"
    }
    )
    return scores

@mlflow.trace(name="test_q3")
def test_q3(rag_retriever: HybridRAGRetrieverModel):
    """Evaluate Q3"""

    question = """Question 3"""
    generated_answer = rag_retriever.invoke(question)
    retrieved_documents = [doc.page_content for doc in rag_retriever.documents]
    correct_answer = """Ground truth answer for question 2""" 
    evaluation_data = {"question": [question],
                    "contexts": [retrieved_documents],
                    "answer":[generated_answer],
                    "reference": [correct_answer] }
    dataset = Dataset.from_dict(evaluation_data)
    scores = evaluate(dataset, metrics=[context_precision, context_recall, faithfulness])
    mlflow.update_current_trace(
    tags={
        "user_query": question,
        "llm_response": generated_answer,
        "context_precision": f"{scores['context_precision'][0]:.4f}",
        "context_recall": f"{scores['context_recall'][0]:.4f}",
        "faithfulness": f"{scores['faithfulness'][0]:.4f}"
    }
    )
    return scores

if __name__ == "__main__":
    main_execution()

    with mlflow.start_run(run_name="RAG_Eval_Session"):
        rag_retriever = HybridRAGRetrieverModel(db_path="db/chroma_db")
        results = [test_q1,test_q2,test_q3]

        # Aggregate across all test scores
        aggregated = {
            "context_precision_mean": sum(float(r["context_precision"][0]) for r in results) / len(results),
            "context_recall_mean": sum(float(r["context_recall"][0]) for r in results) / len(results),
            "faithfulness_mean": sum(float(r["faithfulness"][0]) for r in results) / len(results)
        }
        mlflow.log_metrics(aggregated)




