
import numpy as np
import faiss
import json
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any, Tuple

class FAQSemanticSearch:
    def __init__(self, model_path: str, index_path: str, metadata_path: str):
        """Initialize the semantic search system"""
        print("Loading semantic search system...")
        
        # Load sentence transformer
        self.model = SentenceTransformer(model_path)
        
        # Load FAISS index
        self.index = faiss.read_index(index_path)
        
        # Load metadata
        with open(metadata_path, 'r') as f:
            self.metadata = json.load(f)
            
        print(f"✅ Loaded {self.index.ntotal} FAQs for semantic search")
    
    def search(self, query: str, top_k: int = 5, min_score: float = 0.3) -> List[Dict[str, Any]]:
        """Search for relevant FAQs"""
        # Generate query embedding
        query_embedding = self.model.encode([query])
        query_normalized = query_embedding / np.linalg.norm(query_embedding)
        
        # Search index
        scores, indices = self.index.search(query_normalized.astype('float32'), top_k)
        
        # Format results
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if score >= min_score and idx < len(self.metadata):
                result = self.metadata[idx].copy()
                result['similarity_score'] = float(score)
                result['source'] = 'semantic_search'
                results.append(result)
        
        return results
    
    def get_best_answer(self, query: str, confidence_threshold: float = 0.7) -> Dict[str, Any]:
        """Get the best answer for a query"""
        results = self.search(query, top_k=1)
        
        if results and results[0]['similarity_score'] >= confidence_threshold:
            return {
                'answer': results[0]['answer'],
                'confidence': results[0]['similarity_score'],
                'source': 'faq_direct',
                'question': results[0]['question'],
                'category': results[0]['category']
            }
        else:
            return {
                'answer': None,
                'confidence': results[0]['similarity_score'] if results else 0.0,
                'source': 'low_confidence',
                'needs_human_support': True
            }
