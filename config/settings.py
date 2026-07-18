from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent

PDF_DIRECTORY = BASE_DIR / "data" / "policies"

CHROMA_DB_PATH = BASE_DIR / "data" / "chroma_db"


CHUNK_SIZE = 800
CHUNK_OVERLAP = 150

TOP_K = 5
SIMILARITY_THRESHOLD = 0.75

EMBEDDING_MODEL = "embed-english-v3.0"
LLM_MODEL = "llama-3.3-70b-versatile"
COHERE_API_KEY = os.getenv("COHERE_API_KEY")