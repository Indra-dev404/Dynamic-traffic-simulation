import streamlit as st
import networkx as nx
import plotly.graph_objects as go
import random

# -------------------------------------------
# Generate a Random Directed Traffic Graph
# -------------------------------------------
def generate_graph():
    G = nx.DiGraph()
    edges = [
        ("A", "B", random.randint(2, 10)),
        ("A", "C", random.randint(2, 10)),
        ("B", "D", random.randint(2, 10)),
        ("C", "D", random.randint(2, 10)),
        ("D", "E", random.randint(2, 10)),
        ("B", "E", random.randint(2, 10))
    ]
    G.add_weighted_edges_from(edges)
    return G

# -------------------------------------------
# Dijkstra’s Algorithm using NetworkX
# -------------------------------------------
def dijkstra(graph, source):
    try:
        path_lengths = nx.single_source_dijkstra_path_length(graph, source)
    except Exception as e:
        path_lengths = {}
        st.error(f"Error running Dijkstra: {e}")
    return path_lengths

# -------------------------------------------
# Bellman-Ford Algorithm using NetworkX
# -------------------------------------------
def bellman_ford(graph, source):
    try:
        path_lengths = nx.single_source_bellman_ford_path_length(graph, source)
    except Exception as e:
        path_lengths = {}
        st.error(f"Error running Bellman-Ford: {e}")
    return path_lengths

# -------------------------------------------
# Plotly Visualization of Graph + Distances
# -------------------------------------------
def visualize_plotly(graph, path_lengths, source):
    pos = nx.spring_layout(graph, seed=42)

    # Edge traces
    edge_x = []
    edge_y = []
    weights = []

    for u, v, data in graph.edges(data=True):
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
        weights.append(data['weight'])

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1.5, color='#888'),
        hoverinfo='none',
        mode='lines'
    )

    # Node traces
    node_x = []
    node_y = []
    node_text = []

    for node in graph.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        dist = path_lengths.get(node, "∞")
        node_text.append(f"{node} (Dist: {dist})")

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        hoverinfo='text',
        text=node_text,
        textposition="top center",
        marker=dict(
            color='#00cc96',
            size=20,
            line=dict(width=2)
        )
    )

    fig = go.Figure(data=[edge_trace, node_trace],
        layout=go.Layout(
            showlegend=False,
            margin=dict(b=20,l=5,r=5,t=40),
            hovermode='closest',
            title='Traffic Network Graph',
        )
    )

    st.plotly_chart(fig)

# -------------------------------------------
# STREAMLIT INTERFACE
# -------------------------------------------
st.set_page_config(page_title="Traffic Flow Simulator", layout="wide")
st.title("🚦 Traffic Flow Simulation using Dijkstra & Bellman-Ford")

st.write("This tool simulates traffic flow and computes the shortest path from a source using graph algorithms.")

algo = st.selectbox("Choose Algorithm", ["Dijkstra", "Bellman-Ford"])
source = st.text_input("Enter Source Node (e.g., A)", value="A")

if st.button("Run Simulation"):
    G = generate_graph()

    if source not in G.nodes:
        st.error(f"Source node '{source}' not found in the graph. Try A, B, C, D, or E.")
    else:
        if algo == "Dijkstra":
            path_lengths = dijkstra(G, source)
        else:
            path_lengths = bellman_ford(G, source)

        st.success(f"{algo} algorithm ran successfully from source node '{source}'")
        
        st.write("### 📊 Graph Visualization")
        visualize_plotly(G, path_lengths, source)

        st.write("### 📌 Shortest Distances from Source")
        st.table(path_lengths)