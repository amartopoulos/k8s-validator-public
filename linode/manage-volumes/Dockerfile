#FROM python:3.10.0-slim-bullseye
FROM python:3.10-alpine
RUN pip install linode_api4
COPY linode-manage-volumes.py .
CMD ["python3", "linode-manage-volumes.py"]
