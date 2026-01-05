from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_community.embeddings import FakeEmbeddings

def init_vector_db():
    embeddings = FakeEmbeddings(size=384)

    docs = [
        Document(page_content="If internet is not working, restart the router."),
        Document(page_content="For billing issues, contact the finance department."),
        Document(page_content="If login fails, reset your password.")
    ]

    vectordb = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory="app/vectorstore"
    )

    vectordb.persist()
    print("✅ Vector DB initialized successfully (FAKE embeddings)")

if __name__ == "__main__":
    init_vector_db()
