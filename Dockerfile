FROM ubuntu:noble as base
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV TZ=Europe/Berlin
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && apt-get dist-upgrade -y && apt-get install -y supervisor libgtk-3-dev wget apt-utils nginx
RUN apt-get update && apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release software-properties-common cron unzip zip
RUN apt-get autoclean -y && apt-get autoremove -y && apt-get clean -y

ENV CONDA_DIR /opt/conda
RUN wget "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
RUN bash Miniforge3-$(uname)-$(uname -m).sh -b -p "${CONDA_DIR}"
ENV PATH=$CONDA_DIR/bin:$PATH
RUN chmod +x "${CONDA_DIR}/etc/profile.d/conda.sh"
RUN "${CONDA_DIR}/etc/profile.d/conda.sh"
RUN chmod +x "${CONDA_DIR}/etc/profile.d/mamba.sh"
RUN "${CONDA_DIR}/etc/profile.d/mamba.sh"

RUN conda init bash

RUN mamba update -n base -c defaults mamba conda
RUN mamba install -y python=3.10
RUN mamba update -y --all
RUN pip install pip==23
RUN pip install --upgrade pip requests cryptography pyopenssl
RUN chmod 777 -R /opt/conda


FROM base
WORKDIR /usr/src/graphsimviz/

RUN conda install conda python=3.9

RUN pip install --upgrade pip
RUN conda install -c conda-forge -y graph-tool==2.57

RUN pip install --upgrade cryptography

RUN conda install -c conda-forge -y pandas scipy numpy seaborn networkx progress

RUN pip install psycopg2-binary
COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

WORKDIR /usr/src/graphsimviz/

COPY . .
RUN rm -rf networks


WORKDIR /usr/src/data/
RUN mv /usr/src/graphsimviz/data/download_files.sh .
RUN rm -rf /usr/src/graphsimviz/data
RUN ./download_files.sh

WORKDIR /usr/src/
RUN wget -q https://cloud.uni-hamburg.de/public.php/dav/files/Rw3McfsN7eSLHfG/?accept=zip -O graphs.zip
RUN unzip -q graphs.zip
RUN rm graphs.zip
WORKDIR /usr/src/graphs/disease_disease

WORKDIR /usr/src/graphsimviz/

COPY ./supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 8000

