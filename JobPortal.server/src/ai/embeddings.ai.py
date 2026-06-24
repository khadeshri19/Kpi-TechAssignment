import logging
from typing import Optional, Any

logger = logging.getLogger(__name__)

# Try to import sentence-transformers and numpy
try:
    from sentence_transformers import SentenceTransformer
    import numpy as np
    HAS_SENTENCE_TRANSFORMERS = True
except ImportError:
    HAS_SENTENCE_TRANSFORMERS = False
    logger.warning("sentence-transformers or numpy not installed. Falling back to keyword-based matching.")

_model_instance = None

def get_sentence_transformer() -> Optional[Any]:
    """
    Lazy-loads and returns the sentence transformer model.
    """
    global _model_instance
    if not HAS_SENTENCE_TRANSFORMERS:
        return None
    if _model_instance is None:
        try:
            # Load the lightweight, high-performance all-MiniLM-L6-v2 model locally
            _model_instance = SentenceTransformer('all-MiniLM-L6-v2')
        except Exception as e:
            logger.error(f"Failed to load SentenceTransformer: {str(e)}")
            _model_instance = None
    return _model_instance

def encode_text(text: str) -> Optional[Any]:
    """
    Encodes free-text into a vector embedding using sentence-transformers.
    """
    model = get_sentence_transformer()
    if not model:
        return None
    try:
        return model.encode(text)
    except Exception as e:
        logger.error(f"Error encoding text: {str(e)}")
        return None
