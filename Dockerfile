FROM ubuntu:resolute as base
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
RUN wget "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh"
RUN bash Miniforge3-Linux-x86_64.sh -b -p "${CONDA_DIR}"
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
RUN pip install --upgrade pip requests pyopenssl
RUN chmod 777 -R /opt/conda


FROM base
WORKDIR /usr/src/graphsimviz/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN conda install conda python=3.10

RUN pip install --upgrade pip
# conda-forge ships graph-tool builds per x86-64 microarchitecture level (v1/v3/v4) and picks one by the
# CPU of the build machine. The CI runner has AVX2/AVX-512, the server may not (SIGILL at runtime), so
# force the baseline builds: override the detected CPU and pin the level explicitly.
ENV CONDA_OVERRIDE_ARCHSPEC=x86_64
RUN mamba install -c conda-forge -y graph-tool==2.98 "_x86_64-microarch-level=1" pandas scipy numpy seaborn networkx progress

RUN pip install psycopg2-binary poetry poetry-plugin-export
WORKDIR /usr/src/graphsimviz/

COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes
RUN pip install --no-cache-dir -r requirements.txt

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

