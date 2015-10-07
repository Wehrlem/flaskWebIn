from pyorient import orient
import json
import networkx as nx
from networkx.readwrite import json_graph
files = [ "Badges", "Comments", "Posts", "Users", "Votes","Tags" ]
db_name = 'history'
client = orient.OrientDB("localhost", 2424)
client.db_open( db_name, "root", "don1664" )

def create_simmple_graph():
    results = client.query("select name AS user_name, ID ,in(knows).name AS concepts , inE(knows).strength AS strength, inE(knows).@rid as edgeid from Expert WHERE ID =10")
    G=nx.Graph()
    name= results[0].user_name
    G.add_node(name)
    for i,concepts in enumerate(results[0].concepts):
        G.add_node(concepts)
        G.add_weighted_edges_from([(name,concepts,results[0].strength[i])])
    data = json_graph.node_link_data(G)
    return json.dumps(data)

print create_simmple_graph()



