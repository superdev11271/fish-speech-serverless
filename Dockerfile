ARG VERSION=server-cuda
FROM fishaudio/fish-speech:${VERSION}

USER root
WORKDIR /app

# Model checkpoints are NOT baked into the image — bind-mount them at runtime:
#   docker run -v ./checkpoints:/app/checkpoints ...
# See README.md for how to fetch them on the host.

COPY ./src /app/src
RUN chmod +x /app/src/run.sh

ENV PYTHONPATH="/app:/app/src"

EXPOSE 8080

ENTRYPOINT ["/app/src/run.sh"]
