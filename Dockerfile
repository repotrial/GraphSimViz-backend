FROM ubuntu:latest
WORKDIR /usr/src/graphsimviz/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV TZ=Europe/Berlin
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update --no-install-recommends && apt-get upgrade -y && apt-get install -y supervisor nginx libgtk-3-dev wget git unzip
RUN apt-get autoclean -y && apt-get autoremove -y


ENV CONDA_DIR /opt/conda
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-py38_4.12.0-Linux-x86_64.sh -O ~/miniconda.sh && /bin/bash ~/miniconda.sh -b -p /opt/conda
ENV PATH=$CONDA_DIR/bin:$PATH
RUN conda init bash

RUN conda install conda python=3.8
RUN conda install -c conda-forge -y django=4.0.2

RUN conda install -c conda-forge -y graph-tool==2.45

RUN conda install -c conda-forge -y pandas scipy numpy seaborn networkx progress rise

RUN pip install psycopg2-binary
COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY ./data /usr/src/data
WORKDIR /usr/src/data
RUN unzip -q \*.zip
RUN rm *.zip

WORKDIR /usr/src/

RUN apt-get install -y ssh git
RUN mkdir ~/.ssh/
RUN ssh-keyscan github.com >> ~/.ssh/known_hosts
RUN git clone https://github.com/repotrial/graphsimqt.git
RUN mv graphsimqt/data/graphs .
RUN rm -rf graphsimqt

WORKDIR /usr/src/graphsimviz/

COPY . .
RUN rm -rf data

COPY ./supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 8000
