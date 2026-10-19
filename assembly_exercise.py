# TASK 2
def degrees(graph):
    degree = {}
    for v, line in graph.items():
        degree[v] = len(line)

    return degree

def in_out_degree(graph):
    in_degree = {v: 0 for v in graph}
    out_degree = {v: len(neighbours) for v, neighbours in graph.items()}

    for neighbours in graph.values():
        for v in neighbours:
            in_degree[v] += 1

    return in_degree, out_degree


def dfs(graph, start):
    visited = set()
    order = []

    def visit(v):
        visited.add(v)
        order.append(v)

        for neighbour in sorted(graph[v]):
            if neighbour not in visited:
                visit(neighbour)

    visit(start)
    return order

def connected_components(graph):
    visited = set()
    components = []

    for v in graph:
        if v not in visited:
            comp_order = dfs(graph, v)
            comp_set = set(comp_order)
            visited.update(comp_set)
            components.append(comp_set)

    return components

def is_weakly_connected(graph):
    if not graph:
        return True

    shadow = {v: [] for v in graph}
    for u, neighbours in graph.items():
        for v in neighbours:
            shadow[u].append(v)
            shadow[v].append(u)

    comps = connected_components(shadow)
    return len(comps) == 1


# TASK 4

def eulerian_type(graph, directed=False):
    if not graph:
        return "circuit"

    if directed:
        in_deg, out_deg = in_out_degree(graph)
        active_vertices = {v for v in graph if in_deg[v] > 0 or out_deg[v] > 0}
    else:
        deg = degrees(graph)
        active_vertices = {v for v in graph if deg[v] > 0}

    if not active_vertices:
        return "circuit"

    if directed:
        if not is_weakly_connected(graph):
            shadow = {v: [] for v in graph}
            for u, neighbours in graph.items():
                for v in neighbours:
                    shadow[u].append(v)
                    shadow[v].append(u)

            first_active = next(iter(active_vertices))
            active_comp = set(dfs(shadow, first_active))
            if not active_vertices.issubset(active_comp):
                return "none"
    else:
        comps = connected_components(graph)
        non_isolated_comps = [c for c in comps if any(deg[v] > 0 for v in c)]
        if len(non_isolated_comps) > 1:
            return "none"

    if not directed:
        deg = degrees(graph)
        odd_count = sum(1 for v in graph if deg[v] % 2 != 0)

        if odd_count == 0:
            return "circuit"
        elif odd_count == 2:
            return "path"
        else:
            return "none"

    else:
        in_deg, out_deg = in_out_degree(graph)
        start_nodes = 0
        end_nodes = 0

        for v in graph:
            diff = out_deg[v] - in_deg[v]
            if diff == 1:
                start_nodes += 1
            elif diff == -1:
                end_nodes += 1
            elif diff != 0:
                return "none"

        if start_nodes == 0 and end_nodes == 0:
            return "circuit"
        elif start_nodes == 1 and end_nodes == 1:
            return "path"
        else:
            return "none"

def kmer_composition(text, k):
    kmers = []
    for i in range(k):
        kmers.append(text[i:i +k])
    return kmers

#print(kmer_composition("GATTACA", 4))

def debruijn_graph(kmers):
    graph = {}

    for kmer in kmers:
        prefix = kmer[:-1]
        suffix = kmer[1:]

        if prefix not in graph:
            graph[prefix] = []

        if suffix not in graph:
            graph[suffix] = []

        graph[prefix].append(suffix)

    return graph

def spell_path(nodes):
    path = nodes[0]

    for node in nodes[1:]:
        path = path + node[-1]

    return path

def hierholzer(graph, start, verbose=False):
    unused = {node: sorted(neighbours) for node, neighbours in graph.items()}
    walk = [start]
    current = start




    return walk


def eulerian_path(graph, verbose=False):
    walk = []
