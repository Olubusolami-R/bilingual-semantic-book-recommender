from internal.gradio_ui import create_ui
from internal.embeddings import load_books, build_vector_db
from dotenv import load_dotenv
load_dotenv()

books = load_books()
db_books = build_vector_db(books)

app = create_ui(books, db_books)

if __name__ == "__main__":
    app.launch()