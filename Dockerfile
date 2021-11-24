FROM mas.ops.maap-project.org/root/jupyter-image/vanilla:develop

COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
