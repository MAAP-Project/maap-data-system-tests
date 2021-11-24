FROM mas.ops.maap-project.org/root/jupyter-image/vanilla:develop

RUN pip install maappy_helpers
COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
