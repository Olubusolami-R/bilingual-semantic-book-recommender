import pandas as pd
from embeddings import load_books, build_vector_db

books = load_books()
db_books = build_vector_db(books)

def retrieve_relevant_books(query, k=3):
    """
    Returns a dataframe of the top-k matching rows.
    """
    results = db_books.similarity_search(query, k=k)

    rows = []
    for item in results:
        # ISBN is first token
        isbn = item.page_content.split()[0].strip()
        try:
            isbn = int(isbn)
        except:
            continue

        match = books[books["isbn13"] == isbn]
        if not match.empty:
            rows.append(match)

    if not rows:
        return pd.DataFrame()

    return pd.concat(rows).drop_duplicates("isbn13").reset_index(drop=True)