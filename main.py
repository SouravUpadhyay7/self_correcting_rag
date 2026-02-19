from app.graph.workflow import build_graph

app = build_graph()

result = app.invoke({
    "question": "What is Self-RAG?"
})

print(result)
