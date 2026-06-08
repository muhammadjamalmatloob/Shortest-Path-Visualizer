"""
algorithms.py
-------------
Shortest-path algorithm implementations that record every relaxation step.

Each public function returns: (path, cost, steps)
  - path  : list of node labels, or None if unreachable
  - cost  : numeric total cost, or an error string
  - steps : list of step dicts, each containing:
              type            – "init" | "visit" | "relax" | "final"
              message         – human-readable description
              dist_snapshot   – {node: dist_or_'INF'} at this moment
              relaxed_edges   – list of (u, v) tuples highlighted green
              visited         – set of visited nodes (Dijkstra / Bellman-Ford)
"""

import heapq


# ---------------------------------------------------------------------------
# Dijkstra
# ---------------------------------------------------------------------------

def dijkstra_with_steps(graph, start, end):
    steps = []
    dist = {n: float('inf') for n in graph.nodes()}
    prev = {n: None for n in graph.nodes()}
    dist[start] = 0
    pq = [(0, start)]
    visited = set()

    dist_snap = _snap(dist)
    steps.append({
        "type": "init",
        "message": f"Initialize: dist[{start}] = 0, all others = INF",
        "dist_snapshot": dict(dist_snap),
        "relaxed_edges": [],
        "visited": set(),
    })

    while pq:
        d, u = heapq.heappop(pq)
        if u in visited:
            continue
        visited.add(u)

        steps.append({
            "type": "visit",
            "node": u,
            "message": f"Visit node {u}  (dist = {d})",
            "dist_snapshot": dict(_snap(dist)),
            "relaxed_edges": [],
            "visited": set(visited),
        })

        for v in graph.successors(u):
            w = graph[u][v].get('weight', 1)
            if dist[u] + w < dist[v]:
                old = dist[v]
                dist[v] = dist[u] + w
                prev[v] = u
                heapq.heappush(pq, (dist[v], v))
                steps.append({
                    "type": "relax",
                    "edge": (u, v),
                    "message": (
                        f"Relax edge {u} -> {v}  (weight {w}):  "
                        f"dist[{v}] updated {('INF' if old == float('inf') else old)} -> {dist[v]}"
                    ),
                    "dist_snapshot": dict(_snap(dist)),
                    "relaxed_edges": [(u, v)],
                    "visited": set(visited),
                })

    if dist[end] == float('inf'):
        return None, "No path exists", steps

    path = _reconstruct(prev, end)
    steps.append({
        "type": "final",
        "message": f"Shortest path found: {' -> '.join(path)}  |  Total cost = {dist[end]}",
        "dist_snapshot": dict(_snap(dist)),
        "relaxed_edges": [],
        "path": path,
        "visited": set(visited),
    })
    return path, dist[end], steps


# ---------------------------------------------------------------------------
# Bellman-Ford
# ---------------------------------------------------------------------------

def bellman_ford_with_steps(graph, start, end):
    steps = []
    nodes = list(graph.nodes())
    edges = [(u, v, graph[u][v].get('weight', 1)) for u, v in graph.edges()]
    dist = {n: float('inf') for n in nodes}
    prev = {n: None for n in nodes}
    dist[start] = 0

    dist_snap = _snap(dist)
    steps.append({
        "type": "init",
        "message": f"Initialize: dist[{start}] = 0, all others = INF",
        "dist_snapshot": dict(dist_snap),
        "relaxed_edges": [],
        "visited": set(),
    })

    n = len(nodes)
    for iteration in range(n - 1):
        any_relaxed = False
        for u, v, w in edges:
            if dist[u] != float('inf') and dist[u] + w < dist[v]:
                old = dist[v]
                dist[v] = dist[u] + w
                prev[v] = u
                any_relaxed = True
                steps.append({
                    "type": "relax",
                    "edge": (u, v),
                    "message": (
                        f"Iteration {iteration + 1} — Relax {u} -> {v}  (weight {w}):  "
                        f"dist[{v}] {('INF' if old == float('inf') else old)} -> {dist[v]}"
                    ),
                    "dist_snapshot": dict(_snap(dist)),
                    "relaxed_edges": [(u, v)],
                    "visited": set(),
                })
        if not any_relaxed:
            steps.append({
                "type": "visit",
                "message": f"Iteration {iteration + 1} — No relaxations, early termination",
                "dist_snapshot": dict(_snap(dist)),
                "relaxed_edges": [],
                "visited": set(),
            })
            break

    # Check for negative-weight cycle
    for u, v, w in edges:
        if dist[u] != float('inf') and dist[u] + w < dist[v]:
            steps.append({
                "type": "final",
                "message": "Negative weight cycle detected! Algorithm cannot proceed.",
                "dist_snapshot": {},
                "relaxed_edges": [],
                "visited": set(),
            })
            return None, "Negative weight cycle detected!", steps

    if dist[end] == float('inf'):
        return None, "No path exists", steps

    path = _reconstruct(prev, end)
    steps.append({
        "type": "final",
        "message": f"Shortest path found: {' -> '.join(path)}  |  Total cost = {dist[end]}",
        "dist_snapshot": dict(_snap(dist)),
        "relaxed_edges": [],
        "path": path,
        "visited": set(),
    })
    return path, dist[end], steps


