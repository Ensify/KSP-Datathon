import torch
import torch.nn.functional as F
from torch_geometric_temporal.nn.attention import STConv

class STGCN(torch.nn.Module):
    def __init__(self, num_nodes, in_channels, hidden, features, edge_index, edge_weight):
        super(STGCN, self).__init__()
        self.num_nodes = num_nodes
        self.in_channels = in_channels
        self.features = features
        self.hidden = hidden
        self.edge_index, self.edge_weight = edge_index.T, edge_weight
        self.stconv1 = STConv(self.num_nodes, self.in_channels, self.hidden, features, 3, 3)
        self.linear1 = torch.nn.Linear(features, 10)
        self.linear2 = torch.nn.Linear(10, 1)
        self.dropout = torch.nn.Dropout(0.3)

    def forward(self, x):
        h = self.stconv1(x, self.edge_index, self.edge_weight)
        h = h.reshape(self.num_nodes, self.features)  # Assuming the shape after reshaping is correct
        
        # Apply ReLU and Linear layer to each node representation
        result = []
        for i in range(h.size(0)):
            k = F.elu(h[i, :])
            k = self.linear1(k)
            k = self.dropout(k)
            k = F.elu(k)
            result.append(self.linear2(k))
        
        # Stack the results into a tensor
        result = torch.stack(result)
        return result