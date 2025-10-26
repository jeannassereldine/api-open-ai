
from graph.graph_excecutor import compile_graph


graph = compile_graph()


with open("graph.png", "wb") as f:
    f.write(graph.get_graph().draw_mermaid_png())