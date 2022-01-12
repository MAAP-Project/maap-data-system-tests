FROM mas.ops.maap-project.org/root/jupyter-image/vanilla:develop

RUN pip install pytest

COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
