"""
graph_renderer.py
-----------------
Converts a NetworkX DiGraph into a Pyvis HTML string, highlighting
relaxed edges, visited nodes, and the final shortest path.

Public API
----------
render_graph(graph, relaxed_edges, visited_nodes, final_path, positions)
    -> (html_string, positions_dict)
"""

import json
import os
import tempfile

import networkx as nx
from pyvis.network import Network


# Node colour scheme
_COLOR_PATH    = "#7c3aed"   # on the shortest path
_COLOR_VISITED = "#f59e0b"   # already popped from the priority queue
_COLOR_DEFAULT = "#3b82f6"   # not yet touched

# Edge colour scheme
_COLOR_RELAXED = "#10b981"   # currently being relaxed
_COLOR_DEFAULT_EDGE = "#94a3b8"


def render_graph(
    graph,
    relaxed_edges=None,
    visited_nodes=None,
    final_path=None,
    positions=None,
    undirected_edges=None,
):
    """
    Build a Pyvis HTML visualisation of *graph*.

    Parameters
    ----------
    graph            : nx.DiGraph
    relaxed_edges    : list of (u, v) – edges to colour green this step
    visited_nodes    : set of node labels – nodes to colour amber
    final_path       : list of node labels in order – nodes/edges coloured purple
    positions        : dict {node: (x, y)} – reuse stable layout across steps
    undirected_edges : set of frozensets – edge pairs to render without arrowheads

    Returns
    -------
    (html_content : str, positions : dict)
    """
    if relaxed_edges is None:
        relaxed_edges = []
    if visited_nodes is None:
        visited_nodes = set()
    if final_path is None:
        final_path = []
    if undirected_edges is None:
        undirected_edges = set()

    # Build the set of edges that belong to the final path
    path_edge_set = set()
    for i in range(len(final_path) - 1):
        path_edge_set.add((final_path[i], final_path[i + 1]))

    # Compute a stable spring layout the first time
    if not positions and len(graph.nodes) > 0:
        spring_pos = nx.spring_layout(graph, seed=42, k=2.0)
        positions = {
            n: (int((x + 1) * 300), int((y + 1) * 230))
            for n, (x, y) in spring_pos.items()
        }

    net = Network(
        height="520px",
        width="100%",
        bgcolor="#12102a",
        font_color="#e2e8f0",
        directed=True,
    )

    # --- Nodes ---
    for node in graph.nodes():
        if final_path and node in final_path:
            color, size, font_color = _COLOR_PATH, 26, "#ffffff"
        elif node in visited_nodes:
            color, size, font_color = _COLOR_VISITED, 22, "#1a0533"
        else:
            color, size, font_color = _COLOR_DEFAULT, 18, "#ffffff"

        px, py = (positions or {}).get(node, (300, 250))
        net.add_node(
            node,
            label=node,
            color=color,
            size=size,
            font={"size": 16, "color": font_color, "bold": True},
            borderWidth=2,
            borderWidthSelected=4,
            x=px,
            y=py,
            physics=False,   # pin nodes so the layout stays stable
        )

    # --- Edges ---
    relaxed_set = {tuple(e) for e in relaxed_edges}
    rendered_undirected = set()   # track frozensets already drawn as undirected

    for u, v, data in graph.edges(data=True):
        edge_pair = frozenset({u, v})
        is_undirected = edge_pair in undirected_edges

        # For undirected pairs, only render once (skip the reverse duplicate)
        if is_undirected:
            if edge_pair in rendered_undirected:
                continue
            rendered_undirected.add(edge_pair)

        weight = data.get("weight", 1)
        is_relaxed = (u, v) in relaxed_set
        is_path    = (u, v) in path_edge_set

        if is_relaxed or is_path:
            color, width = _COLOR_RELAXED, (3 if is_relaxed else 2)
        else:
            color, width = _COLOR_DEFAULT_EDGE, 1.5

        arrows_config = (
            {"to": {"enabled": False}, "from": {"enabled": False}}
            if is_undirected
            else {"to": {"enabled": True, "scaleFactor": 0.8}}
        )

        net.add_edge(
            u, v,
            title=f"Weight: {weight}",
            label=str(weight),
            color=color,
            width=width,
            font={"size": 20, "color": "#c77dff", "bold": True, "strokeWidth": 3, "strokeColor": "#06040f"},
            arrows=arrows_config,
        )

    net.set_options(json.dumps({
        "physics": {"enabled": False},
        "edges":   {"smooth": {"type": "curvedCW", "roundness": 0.2}},
        "nodes":   {"shape": "dot", "shadow": True},
    }))

    # Write to a temp file, read back, then clean up
    tmp_path = tempfile.mktemp(suffix=".html")
    net.save_graph(tmp_path)
    with open(tmp_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    os.unlink(tmp_path)

    return html_content, positions