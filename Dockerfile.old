FROM idm-docker-staging.packages.idmod.org/ubuntu-mono-pythonnet:a49e9b7_1597089628

RUN apt-get update -y
# preempt tzdata install in the next line
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends tzdata
RUN apt-get install -y libtiff5-dev libjpeg8-dev libopenjp2-7-dev zlib1g-dev \
    libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python3-tk \
    libharfbuzz-dev libfribidi-dev libxcb1-dev

# These are here to support user scripts.
RUN pip3 install numpy matplotlib scipy

# This causes pythonnet to include /app in the list of folders
# it looks in for assemblies.
ENV PYTHONPATH=/app

COPY bin /app
COPY seir.py /app
COPY cmsmodel.py /app
