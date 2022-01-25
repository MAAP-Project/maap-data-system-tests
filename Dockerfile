FROM continuumio/miniconda3:4.7.12

RUN mkdir /projects
WORKDIR /projects
RUN sed -i -e 's/\/root/\/projects/g' /etc/passwd

# Remove the DST Root CA X3 certificate and update certs. 
# We should consider removing these two commands after upgrading from miniconda3:4.7.12
# For more info, see: https://letsencrypt.org/docs/dst-root-ca-x3-expiration-september-2021/
RUN sed -i 's/mozilla\/DST_Root_CA_X3.crt/!mozilla\/DST_Root_CA_X3.crt/g' /etc/ca-certificates.conf
RUN update-ca-certificates

# To use dependency resolver from the latest pip version
RUN pip install --no-cache-dir --upgrade pip

# install maap-py library
ENV MAAP_CONF='/projects/maap-py/'

RUN git clone --single-branch --branch master https://github.com/MAAP-Project/maap-py.git \
    && cd maap-py \
    && pip install --no-cache-dir -e .

RUN touch /root/.bashrc && echo "cd /projects >& /dev/null" >> /root/.bashrc
RUN echo "PATH=/opt/conda/bin:${PATH}" >> /etc/environment

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
