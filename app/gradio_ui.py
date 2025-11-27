import gradio as gr
from search import retrieve_relevant_books

def format_results(df):
    if df.empty:
        return "<p>No results found.</p>"

    html = ""
    for _, row in df.iterrows():
        title = row["title"]
        isbn = row["isbn13"]
        desc = row["tagged_description"]
        cover_url = f"https://covers.openlibrary.org/b/isbn/{isbn}-M.jpg"

        html += f"""
        <div style="
            border: 1px solid #ddd;
            padding: 10px;
            border-radius: 8px;
            margin-bottom: 18px;
            display: flex;
            gap: 12px;
        ">
            <img src="{cover_url}" alt="cover image"
                style="width: 110px; height: auto; border-radius: 4px; border: 1px solid #ccc;">
            <div style="flex: 1;">
                <h3 style="margin-bottom: 4px;">{title}</h3>
                <p><strong>ISBN:</strong> {isbn}</p>
                <p style="margin-top: 6px; line-height: 1.4;">{desc}</p>
            </div>
        </div>
        """
    return html


def gradio_search(query, k=3, translate_checkbox=True):
    df = retrieve_relevant_books(query, k=int(k), translate=bool(translate_checkbox))
    if df.empty:
        return "No matches found."
    return format_results(df)


def create_ui():
    """Return a Gradio Blocks app without launching it."""
    with gr.Blocks() as app:
        gr.Markdown("## Bilingual Book Search (Yoruba and English) on English Books")

        with gr.Row():
            txt = gr.Textbox(
                label="Enter your query (Yoruba or English)",
                placeholder="e.g. ìtàn ìfẹ́"
            )
            k = gr.Slider(
                minimum=1, maximum=10, step=1, value=3,
                label="Number of results (k)"
            )
            translate_cb = gr.Checkbox(
                value=True,
                label="Translate query (Yoruba → English)"
            )

        out = gr.HTML(label="<h3>Search Results</h3>")
        btn = gr.Button("Search")

        btn.click(
            gradio_search,
            inputs=[txt, k, translate_cb],
            outputs=out
        )

    return app