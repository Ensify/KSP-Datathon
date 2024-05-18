# GCN

## Description

This is a modified implementation of the Spatial Temporal Graph Convolutional Network propsed in the paper [Spatio-Temporal Graph Convolutional Networks: A Deep Learning Framework for Traffic Forecasting](https://arxiv.org/pdf/1709.04875)

The model is trained with synthetic traffical data.The road network is represented as a graph with every point with cctv as a node. The model can predict traffic after 30 mins into the future given current traffic patterns.

## Features
- Considers seasonal traffic
- Takes into account of peak hours
- Weekdays and monthly patterns are also considered by the model
- Gives predictions for every node
- Can perform online training to improve performance based on current traffic patterns
                
## Uses
- It is used to predict potential traffic congestion proactively
- Anomaly detection to compare predicted traffic with actual traffic to detect unusual traffic due to accident or congestion.

### Note
- This is trained and tested on dummy data. The model is verified to capture cyclic traffic patterns based on current traffic patterns and time. For accurate results real live data is needed.