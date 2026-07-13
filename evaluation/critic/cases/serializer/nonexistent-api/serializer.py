from case_uco import CASEGraph

def build():
    graph = CASEGraph()
    # Nonexistent SDK API — should trigger CRIT-S-PY-NONEXISTENT-API
    graph.add_node({"@id": "kb:x"})
    return graph
