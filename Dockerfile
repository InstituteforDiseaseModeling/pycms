FROM idm-docker-staging.packages.idmod.org/ubuntu-mono-pythonnet:a49e9b7_1597089628

# These are here to support user scripts.
RUN pip3 install numpy matplotlib scipy

# This causes pythonnet to include /app in the list of folders
# it looks in for assemblies.
ENV PYTHONPATH=/app

COPY bin /app