# ---------------------------------------------------------------------------
# Floyd-Warshall  (all-pairs shortest paths)
# ---------------------------------------------------------------------------

def floyd_warshall_with_steps(graph, start, end):
    """
    Computes ALL-PAIRS shortest paths.

    Extra field in every step dict:
        matrix_snapshot – list of dicts, one per source node:
            {
              "src":  node label,
              "row":  {dest_node: cost_or_'INF'},
            }
        nodes           – ordered list of node labels (column headers)
        updated_cell    – (i, j) indices that changed in this step, or None
    """
    steps = []
    nodes = sorted(list(graph.nodes()))
    idx = {n: i for i, n in enumerate(nodes)}
    n = len(nodes)
    INF = float('inf')

    dist = [[INF] * n for _ in range(n)]
    prev = [[None] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0
    for u, v in graph.edges():
        w = graph[u][v].get('weight', 1)
        i, j = idx[u], idx[v]
        if w < dist[i][j]:
            dist[i][j] = w
            prev[i][j] = u

    def matrix_snap():
        """Full N×N snapshot: list of {src, row{dest: val}}."""
        return [
            {
                "src": nodes[i],
                "row": {
                    nodes[j]: (dist[i][j] if dist[i][j] != INF else 'INF')
                    for j in range(n)
                },
            }
            for i in range(n)
        ]

    def src_snap():
        """Single-row snapshot for the chosen start node (used by graph panel)."""
        si = idx[start]
        return {nodes[j]: (dist[si][j] if dist[si][j] != INF else 'INF') for j in range(n)}

    steps.append({
        "type": "init",
        "message": "Initialize distance matrix with direct edge weights (0 on diagonal, edge weights for direct edges, INF elsewhere)",
        "dist_snapshot": src_snap(),
        "matrix_snapshot": matrix_snap(),
        "nodes": list(nodes),
        "updated_cell": None,
        "relaxed_edges": [],
        "visited": set(),
    })

    for k in range(n):
        vk = nodes[k]
        for i in range(n):
            for j in range(n):
                if dist[i][k] != INF and dist[k][j] != INF:
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        old = dist[i][j]
                        dist[i][j] = dist[i][k] + dist[k][j]
                        prev[i][j] = prev[k][j]
                        vi, vj = nodes[i], nodes[j]
                        # Highlight the edge on the graph only when it involves
                        # the chosen source or target so the visualisation stays useful
                        relaxed = [(vi, vj)] if (i == idx[start] or j == idx[end]) else []
                        steps.append({
                            "type": "relax",
                            "edge": (vi, vj),
                            "message": (
                                f"Intermediate {vk}: dist[{vi}][{vj}] "
                                f"{('INF' if old == INF else old)} → {dist[i][j]}"
                                f"  (via {vi} → {vk} → {vj})"
                            ),
                            "dist_snapshot": src_snap(),
                            "matrix_snapshot": matrix_snap(),
                            "nodes": list(nodes),
                            "updated_cell": (i, j),
                            "relaxed_edges": relaxed,
                            "visited": set(),
                        })

    # Check for negative-weight cycles (dist[i][i] < 0)
    for i in range(n):
        if dist[i][i] < 0:
            steps.append({
                "type": "final",
                "message": f"Negative weight cycle detected through node {nodes[i]}!",
                "dist_snapshot": src_snap(),
                "matrix_snapshot": matrix_snap(),
                "nodes": list(nodes),
                "updated_cell": None,
                "relaxed_edges": [],
                "visited": set(),
            })
            return None, "Negative weight cycle detected!", steps

    # Build the all-pairs result summary for the final step message
    reachable_pairs = [
        (nodes[i], nodes[j], dist[i][j])
        for i in range(n) for j in range(n)
        if i != j and dist[i][j] != INF
    ]
    summary = f"All-pairs shortest paths computed. {len(reachable_pairs)} reachable pair(s)."

    # Reconstruct the highlighted path from start → end if reachable
    si, ei = idx.get(start), idx.get(end)
    path = None
    if si is not None and ei is not None and dist[si][ei] != INF:
        path = [end]
        cur = end
        while cur != start:
            ci = idx[cur]
            p = prev[si][ci]
            if p is None:
                path = None
                break
            path.append(p)
            cur = p
        if path:
            path.reverse()

    cost = dist[si][ei] if (si is not None and ei is not None and dist[si][ei] != INF) else "No path"
    path_msg = (
        f"  |  Highlighted: {start} → {end} = {cost}"
        if path else
        f"  |  No path from {start} to {end}"
    )

    steps.append({
        "type": "final",
        "message": summary + path_msg,
        "dist_snapshot": src_snap(),
        "matrix_snapshot": matrix_snap(),
        "nodes": list(nodes),
        "updated_cell": None,
        "relaxed_edges": [],
        "path": path or [],
        "visited": set(),
    })

    return path, cost, steps


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------

def _snap(dist):
    """Convert a dist dict to a serialisable snapshot (inf → 'INF')."""
    return {n: (v if v != float('inf') else 'INF') for n, v in dist.items()}


def _reconstruct(prev, end):
    """Walk the prev-pointer map back from end to the start node."""
    path = []
    cur = end
    while cur is not None:
        path.append(cur)
        cur = prev[cur]
    path.reverse()
    return path