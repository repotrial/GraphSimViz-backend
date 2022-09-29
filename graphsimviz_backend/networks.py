import os


def get_data_dir():
    return "/usr/src/graphs/"


def get_network_dir(network1, network2):
    pre1 = network1.split('_')[0]
    pre2 = network2.split('_')[0]
    dir1 = os.path.join(get_data_dir(), f'{pre1}_{pre2}')
    if os.path.exists(dir1):
        return dir1
    dir2 = os.path.join(get_data_dir(), f'{pre2}_{pre1}')
    if os.path.exists(dir2):
        return dir2
    return None


def get_network_files(network1, network2, id_space):
    wd = get_network_dir(network1, network2)
    if wd is None:
        return None
    files = []
    id_space_prefix = 'mondo' if id_space == 'MONDO' else 'icd10'

    suffix = network1.split("_")[1]
    suffix = suffix + ('_based_pruned_below4lev.gt' if suffix == 'symptom' else '_based.gt')

    file1 = os.path.join(wd, f'{id_space_prefix}_{suffix}')
    print(file1)
    if os.path.exists(file1):
        files.append(file1)
    else:
        print(f"Error, file could not be found for network1: {network1}")
        return None

    suffix = network2.split("_")[1]
    suffix = suffix + ('_based_pruned_below4lev.gt' if suffix == 'symptom' else '_based.gt')

    file2 = os.path.join(wd, f'{id_space_prefix}_{suffix}')
    print(file2)
    if os.path.exists(file2):
        files.append(file2)
    else:
        print(f"Error, file could not be found for network2: {network2}")
        return None

    return files


def read_graph(file):
    import graph_tool as gt
    return gt.load_graph(file)


def get_subnetwork(nodes, file):
    from graph_tool.all import GraphView, Graph
    g = read_graph(file)
    filter = g.new_vertex_property('bool')
    for v in g.vertices():
        id = g.vp.ID[v]
        if id in nodes:
            filter[v] = True
    sub = GraphView(g, vfilt=filter)
    sub = Graph(sub, prune=True)
    node_map = dict()
    for v in sub.vertices():
        node_map[int(v)] = sub.vp.ID[v]
    edges = []
    for e in sub.edges():
        edges.append((int(e.source()), int(e.target())))
    out = {'nodes': node_map, 'edges': edges}

    return out


def get_networks(network1, network2, id_space, nodes):
    files = get_network_files(network1, network2, id_space)
    networks = []
    for file in files:
        networks.append(get_subnetwork(nodes, file))
    return networks
