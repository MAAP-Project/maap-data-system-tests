FROM mas.ops.maap-project.org/root/jupyter-image/vanilla:develop

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
