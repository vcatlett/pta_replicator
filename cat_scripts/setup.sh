conda create --name pta_replicator-3.10 python=3.10 -y
conda activate pta_replicator-3.10
conda install pip -y
conda install -c conda-forge enterprise-pulsar -y
pip install pint-pulsar python-dotenv ipykernel
