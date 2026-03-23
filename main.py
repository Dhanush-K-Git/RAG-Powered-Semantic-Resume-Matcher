import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
client = chromadb.PersistentClient(path="./resume_vault")

def rank_resumes(job_description_text):
    collection = client.get_or_create_collection(name="resumes")
    query_vector = model.encode([job_description_text]).tolist()

    results = collection.query(
        query_embeddings=query_vector,
        n_results=10, 
        include=["documents", "distances"]
    )

    temp_results = []
    if results['ids'] and results['ids'][0]:
        for i in range(len(results['ids'][0])):
            # Calculate raw score (higher is better)
            score_raw = (1 - results['distances'][0][i]) * 100 
            
            temp_results.append({
                "Candidate Name": results['ids'][0][i],
                "Score_Raw": score_raw, # Use this for sorting
                "Content": results['documents'][0][i]
            })

    # SORT NUMERICALLY: Ensure the 38% candidate beats the 4% candidate
    sorted_data = sorted(temp_results, key=lambda x: x['Score_Raw'], reverse=True)

    # Format for the UI
    final_output = []
    for r in sorted_data:
        final_output.append({
            "Candidate Name": r["Candidate Name"],
            "Match Score": f"{r['Score_Raw']:.2f}%",
            "Content": r["Content"]
        })

    return final_output