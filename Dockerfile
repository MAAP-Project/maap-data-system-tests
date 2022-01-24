FROM mas.ops.maap-project.org/root/jupyter-image/vanilla:develop

RUN apt-get update && \
      apt-get install firefox-esr -y && \
      apt-get clean

RUN wget -qO- https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux32.tar.gz | tar --transform 's/-.*/geckodriver/' -xvz && \
      mv geckodriver /usr/bin/geckodriver && \
      chmod +x /usr/bin/geckodriver

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY entrypoint.sh /entrypoint.sh

USER 1001

ENTRYPOINT ["/entrypoint.sh"]
