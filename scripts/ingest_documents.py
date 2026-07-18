from ingestion.embedder import EmbeddingModel

embedding_model = EmbeddingModel()

embeddings = embedding_model.get_embeddings()

vector = embeddings.embed_query("Hello World")

print(len(vector))