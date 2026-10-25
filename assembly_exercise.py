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
    stack = [start]

    while stack:
        v = stack.pop()
        if v not in visited:
            visited.add(v)
            order.append(v)
            # Push neighbours in reverse sorted order so that the smallest
            # neighbour is popped and processed first (matching sorted DFS order)
            for neighbour in sorted(graph.get(v, []), reverse=True):
                if neighbour not in visited:
                    stack.append(neighbour)

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
    # Maintain a copy of unused outgoing edges sorted alphabetically
    unused = {node: sorted(neighbours) for node, neighbours in graph.items()}

    # Total edges in the graph to check termination easily
    total_edges = sum(len(neighbours) for neighbours in graph.values())
    used_edges = 0

    # Step 1: Initial walk from the designated start node
    walk = [start]
    curr = start
    while curr in unused and unused[curr]:
        # Always take the edge whose end node comes first alphabetically
        next_node = unused[curr].pop(0)
        walk.append(next_node)
        used_edges += 1
        curr = next_node

    if verbose:
        print(f"Walk 1: {' -> '.join(walk)}")

    # Steps 2, 3, 4: Splicing sub-walks until every edge is used
    while used_edges < total_edges:
        # Step 3: Traverse the current walk from its first node,
        # stopping at the first position whose node still has an unused edge.
        restart_idx = None
        restart_node = None
        for i, node in enumerate(walk):
            if node in unused and len(unused[node]) > 0:
                restart_idx = i
                restart_node = node
                break

        # Sub-walk starting from restart_node
        sub_walk = [restart_node]
        curr = restart_node
        while curr in unused and unused[curr]:
            next_node = unused[curr].pop(0)
            sub_walk.append(next_node)
            used_edges += 1
            curr = next_node

        if verbose:
            print(f"Restart at '{restart_node}': {' -> '.join(sub_walk)}")

        # Step 4: Splice the sub_walk into walk at restart_idx (replacing only that occurrence)
        # Note: sub_walk starts and ends at restart_node.
        walk = walk[:restart_idx] + sub_walk + walk[restart_idx + 1:]

        if verbose:
            print(f"After splice: {' -> '.join(walk)}")

    return walk


def eulerian_path(graph, verbose=False):
    # Calculate in-degrees and out-degrees across the graph
    in_deg = {v: 0 for v in graph}
    out_deg = {v: len(neighbours) for v, neighbours in graph.items()}
    for neighbours in graph.values():
        for v in neighbours:
            in_deg[v] = in_deg.get(v, 0) + 1

    # In a directed Eulerian path, the start node must have out - in = +1.
    start_node = None
    for v in graph:
        if out_deg[v] - in_deg.get(v, 0) == 1:
            start_node = v
            break

    # If all nodes are balanced (Eulerian circuit), pick the alphabetically first node
    if start_node is None:
        start_node = min(graph.keys())

    return hierholzer(graph, start_node, verbose=verbose)

# TASK 4
def contigs(graph):
    # Compute in-degrees and out-degrees across all nodes
    in_deg = {v: 0 for v in graph}
    out_deg = {v: len(neighbours) for v, neighbours in graph.items()}
    for neighbours in graph.values():
        for v in neighbours:
            in_deg[v] = in_deg.get(v, 0) + 1

    # Track unused edges as sorted multiset/list copies so parallel edges are preserved
    # and edges are visited deterministically
    unused = {u: sorted(neighbours) for u, neighbours in graph.items()}

    contig_paths = []

    # Phase 1: Start at every node that is NOT 1-in-1-out
    # Sort nodes so traversal order is completely deterministic
    for node in sorted(graph.keys()):
        is_1_in_1_out = (in_deg.get(node, 0) == 1 and out_deg.get(node, 0) == 1)

        if not is_1_in_1_out:
            # Consume every outgoing edge from this non-1-in-1-out node
            while unused[node]:
                next_node = unused[node].pop(0)
                path = [node, next_node]
                curr = next_node

                # Follow path as long as the current node is 1-in-1-out
                while in_deg.get(curr, 0) == 1 and out_deg.get(curr, 0) == 1:
                    # An isolated 1-in-1-out loop on itself or continuing forward
                    if not unused[curr]:
                        break
                    next_step = unused[curr].pop(0)
                    path.append(next_step)
                    curr = next_step

                contig_paths.append(path)

    # Phase 2: Isolated cycles where EVERY node is 1-in-1-out
    # Find all remaining nodes that still have unused edges
    nodes_with_edges = {v for v, edges in unused.items() if edges}

    while nodes_with_edges:
        # 1. Identify all nodes in the connected component of the cycle
        cycle_nodes = set()
        stack = [next(iter(nodes_with_edges))]
        while stack:
            u = stack.pop()
            if u not in cycle_nodes:
                cycle_nodes.add(u)
                for v in unused[u]:
                    if v not in cycle_nodes:
                        stack.append(v)

        # 2. Per the rule: Start at the alphabetically first node in the cycle
        start_node = min(cycle_nodes)

        # 3. Trace the closed cycle until it returns to start_node
        cycle_path = [start_node]
        curr = start_node
        while True:
            next_node = unused[curr].pop(0)
            cycle_path.append(next_node)
            curr = next_node
            if curr == start_node:
                break

        contig_paths.append(cycle_path)

        # Refresh the remaining nodes with edges
        nodes_with_edges = {v for v, edges in unused.items() if edges}

    # Spell each path into its DNA sequence string and return sorted
    spelled_contigs = [spell_path(p) for p in contig_paths]
    return sorted(spelled_contigs)

