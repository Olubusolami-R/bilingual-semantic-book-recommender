from langchain.text_splitter import CharacterTextSplitter
from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
import pandas as pd

def load_books(csv_path="books_cleaned.csv"):
    return pd.read_csv(csv_path)

def build_vector_db(books):
    raw_documents = [
        Document(page_content=row)
        for row in books["tagged_description"].astype(str)
    ]

    text_splitter = CharacterTextSplitter(
        chunk_size=5000,
        chunk_overlap=0,
        separator="\n"
    )

    documents = text_splitter.split_documents(raw_documents)

    embeddings = OpenAIEmbeddings()

    db_books=Chroma.from_documents(
        documents,
        embedding=embeddings
    )
    return db_books