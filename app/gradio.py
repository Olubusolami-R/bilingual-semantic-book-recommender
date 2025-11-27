import gradio as gr

def gradio_search(query, k=3, translate_checkbox=True):
    # optionally force translation by checkbox
    df = retrieve_relevant_books_simple(query, k=int(k), translate=bool(translate_checkbox))
    if df.empty:
        return "No matches found."
    return format_results(df)

with gr.Blocks() as app:
    gr.Markdown("## Bilingual Book Search (Yoruba and English) on English Books")
    with gr.Row():
        txt = gr.Textbox(label="Enter your query (Yoruba or English)", placeholder="e.g. ìtàn ìfẹ́")
        k = gr.Slider(minimum=1, maximum=10, step=1, value=3, label="Number of results (k)")
        translate_cb = gr.Checkbox(value=True, label="Translate query (Yoruba → English)")
    out = gr.HTML(label="<h3>Search Results</h3>")
    btn = gr.Button("Search")
    btn.click(gradio_search, inputs=[txt, k, translate_cb], outputs=out)

app.launch()