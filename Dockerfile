FROM continuumio/miniconda3:4.7.12

RUN pip install --no-cache-dir --upgrade pip --update setuptools

# install maap-py library
ENV MAAP_CONF='/projects/maap-py/'
RUN git clone --single-branch --branch master https://github.com/MAAP-Project/maap-py.git \
    && cd maap-py \
    && pip install --no-cache-dir -e .

# install testing requirements
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
