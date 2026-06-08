"""
app.py
------
Entry point for the Shortest Path Visualizer Streamlit app.

Run with:
    streamlit run app.py

Project layout
--------------
app.py              ← you are here (page config, session state, main panel)
styles.py           ← global CSS
algorithms.py       ← Dijkstra / Bellman-Ford / Floyd-Warshall with step recording
graph_renderer.py   ← Pyvis HTML rendering helper
sidebar.py          ← sidebar UI (graph editor + algorithm runner)
"""

import networkx as nx
import streamlit as st

from graph_renderer import render_graph
from sidebar import render_sidebar
from styles import inject_styles

# -----------------------------------------------------------------------
# PAGE CONFIG  (must be the very first Streamlit call)
# -----------------------------------------------------------------------
st.set_page_config(
    page_title="Shortest Path Visualizer",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_styles()

# -----------------------------------------------------------------------
# SESSION STATE INITIALISATION
# -----------------------------------------------------------------------
_DEFAULTS = {
    "graph":            nx.DiGraph(),
    "relaxation_steps": [],
    "current_step":     0,
    "path_result":      None,
    "run_done":         False,
    "node_positions":   {},
}
for key, default in _DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = default

G: nx.DiGraph = st.session_state.graph

# -----------------------------------------------------------------------
# SIDEBAR
# -----------------------------------------------------------------------
render_sidebar(G)

# -----------------------------------------------------------------------
# MAIN PANEL — header + metrics
# -----------------------------------------------------------------------
st.markdown("# Shortest Path Visualizer")
st.markdown("Build a graph, pick an algorithm, step through every relaxation.")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Nodes", len(G.nodes))
with col2:
    st.metric("Edges", len(G.edges))
with col3:
    pr = st.session_state.path_result
    st.metric("Path Cost", pr["cost"] if pr and pr["path"] else "—")
with col4:
    steps = st.session_state.relaxation_steps
    st.metric("Total Steps", len(steps) if steps else "—")

st.markdown("")

# -----------------------------------------------------------------------
# MAIN PANEL — two-column layout: graph visualisation + step panel
# -----------------------------------------------------------------------
left_col, right_col = st.columns([3, 2], gap="medium")

# ---- Determine what to highlight at the current step ----
steps   = st.session_state.relaxation_steps
cur_idx = st.session_state.current_step

current_relaxed    = []
current_visited    = set()
current_final_path = []

if steps and cur_idx < len(steps):
    step = steps[cur_idx]
    current_relaxed    = step.get("relaxed_edges", [])
    current_visited    = step.get("visited", set())
    if step.get("type") == "final" and step.get("path"):
        current_final_path = step["path"]
elif steps and cur_idx >= len(steps):
    last = steps[-1]
    current_final_path = last.get("path", [])
    current_visited    = last.get("visited", set())

# ---- Graph panel ----
with left_col:
    if len(G.nodes) == 0:
        st.markdown("""
        <div style="background:#1a1535; border-radius:16px; padding:60px 40px; text-align:center;
                    box-shadow:0 2px 16px rgba(0,0,0,0.4); color:#7c3aed; border:1px solid #2d2060;">
            <div style="font-size:2.5rem; font-weight:800; font-family:'DM Sans',sans-serif; color:#c4b5fd;">
                Empty Graph
            </div>
            <div style="font-size:1rem; color:#7c6aaa; margin-top:12px; font-family:'Space Mono',monospace;">
                Add edges from the sidebar to get started.
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        try:
            html_code, positions = render_graph(
                G,
                relaxed_edges  = current_relaxed,
                visited_nodes  = current_visited,
                final_path     = current_final_path,
                positions      = st.session_state.node_positions or None,
                undirected_edges = st.session_state.get("undirected_edges", set()),
            )
            if positions:
                st.session_state.node_positions = positions
            st.iframe(html_code, height=530)
        except Exception as e:
            st.error(f"Render error: {e}")

    # Colour legend
    st.markdown("""
    <div style="display:flex; gap:14px; flex-wrap:wrap; margin-top:8px;">
        <span style="font-family:'Space Mono',monospace; font-size:0.75rem;">
            <span style="background:#3b82f6;color:white;padding:2px 8px;border-radius:4px;">Unvisited</span>
        </span>
        <span style="font-family:'Space Mono',monospace; font-size:0.75rem;">
            <span style="background:#f59e0b;color:white;padding:2px 8px;border-radius:4px;">Visited</span>
        </span>
        <span style="font-family:'Space Mono',monospace; font-size:0.75rem;">
            <span style="background:#7c3aed;color:white;padding:2px 8px;border-radius:4px;">Shortest Path</span>
        </span>
        <span style="font-family:'Space Mono',monospace; font-size:0.75rem;">
            <span style="background:#10b981;color:white;padding:2px 8px;border-radius:4px;">Relaxed Edge</span>
        </span>
        <span style="font-family:'Space Mono',monospace; font-size:0.75rem;">
            <span style="background:#94a3b8;color:white;padding:2px 8px;border-radius:4px;">Default Edge</span>
        </span>
    </div>
    """, unsafe_allow_html=True)

# ---- Step panel ----
with right_col:
    steps = st.session_state.relaxation_steps

    if not steps:
        if not st.session_state.run_done:
            st.markdown("""
            <div class="info-box">
                Run an algorithm from the sidebar to see step-by-step relaxations here.
                <br><br>
                Each edge relaxation will be shown with updated distances.
            </div>
            """, unsafe_allow_html=True)
        else:
            pr = st.session_state.path_result
            if pr:
                st.error(f"Error: {pr['cost']}")
    else:
        cur_idx = st.session_state.current_step
        total   = len(steps)

        # Navigation controls
        st.markdown(
            f'<div class="algo-badge">{st.session_state.algo} — Step {cur_idx + 1} of {total}</div>',
            unsafe_allow_html=True,
        )

        nav_c1, nav_c2, nav_c3, nav_c4 = st.columns(4)
        with nav_c1:
            if st.button("|<", help="First step", use_container_width=True):
                st.session_state.current_step = 0
                st.rerun()
        with nav_c2:
            if st.button("<", help="Previous step", use_container_width=True):
                if st.session_state.current_step > 0:
                    st.session_state.current_step -= 1
                    st.rerun()
        with nav_c3:
            if st.button(">", help="Next step", use_container_width=True):
                if st.session_state.current_step < total - 1:
                    st.session_state.current_step += 1
                    st.rerun()
        with nav_c4:
            if st.button(">|", help="Last step", use_container_width=True):
                st.session_state.current_step = total - 1
                st.rerun()

        st.progress((cur_idx + 1) / total)
        st.markdown("")

        # Current step detail card
        step       = steps[cur_idx]
        step_type  = step.get("type", "relax")
        type_class = {"init": "init", "visit": "visit", "relax": "relax", "final": "final"}.get(step_type, "relax")

        st.markdown(f"""
        <div class="step-card {type_class}">
            <div style="font-size:0.7rem; text-transform:uppercase; letter-spacing:1px; opacity:0.6; margin-bottom:4px;">
                {step_type.upper()}
            </div>
            {step["message"]}
        </div>
        """, unsafe_allow_html=True)

        # Distance table — full matrix for Floyd-Warshall, single-row for others
        is_fw = st.session_state.get("algo") == "Floyd-Warshall"

        if is_fw:
            matrix    = step.get("matrix_snapshot", [])
            col_nodes = step.get("nodes", [])
            updated_cell = step.get("updated_cell")   # (row_i, col_j) or None
            prev_matrix  = steps[cur_idx - 1].get("matrix_snapshot", []) if cur_idx > 0 else []

            if matrix and col_nodes:
                st.markdown("**All-pairs distance matrix at this step:**")

                # Build an HTML table
                header_cells = "".join(
                    f'<th style="padding:5px 10px;text-align:center;'
                    f'font-family:var(--font-mono,monospace);font-size:0.72rem;'
                    f'color:#a89cc8;border-bottom:1px solid rgba(155,93,229,0.25);">{c}</th>'
                    for c in col_nodes
                )
                header_row = (
                    f'<tr><th style="padding:5px 10px;font-family:var(--font-mono,monospace);'
                    f'font-size:0.72rem;color:#a89cc8;border-bottom:1px solid rgba(155,93,229,0.25);">src \\ dst</th>'
                    f'{header_cells}</tr>'
                )

                body_rows = ""
                for ri, row_info in enumerate(matrix):
                    src = row_info["src"]
                    prev_row = prev_matrix[ri]["row"] if prev_matrix and ri < len(prev_matrix) else {}
                    row_html = ""
                    for ci, col in enumerate(col_nodes):
                        val = row_info["row"].get(col, "INF")
                        prev_val = prev_row.get(col)
                        is_updated = (
                            updated_cell is not None
                            and updated_cell == (ri, ci)
                        )
                        is_changed = (
                            not is_updated
                            and prev_val is not None
                            and prev_val != val
                        )
                        if is_updated:
                            cell_bg    = "rgba(11,240,168,0.18)"
                            cell_color = "#0bf0a8"
                            cell_border = "1px solid rgba(11,240,168,0.55)"
                            cell_fw = "800"
                        elif is_changed:
                            cell_bg    = "rgba(155,93,229,0.12)"
                            cell_color = "#c77dff"
                            cell_border = "1px solid rgba(155,93,229,0.30)"
                            cell_fw = "700"
                        else:
                            cell_bg    = "transparent"
                            cell_color = "#f2eeff"
                            cell_border = "1px solid rgba(155,93,229,0.10)"
                            cell_fw = "400"

                        display = str(val)
                        row_html += (
                            f'<td style="padding:5px 10px;text-align:center;'
                            f'font-family:var(--font-mono,monospace);font-size:0.75rem;'
                            f'background:{cell_bg};color:{cell_color};'
                            f'border:{cell_border};border-radius:4px;'
                            f'font-weight:{cell_fw};">{display}</td>'
                        )
                    body_rows += (
                        f'<tr><td style="padding:5px 10px;font-family:var(--font-mono,monospace);'
                        f'font-size:0.75rem;font-weight:700;color:#9b5de5;'
                        f'border-right:1px solid rgba(155,93,229,0.25);">{src}</td>'
                        f'{row_html}</tr>'
                    )

                table_html = (
                    f'<div style="overflow-x:auto;margin:10px 0;">'
                    f'<table style="border-collapse:separate;border-spacing:3px;width:100%;">'
                    f'<thead>{header_row}</thead>'
                    f'<tbody>{body_rows}</tbody>'
                    f'</table>'
                    f'<div style="font-family:var(--font-mono,monospace);font-size:0.68rem;'
                    f'color:#5c5178;margin-top:6px;">'
                    f'&#9646; green cell = updated this step &nbsp;|&nbsp; purple = changed earlier</div>'
                    f'</div>'
                )
                st.markdown(table_html, unsafe_allow_html=True)
        else:
            dist_snap = step.get("dist_snapshot", {})
            if dist_snap:
                st.markdown("**Distance table at this step:**")
                prev_snap  = steps[cur_idx - 1].get("dist_snapshot", {}) if cur_idx > 0 else {}
                cells_html = ""
                for node, val in sorted(dist_snap.items()):
                    prev_val      = prev_snap.get(node)
                    updated_class = "updated" if prev_val is not None and prev_val != val else ""
                    display_val   = str(val) if val != float('inf') else "INF"
                    cells_html   += f'<div class="dist-cell {updated_class}">{node}: {display_val}</div>'
                st.markdown(f'<div class="dist-table">{cells_html}</div>', unsafe_allow_html=True)

        # Final path highlight
        if step_type == "final" and step.get("path"):
            path = step["path"]
            cost = st.session_state.path_result["cost"]
            st.markdown(f"""
            <div class="path-highlight">
                Shortest Path<br>
                {" -> ".join(path)}<br>
                Total cost: {cost}
            </div>
            """, unsafe_allow_html=True)

        # Collapsible full log
        with st.expander("All steps log"):
            for i, s in enumerate(steps):
                marker = " <-- current" if i == cur_idx else ""
                st.markdown(f"""
                <div style="font-family:'Space Mono',monospace; font-size:0.75rem;
                            padding:6px 10px; border-radius:6px;
                            background:{'#ede9fe' if i == cur_idx else 'transparent'};
                            color:{'#4c1d95' if i == cur_idx else '#475569'};
                            margin:2px 0;">
                    {i + 1}. {s['message']}{marker}
                </div>
                """, unsafe_allow_html=True)