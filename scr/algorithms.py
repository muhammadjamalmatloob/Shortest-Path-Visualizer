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
# Floyd-Warshall
# ---------------------------------------------------------------------------

def floyd_warshall_with_steps(graph, start, end):
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

    def snap():
        si = idx[start]
        return {nodes[i]: (dist[si][i] if dist[si][i] != INF else 'INF') for i in range(n)}

    steps.append({
        "type": "init",
        "message": "Initialize distance matrix with direct edge weights",
        "dist_snapshot": snap(),
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
                        relaxed = [(vi, vj)] if i == idx[start] else []
                        steps.append({
                            "type": "relax",
                            "edge": (vi, vj),
                            "message": (
                                f"Via {vk}: dist[{vi}][{vj}] updated "
                                f"{('INF' if old == INF else old)} -> {dist[i][j]}"
                            ),
                            "dist_snapshot": snap(),
                            "relaxed_edges": relaxed,
                            "visited": set(),
                        })

    si, ei = idx.get(start), idx.get(end)
    if si is None or ei is None or dist[si][ei] == INF:
        return None, "No path exists", steps

    # Reconstruct path from prev matrix
    path = [end]
    cur = end
    while cur != start:
        ci = idx[cur]
        p = prev[si][ci]
        if p is None:
            return None, "No path exists", steps
        path.append(p)
        cur = p
    path.reverse()

    steps.append({
        "type": "final",
        "message": f"Shortest path found: {' -> '.join(path)}  |  Total cost = {dist[si][ei]}",
        "dist_snapshot": snap(),
        "relaxed_edges": [],
        "path": path,
        "visited": set(),
    })
    return path, dist[si][ei], steps


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