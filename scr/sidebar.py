"""
sidebar.py
----------
Renders the Streamlit sidebar: graph editor (add/remove nodes & edges)
and algorithm runner (source, target, algorithm choice).

Call render_sidebar(G) from app.py inside a `with st.sidebar:` block,
or just call render_sidebar(G) directly — the function opens its own
`with st.sidebar:` context internally.
"""

import networkx as nx
import streamlit as st

from algorithms import (
    bellman_ford_with_steps,
    dijkstra_with_steps,
    floyd_warshall_with_steps,
)


def render_sidebar(G: nx.DiGraph) -> None:
    """Draw the full sidebar and mutate session_state as needed."""
    with st.sidebar:
        st.markdown("## Graph Editor")

        _section_add_edge(G)
        _section_add_node(G)
        _section_remove(G)
        _section_algorithm(G)


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------

def _section_add_edge(G: nx.DiGraph) -> None:
    st.markdown('<div class="section-head">Add / Update Edge</div>', unsafe_allow_html=True)

    # Initialise undirected-edge tracker in session state
    if "undirected_edges" not in st.session_state:
        st.session_state.undirected_edges = set()

    c1, c2 = st.columns(2)
    with c1:
        node_from = st.text_input("From", value="", placeholder="A", key="from_node").strip().upper()
    with c2:
        node_to = st.text_input("To", value="", placeholder="B", key="to_node").strip().upper()

    edge_weight   = st.number_input("Weight", value=1, step=1, key="ew")
    directed_edge = st.checkbox("Directed edge", value=True)

    if st.button("Add / Update Edge", use_container_width=True):
        if node_from and node_to and node_from != node_to:
            G.add_edge(node_from, node_to, weight=edge_weight)
            if not directed_edge:
                # Add reverse edge so both directions work for algorithms
                G.add_edge(node_to, node_from, weight=edge_weight)
                # Track this pair as undirected for rendering (store as frozenset)
                st.session_state.undirected_edges.add(frozenset({node_from, node_to}))
            else:
                # If re-adding as directed, remove from undirected set if present
                st.session_state.undirected_edges.discard(frozenset({node_from, node_to}))
            _reset_run_state()
            st.rerun()
        else:
            st.error("Enter valid distinct node names.")


def _section_add_node(G: nx.DiGraph) -> None:
    st.markdown('<div class="section-head">Add Isolated Node</div>', unsafe_allow_html=True)

    lone_node = st.text_input("Node name", value="", placeholder="Z", key="lone").strip().upper()
    if st.button("Add Node", use_container_width=True):
        if lone_node:
            G.add_node(lone_node)
            st.rerun()
        else:
            st.error("Enter a node name.")


def _section_remove(G: nx.DiGraph) -> None:
    st.markdown('<div class="section-head">Remove Elements</div>', unsafe_allow_html=True)

    del_node = st.text_input("Node to delete", value="", placeholder="A", key="del_n").strip().upper()
    if st.button("Delete Node", use_container_width=True):
        if G.has_node(del_node):
            G.remove_node(del_node)
            _reset_run_state()
            st.rerun()
        else:
            st.error("Node not found.")

    c3, c4 = st.columns(2)
    with c3:
        del_from = st.text_input("Edge from", value="", placeholder="A", key="del_ef").strip().upper()
    with c4:
        del_to = st.text_input("Edge to", value="", placeholder="B", key="del_et").strip().upper()

    if st.button("Delete Edge", use_container_width=True):
        if G.has_edge(del_from, del_to):
            G.remove_edge(del_from, del_to)
            _reset_run_state()
            st.rerun()
        else:
            st.error("Edge not found.")


def _section_algorithm(G: nx.DiGraph) -> None:
    st.markdown('<div class="section-head">Algorithm</div>', unsafe_allow_html=True)

    all_nodes = sorted(list(G.nodes()))
    if all_nodes:
        source_node = st.selectbox("Source node", all_nodes, key="src")
        target_node = st.selectbox("Target node", all_nodes, key="tgt")
    else:
        source_node, target_node = None, None
        st.info("Add nodes to the graph first.")

    selected_algo = st.radio(
        "Algorithm",
        ["Dijkstra", "Bellman-Ford", "Floyd-Warshall"],
        key="algo",
    )

    if selected_algo == "Floyd-Warshall":
        st.info(
            "Floyd-Warshall computes **all-pairs** shortest paths. "
            "Source & target are used only to highlight one path on the graph.",
            icon="ℹ️",
        )

    if st.button("Run Algorithm", use_container_width=True, type="primary"):
        if source_node and target_node and source_node != target_node:
            algo_map = {
                "Dijkstra":       dijkstra_with_steps,
                "Bellman-Ford":   bellman_ford_with_steps,
                "Floyd-Warshall": floyd_warshall_with_steps,
            }
            path, cost, steps = algo_map[selected_algo](G, source_node, target_node)
            st.session_state.relaxation_steps = steps
            st.session_state.current_step     = 0
            st.session_state.path_result      = {"path": path, "cost": cost}
            st.session_state.run_done         = True
            st.rerun()
        else:
            st.error("Select distinct source and target nodes.")

    st.markdown("---")

    if st.button("Clear Graph", use_container_width=True):
        st.session_state.graph = nx.DiGraph()
        st.session_state.relaxation_steps = []
        st.session_state.run_done         = False
        st.session_state.path_result      = None
        st.session_state.current_step     = 0
        st.session_state.node_positions   = {}
        st.session_state.undirected_edges = set()
        st.rerun()


def _reset_run_state() -> None:
    """Clear algorithm results whenever the graph topology changes."""
    st.session_state.relaxation_steps = []
    st.session_state.run_done         = False
    st.session_state.path_result      = None
    st.session_state.node_positions   = {}