from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_community.embeddings import FakeEmbeddings

PERSIST_DIR = "app/vectorstore"


def load_vector_store():
    embeddings = FakeEmbeddings(size=384)
    vectordb = Chroma(
        persist_directory=PERSIST_DIR,
        embedding_function=embeddings
    )
    return vectordb


def initialize_vector_store():
    """
    Load dummy FAQ / support articles into vector DB
    """
    documents = [
        Document(
            page_content="To reset your password, go to settings and click on 'Reset Password'.",
            metadata={"source": "faq_password"}
        ),
        Document(
            page_content="Refunds are processed within 5-7 business days after approval.",
            metadata={"source": "faq_refund"}
        ),
        Document(
            page_content="For internet issues, restart your router and contact support if issue persists.",
            metadata={"source": "faq_internet"}
        ),
    ]

    embeddings = FakeEmbeddings(size=384)

    vectordb = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=PERSIST_DIR
    )

    vectordb.persist()
    return vectordb


def search_knowledge_base(query: str):
    vectordb = load_vector_store()
    results = vectordb.similarity_search(query, k=2)

    if not results:
        return "No relevant knowledge found."

    return [doc.page_content for doc in results]
