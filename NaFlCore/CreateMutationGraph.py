import networkx as nx
from subprocess import check_call
from uuid import uuid4

def createMutationGraph(*queues):
    G = nx.DiGraph()
    G.add_node("INIT")

    for queue in queues:
        for file in queue.queue:
            if file.bitmap == None:
                G.add_edge("INIT", file.id)

            for des in file.descendants:
                    G.add_edge(file.id, des.id)

    unique = uuid4()
    nx.nx_pydot.write_dot(G,'mgraph%s.dot' % (unique))
    check_call(['dot','-Tpng','mgraph%s.dot' % (unique),'-o','mgraph%s.png' % unique])