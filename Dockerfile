FROM ubuntu:16.04
MAINTAINER kainos

# Install Ruby and other OS stuff
RUN apt-get update && \
    apt-get install -y build-essential \
      bzip2 \
      ca-certificates \
      curl \
      gcc \
      git \
      libcurl3 \
      libcurl4-openssl-dev \
      wget \
      zlib1g-dev \
      libfontconfig \
      libxml2-dev \
      libxslt1-dev \
      make \
      python-pip \
      python2.7 \
      python2.7-dev \
      python3.5 \
      python3-pip && \
    rm -rf /var/lib/apt/lists/*

# sqlmap
WORKDIR /opt
ENV SQLMAP_PATH /opt/sqlmap/sqlmap.py
RUN git clone --depth=1 https://github.com/sqlmapproject/sqlmap.git

# dirb
COPY vendor/dirb222.tar.gz dirb222.tar.gz

RUN tar xvfz dirb222.tar.gz > /dev/null && \
    cd dirb222 && \
    chmod 755 ./configure && \
    ./configure && \
    make && \
    ln -s /opt/dirb222/dirb /usr/local/bin/dirb

ENV DIRB_WORDLISTS /opt/dirb222/wordlists

# nmap
RUN apt-get update && \
    apt-get install -y nmap && \
    rm -rf /var/lib/apt/lists/*

# Required Python libraries
RUN pip3 install --upgrade pip
RUN pip3 install requests
RUN pip3 install sslyze
RUN pip3 install trufflehog

# sslyze
RUN pip install --upgrade setuptools && \
    pip install --upgrade sslyze
ENV SSLYZE_PATH /usr/local/bin/sslyze

# Allow Python modules to be imported
ENV PYTHONPATH "${PYTHONPATH}:/working/attackfiles"

COPY bin/attacker.py /usr/local/bin/attacker.py
ENTRYPOINT [ "/usr/local/bin/attacker.py" ]
