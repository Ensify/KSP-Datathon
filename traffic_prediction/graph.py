import torch
import csv
import numpy as np
from stgn import STGCN

from torch_geometric.data import Data
from torch_geometric.utils import to_networkx
import matplotlib.pyplot as plt
import networkx as nx
from io import BytesIO
import cv2

def load_model(weights, edges):
    """
    Load the model from the given weights file.
    """
    edge_indexes, edge_weights = load_graph(edges)
    
    model = STGCN(num_nodes = 9, in_channels = 6, hidden=10, features= 6, edge_index=edge_indexes, edge_weight=edge_weights)

    model.load_state_dict(torch.load(weights))
    model.eval()

    return model

def load_graph(edges_file):
    edge_indexes = []
    edge_weights = []
    with open(edges_file, "r") as f:
        reader = csv.reader(f)
        for i,row in enumerate(reader): 
            if i == 0:
                continue
            edge_indexes.append([int(row[1])-1, int(row[2])-1])
            edge_indexes.append([int(row[2])-1, int(row[1])-1])
            edge_weights.append([float(row[3])])
            edge_weights.append([float(row[3])])

    edge_indexes = torch.tensor(edge_indexes, dtype= torch.int64) 
    edge_weights = torch.tensor(edge_weights, dtype= torch.float)

    return edge_indexes, edge_weights
    
def infer(model, x):
    """
    x: Shape (5, 9, 6) (timestep, nodes, features)

    returns list of size 9
    """
    x = torch.tensor(x, dtype=torch.float32)
    x = x.reshape(1,*x.shape)
    prediction = model(x)

    return  [int(pred.item()) for pred in prediction]

def build_representation(output, edges):
    print(output)
    edge_indexes, edge_weights = load_graph(edges)
    x = torch.tensor([i for i in range(9)], dtype=torch.float)
    data = Data(x= x, edge_index=edge_indexes.t().contiguous(), edge_attr= edge_weights, num_nodes = 9)

    print(data)
    G = to_networkx(data, to_undirected=True)
    plt.figure(figsize=(12,12))
    plt.axis('off')
    nx.draw_networkx(G,
                    pos=nx.spring_layout(G, seed=0),
                    with_labels=True,
                    node_size=800,
                    node_color=data.y,
                    cmap="hsv",
                    vmin=-2,
                    vmax=3,
                    width=0.8,
                    edge_color="grey",
                    font_size=14,
                    labels = {i: output[i] for i in range(9)},
                    )
    print("generated plot")
    # Save the figure to a buffer
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    # Read the buffer as an image
    img_arr = np.frombuffer(buf.getvalue(), dtype=np.uint8)
    buf.close()
    img = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)
    
    return img


if __name__ == '__main__':

    model = load_model(weights='models/stgcn_model_final.pth', edges = "data/edges.csv")
    sample = np.zeros((5,9,6))
    print(infer(model,sample))
    build_representation(sample, "data/edges.csv")