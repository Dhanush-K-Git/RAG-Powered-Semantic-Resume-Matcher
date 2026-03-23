import os
import chromadb
from sentence_transformers import SentenceTransformer
from resume_parser import extract_text_from_pdf

def run_indexing():
    """Function to process all resumes and RESET the database memory"""
    model = SentenceTransformer('all-MiniLM-L6-v2')
    client = chromadb.PersistentClient(path="./resume_vault")
    
    # 1. THE ERASER: Delete the old collection to remove "Ghost" resumes
    try:
        client.delete_collection(name="resumes")
    except:
        pass # If it doesn't exist yet, that's fine
    
    # 2. THE FRESH START: Create a brand new, empty collection
    collection = client.create_collection(name="resumes")

    resume_dir = "data/resumes"
    if not os.path.exists(resume_dir):
        return "No resumes found to index."

    count = 0
    for filename in os.listdir(resume_dir):
        if filename.endswith(".pdf"):
            file_path = os.path.join(resume_dir, filename)
            text = extract_text_from_pdf(file_path)
            
            # Indexing into ChromaDB
            collection.add(
                documents=[text],
                ids=[filename]
            )
            count += 1
    
    return f"Successfully indexed {count} resumes!"