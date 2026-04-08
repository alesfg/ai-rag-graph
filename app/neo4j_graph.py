from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

load_dotenv()


class Neo4jGraph:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            os.getenv("NEO4J_URI"),
            auth=(os.getenv("NEO4J_USER"), os.getenv("NEO4J_PASSWORD"))
        )

    def close(self):
        self.driver.close()

    def add_relation(self, entity1, entity2):
        query = """
        MERGE (a:Entity {name: $e1})
        MERGE (b:Entity {name: $e2})
        MERGE (a)-[:RELATED_TO]->(b)
        """
        with self.driver.session() as session:
            session.run(query, e1=entity1, e2=entity2)

    def get_relations(self, entity):
        query = """
        MATCH (a:Entity {name: $name})-[:RELATED_TO]->(b)
        RETURN b.name AS related
        """
        with self.driver.session() as session:
            result = session.run(query, name=entity)
            return [record["related"] for record in result]