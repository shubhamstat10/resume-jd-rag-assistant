from langchain_huggingface import HuggingFaceEmbeddings


def get_embedding_model():

    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    return embedding_model


if __name__ == "__main__":

    model = get_embedding_model()

    text = "Python, SQL, Machine Learning and Statistics"

    vector = model.embed_query(text)

    print("Embedding dimension:", len(vector))
    print("First 10 values:", vector[:10])