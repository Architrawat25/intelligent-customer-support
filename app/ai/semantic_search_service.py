import os
import json
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path

# Only import if available (graceful degradation)
try:
    from sentence_transformers import SentenceTransformer
    import faiss
    import numpy as np
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False

logger = logging.getLogger(__name__)

class SemanticSearchService:
    """Production-ready semantic search service with fallback"""

    def __init__(self, data_dir: str = "app/data"):
        self.data_dir = Path(data_dir)
        self.model = None
        self.index = None
        self.metadata = []
        self.is_initialized = False

        if AI_AVAILABLE:
            try:
                self._load_components()
                self.is_initialized = True
                logger.info("✅ Semantic search initialized successfully")
            except Exception as e:
                logger.error(f"❌ Failed to initialize semantic search: {e}")
                self.is_initialized = False
        else:
            logger.warning("⚠️ AI libraries not available, using fallback mode")

    def _load_components(self):
        """Load all AI components"""
        # Load sentence transformer
        model_path = self.data_dir / "models" / "sentence_transformer"
        if not model_path.exists():
            raise FileNotFoundError(f"Model not found at {model_path}")

        self.model = SentenceTransformer(str(model_path))
        logger.info(f"Loaded SentenceTransformer from {model_path}")

        # Load FAISS index
        index_path = self.data_dir / "models" / "faiss_index.bin"
        if not index_path.exists():
            raise FileNotFoundError(f"FAISS index not found at {index_path}")

        self.index = faiss.read_index(str(index_path))
        logger.info(f"Loaded FAISS index with {self.index.ntotal} vectors")

        # Load metadata
        metadata_path = self.data_dir / "data" / "faq_metadata.json"
        if not metadata_path.exists():
            raise FileNotFoundError(f"Metadata not found at {metadata_path}")

        with open(metadata_path, 'r') as f:
            self.metadata = json.load(f)
        logger.info(f"Loaded {len(self.metadata)} FAQ metadata entries")

    def search_faqs(
            self,
            query: str,
            top_k: int = 5,
            min_score: float = 0.3
    ) -> List[Dict[str, Any]]:
        """Search for relevant FAQs"""
        if not self.is_initialized:
            logger.warning("Semantic search not available, returning empty results")
            return []

        try:
            # Generate query embedding
            query_embedding = self.model.encode([query])
            query_normalized = query_embedding / np.linalg.norm(query_embedding)

            # Search index
            scores, indices = self.index.search(
                query_normalized.astype('float32'),
                top_k
            )

            # Format results
            results = []
            for score, idx in zip(scores[0], indices[0]):
                if score >= min_score and idx < len(self.metadata):
                    result = self.metadata[idx].copy()
                    result['similarity_score'] = float(score)
                    result['source'] = 'semantic_search'
                    results.append(result)

            logger.info(f"Found {len(results)} relevant FAQs for query: {query[:50]}...")
            return results

        except Exception as e:
            logger.error(f"Error in semantic search: {e}")
            return []

    def get_best_answer(
            self,
            query: str,
            confidence_threshold: float = 0.7
    ) -> Dict[str, Any]:
        """Get the best answer for a query"""
        if not self.is_initialized:
            return self._fallback_response()

        results = self.search_faqs(query, top_k=1)

        if results and results[0]['similarity_score'] >= confidence_threshold:
            return {
                'answer': results[0]['answer'],
                'confidence': results[0]['similarity_score'],
                'source': 'faq_direct',
                'question': results[0]['question'],
                'category': results[0]['category'],
                'faq_id': results[0]['id']
            }
        else:
            return {
                'answer': self._generate_fallback_answer(query, results),
                'confidence': results[0]['similarity_score'] if results else 0.0,
                'source': 'low_confidence' if results else 'no_match',
                'needs_human_support': True,
                'related_faqs': results[:3] if results else []
            }

    def _generate_fallback_answer(self, query: str, results: List[Dict]) -> str:
        """Generate a fallback answer when confidence is low"""
        if results:
            return f"I found some related information, but I'm not fully confident in the answer. You might find these topics helpful: {', '.join([r['category'] for r in results[:2]])}. For the most accurate assistance, please contact our support team."
        else:
            return "I couldn't find specific information about your question in our knowledge base. Please contact our support team for personalized assistance."

    def _fallback_response(self) -> Dict[str, Any]:
        """Fallback when AI is not available"""
        return {
            'answer': "I apologize, but our AI-powered search is currently unavailable. Please contact our support team for assistance.",
            'confidence': 0.0,
            'source': 'system_unavailable',
            'needs_human_support': True
        }

    def is_available(self) -> bool:
        """Check if semantic search is available"""
        return self.is_initialized

# Global instance with lazy loading
_search_service = None

def get_search_service() -> SemanticSearchService:
    """Get singleton search service instance"""
    global _search_service
    if _search_service is None:
        _search_service = SemanticSearchService()
    return _search_service
