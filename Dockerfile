FROM ubuntu:18.04

# Set up tools to install latest stable mono.
RUN apt-get update && apt-get install -y \
    	    dirmngr \
	    gnupg \
    	    apt-transport-https \
    	    ca-certificates \
    &&  rm -rf /var/lib/apt/lists/*
  
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 3FA7E0328081BFF6A14DA29AA6A19B38D3D831EF \
    && echo "deb https://download.mono-project.com/repo/ubuntu stable-bionic main" | tee /etc/apt/sources.list.d/mono-official-stable.list \
    && apt update \
    && apt install -y \
       	   mono-complete \
	   ca-certificates-mono \
	   clang \
	   libglib2.0-dev \
	   python3 \
	   python3-pip \
    && rm -rf /var/lib/apt/lists/* \
    && mono --version
  
COPY bin /app

RUN pip3 install --egg pythonnet
RUN pip3 install numpy
RUN pip3 install matplotlib
RUN pip3 install scipy

# This causes pythonnet to include /app in the list of folders
# it looks in for assemblies.
ENV PYTHONPATH=/app