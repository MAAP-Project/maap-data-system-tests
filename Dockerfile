FROM mas.ops.maap-project.org/root/jupyter-image/vanilla:develop

RUN wget -qO-  https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux32.tar.gz | tar xvz - -C /usr/bin && \
      chmod +x /usr/bin/geckodriver

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
