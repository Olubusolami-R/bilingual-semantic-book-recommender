import pandas as pd
from embeddings import load_books, build_vector_db
from translate import translate_yoruba_to_english

books = load_books()
db_books = build_vector_db(books)
def retrieve_relevant_books(query, k=3, translate=False):
    """
    Pipeline to:
      - detect language (langdetect)
      - if Yoruba (translate True), translate to English
      - run your existing db_books.similarity_search on the English query
      - return a single pandas.DataFrame of matched books (unique)
    """

    if translate:
        q_for_search = translate_yoruba_to_english(query)
    else:
        q_for_search = query

    # 2) run similarity search on your existing vector store
    results = db_books.similarity_search(q_for_search, k=k)

    # 3) convert Document results into a single DataFrame (same logic as earlier)
    rows = []

    for r in results:
        content = r.page_content.strip()
        isbn_str = content.split()[0]
        matched_df = pd.DataFrame()

        if isbn_str.isdigit():
            isbn = int(isbn_str)
            matched_df = books[books["isbn13"] == isbn]

        if matched_df.empty:
            snippet = content[:120].strip()
            matched_df = books[books["tagged_description"].str.contains(snippet, na=False)]

        if not matched_df.empty:
            rows.append(matched_df)

    if not rows:
        return pd.DataFrame()

    df = pd.concat(rows, ignore_index=True)
    if "isbn13" in df.columns:
        df = df.drop_duplicates(subset=["isbn13"]).reset_index(drop=True)
    return df