# TASK 5
from collections import Counter
from Bio import SeqIO


# Ensure previous task functions (kmer_composition, debruijn_graph, spell_path,
# hierholzer, eulerian_path, eulerian_type, contigs) are imported or defined above.

def trim_cycle(seq, k):
    """
    Trims the repeated (k - 1) prefix at the end of a closed cycle/walk
    if it ends at the node where it started.
    """
    overlap = k - 1
    if len(seq) > overlap and seq.endswith(seq[:overlap]):
        return seq[:-overlap]
    return seq


def is_circular_equivalent(s, t):
    """Checks if two strings describe the same circular genome."""
    return len(s) == len(t) and s in (t + t)


def run_task5(fasta_file="reads.fasta"):
    # 1. Read error-free reads
    reads = [str(rec.seq) for rec in SeqIO.parse(fasta_file, "fasta")]

    k_values = [9, 12, 13, 14, 21]
    results = []

    print(
        f"{'k':<4} | {'|V|':<6} | {'|E|':<6} | {'eulerian_type':<13} | {'contigs':<8} | {'longest contig':<16} | {'spelled string':<16}")
    print("-" * 80)

    for k in k_values:
        # Step 3: Collect distinct k-mers from all reads
        kmers_set = set()
        for read in reads:
            for i in range(len(read) - k + 1):
                kmers_set.add(read[i:i + k])

        sorted_kmers = sorted(kmers_set)
        graph = debruijn_graph(sorted_kmers)

        # Graph statistics
        num_v = len(graph)
        num_e = sum(len(adj) for adj in graph.values())
        etype = eulerian_type(graph, directed=True)

        # Contig computation
        all_contigs = contigs(graph)
        num_contigs = len(all_contigs)

        # Trim contigs if they are closed cycles
        trimmed_contigs = [trim_cycle(c, k) for c in all_contigs]
        longest_contig_len = max(len(c) for c in trimmed_contigs) if trimmed_contigs else 0

        # Eulerian walk assembly (if applicable)
        spelled_trimmed = None
        spelled_len_str = "—"
        if etype != "none":
            walk = eulerian_path(graph)
            spelled = spell_path(walk)

            # Step 4: Self-checks for spelled string
            spelled_kmers = {spelled[i:i + k] for i in range(len(spelled) - k + 1)}
            assert spelled_kmers == kmers_set, f"k={k}: Spelled string k-mers do not match graph k-mers"
            assert len(spelled) == num_e + k - 1, f"k={k}: Spelled string length mismatch"

            # Step 5: Trim cycles
            spelled_trimmed = trim_cycle(spelled, k)
            spelled_len_str = str(len(spelled_trimmed))

        # Step 4: Self-check 1 on contig edges
        total_contig_edges = Counter()
        for c in all_contigs:
            for i in range(len(c) - k + 1):
                kmer = c[i:i + k]
                total_contig_edges[(kmer[:-1], kmer[1:])] += 1

        graph_edges = Counter((u, v) for u, neighbors in graph.items() for v in neighbors)
        assert total_contig_edges == graph_edges, f"k={k}: Contig edges do not partition graph edges"

        results.append({
            "k": k,
            "V": num_v,
            "E": num_e,
            "etype": etype,
            "num_contigs": num_contigs,
            "longest_contig": longest_contig_len,
            "spelled_trimmed": spelled_trimmed,
            "spelled_str": spelled_len_str
        })

        print(
            f"{k:<4} | {num_v:<6} | {num_e:<6} | {etype:<13} | {num_contigs:<8} | {longest_contig_len:<16} | {spelled_len_str:<16}")

    # Step 8: Circular sequence equivalence check
    valid_assemblies = [(r["k"], r["spelled_trimmed"]) for r in results if r["spelled_trimmed"] is not None]
    if valid_assemblies:
        base_k, base_seq = valid_assemblies[0]
        print("\nCircular equivalence check against k =", base_k, f"(length = {len(base_seq)}):")
        all_equal = True
        for k_val, seq in valid_assemblies[1:]:
            equivalent = is_circular_equivalent(base_seq, seq)
            print(f"  k={base_k} vs k={k_val}: {'Equivalent' if equivalent else 'NOT equivalent'}")
            if not equivalent:
                all_equal = False
        print(f"\nDo all spelled strings describe the same circle? {'Yes' if all_equal else 'No'}")


if __name__ == "__main__":
    run_task5("reads.fasta")
