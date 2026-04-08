from collections import defaultdict
from app.llm import ask_llm

graph = defaultdict(list)


def add_relation(entity1: str, entity2: str):
    graph[entity1].append(entity2)


def get_relations(entity: str):
    return graph.get(entity, [])


def get_graph():
    return dict(graph)


def extract_relations(text: str):
    prompt = f"""
Extract relationships from the following text.

Return them as pairs in this format:
entity1 -> entity2

Text:
{text}
"""

    response = ask_llm(prompt)

    relations = []

    for line in response.split("\n"):
        if "->" in line:
            parts = line.split("->")
            if len(parts) == 2:
                e1 = parts[0].strip()
                e2 = parts[1].strip()
                relations.append((e1, e2))

    return relations