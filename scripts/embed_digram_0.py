from bokeh.models import (BoxZoomTool, Circle, HoverTool,
                          MultiLine, Plot, Range1d, ResetTool)
from bokeh.palettes import Spectral4, Spectral8
from bokeh.plotting import from_networkx

import datapane as dp
import networkx as nx
import pandas as pd

# get csv file from URL, load into csv, read it as networkx graph.

data = pd.read_csv(
    'https://raw.githubusercontent.com/wey-gu/identity-correlation-datagen/main/sample/hand_crafted/user.csv',
    header=0,
    names=['user_id', 'email', 'name', 'birth', 'addr', 'phone'])

G = nx.from_pandas_edgelist(
    data,
    create_using=nx.MultiGraph(),
    source='user_id',
    target='email',
    edge_attr=['email'])

# G_phone = nx.from_pandas_edgelist(
#     data,
#     create_using=nx.MultiGraph(),
#     source='user_id',
#     target='phone')

nx.set_node_attributes(G, pd.Series(data.name.to_numpy(), index=data.user_id).to_dict(), 'name')
nx.set_node_attributes(G, pd.Series(data.email.to_numpy(), index=data.user_id).to_dict(), 'email')
nx.set_node_attributes(G, pd.Series(data.birth.to_numpy(), index=data.user_id).to_dict(), 'birth')
nx.set_node_attributes(G, pd.Series(data.addr.to_numpy(), index=data.user_id).to_dict(), 'addr')
nx.set_node_attributes(G, pd.Series(data.phone.to_numpy(), index=data.user_id).to_dict(), 'phone')
nx.set_node_attributes(G, pd.Series(data.email.to_numpy(), index=data.email).to_dict(), 'name')
# nx.set_node_attributes(G, pd.Series(data.phone.to_numpy(), index=data.phone).to_dict(), 'name')

# # merge two graphs
# G = nx.compose(G, G_phone)


# Show with Bokeh
plot = Plot(width=400, height=400,
            x_range=Range1d(-1.1, 1.1), y_range=Range1d(-1.1, 1.1))
plot.title.text = "User shared email"

node_hover_tool = HoverTool(tooltips=[("vertex_id", "@index"), ("name", "@name")])
plot.add_tools(node_hover_tool, BoxZoomTool(), ResetTool())

#graph_renderer = from_networkx(G, nx.spring_layout, scale=1, center=(0, 0))
graph_renderer = from_networkx(
    G, nx.spring_layout,
    seed=321313,
    scale=1, center=(0, 0))

graph_renderer.node_renderer.glyph = Circle(size=19, fill_color="name")
graph_renderer.edge_renderer.glyph = MultiLine(line_alpha=0.8, line_width=1)
plot.renderers.append(graph_renderer)

dp.Report(dp.Plot(plot)).save(path="embed_graph_0.html")
#dp.Report(dp.Plot(plot)).upload(name="User Shared Email")
