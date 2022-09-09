# FROM nvidia/cuda:11.3.1-cudnn8-devel-ubuntu18.04
FROM nvidia/cuda:11.6.2-devel-ubuntu20.04

LABEL maintainer="Solovyanov M. <miksolo@yandex.ru>"

ENV LANG C.UTF-8
ENV DEBIAN_FRONTEND noninteractive
ENV MPLLOCALFREETYPE 1


RUN apt update && apt install -y software-properties-common

RUN add-apt-repository ppa:deadsnakes/ppa && apt update

RUN apt install -y \
    build-essential \
    git \
    wget \
    vim \
    curl \
    zip \
    # zlib1g-dev \
    unzip \
    pkg-config \
    libgl-dev \
    libblas-dev \
    liblapack-dev \
    libsndfile1 \
    # python3-tk \
    python3-wheel \
    # graphviz \
    libhdf5-dev \
    python3.10 \
    python3-dev \
    # python3.10-distutils 
    python3-distutils
    
# RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py &&\
#     python3 get-pip.py &&\
#     rm get-pip.py &&\
#     # best practice to keep the Docker image lean
#     rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN apt install python3-pip -y

RUN python3 -m pip --no-cache-dir install \
    numpy \
    matplotlib \
    scipy \
    pandas \
    jupyter

RUN pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu116

RUN mkdir  -p /python_requirements
# Copy req.
COPY model_processing/requirements.txt  /python_requirements/requirements.txt

# Install essential Python packages
RUN pip install --no-cache-dir --upgrade -r /python_requirements/requirements.txt

WORKDIR /src

# Add profiling library support
ENV LD_LIBRARY_PATH /usr/local/cuda/extras/CUPTI/lib64:${LD_LIBRARY_PATH}

# Export port for Jupyter Notebook
EXPOSE 8888


# By default start running jupyter notebook
ENTRYPOINT ["jupyter-notebook", "--allow-root" , "--no-browser" , "--ip=0.0.0.0" ]