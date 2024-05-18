FROM python:3.11.9

WORKDIR /app

RUN pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cpu
RUN pip install pyg_lib torch_scatter torch_sparse torch_cluster torch_spline_conv -f https://data.pyg.org/whl/torch-2.3.0+cpu.html

ADD requirements.txt requirements.txt

RUN pip install -r requirements.txt

RUN apt-get update && apt-get install ffmpeg libgl1 libsm6 libxext6  -y

ADD data data
ADD weights weights
ADD app.py .
ADD graph.py .
ADD cut.mp4 .
ADD stgn.py .

RUN rm /usr/local/lib/python3.11/site-packages/torch_geometric_temporal/nn/attention/tsagcn.py

ADD tsagcn.py /usr/local/lib/python3.11/site-packages/torch_geometric_temporal/nn/attention/tsagcn.py

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]