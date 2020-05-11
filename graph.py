import sys
import subprocess

from neo4j import GraphDatabase
from pprint import pprint
from dig import dig

gdb = GraphDatabase.driver("bolt://localhost:7687", auth=("", ""))

# Pre-condition: data (tree - dict/list/str), parent_id (ID of parent node)


def format_str(x): x.replace("\\n", " ") \
        .replace("\\", "\\\\") \
        .replace("'", "\\'") \
        .replace('"', '\\"')


def insert(data, parent_id):
    if(isinstance(data, dict)):
        for k, v in data.items():
            query = "MATCH (p:Node) WHERE ID(p)=" \
                + str(parent_id) \
                + " MERGE (p)-[:CHILD]->(a:Node {data: '" \
                + format_str(k) \
                + "'}) RETURN ID(a)"

            node_id = session.run(query).single().value()
            insert(v, node_id)

    if(isinstance(data, list)):
        for a in data:
            insert(a, parent_id)

    if(isinstance(data, str)):
        query = "MATCH (p:Node) WHERE ID(p)=" \
            + str(parent_id) \
            + " MERGE (p)-[:CHILD]->(a:Node {data: '" \
            + format_str(data) + "'})"
        session.run(query)


with gdb.session() as session:
    d = {}
    title = ''

    if(len(sys.argv) == 1):
        print("Specify manual to load")
        sys.exit(0)

    output = subprocess.run(("mman -Thtml "
                             + sys.argv[1]
                             + " | cat").split(" "), stdout=subprocess.PIPE)
    output = output.stdout.decode("utf-8")

    data = dig(output, session)
    d = dict(data.final)
    title = data.title
    pprint(d)

    parent_id = session.run("MERGE (p:Node{data:'"
                            + format_str(title)
                            + "'}) RETURN ID(p)").single().value()

    insert(d, parent_id)
