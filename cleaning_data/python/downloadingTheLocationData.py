import networkx as nx
import osmnx as ox

ox.config(use_cache=True, log_console=True)
# download street network data from OSM and construct a MultiDiGraph model
G = ox.graph_from_point((19.429052, -99.141523), dist=750, network_type="drive")
# impute edge (driving) speeds and calculate edge traversal times
G = ox.add_edge_speeds(G)
G = ox.add_edge_travel_times(G)
# you can convert MultiDiGraph to/from geopandas GeoDataFrames
(gdf_nodes, gdf_edges) = ox.graph_to_gdfs(G,fill_edge_geometry=False)
G = ox.graph_from_gdfs(gdf_nodes, gdf_edges, graph_attrs=G.graph)
# convert MultiDiGraph to DiGraph to use nx.betweenness_centrality function
# choose between parallel edges by minimizing travel_time attribute value
D = ox.utils_graph.get_digraph(G, weight="travel_time")
# calculate node betweenness centrality, weighted by travel time
bc = nx.betweenness_centrality(D, weight="travel_time", normalized=True)
nx.set_node_attributes(G, values=bc, name="bc")
# plot the graph, coloring nodes by betweenness centrality
nc = ox.plot.get_node_colors_by_attr(G, "bc", cmap="plasma")
fig, ax = ox.plot_graph(
    G, bgcolor="k", node_color=nc, node_size=50, edge_linewidth=2, edge_color="#333333")

gdf_nodes.to_file('nodes.json', driver='GeoJSON')
gdf_edges.to_file('edges.json', driver='GeoJSON')