FROM alpine:3.20
CMD ["sh", "-c", "echo GHCR OK; echo arch=$(uname -m); sleep 3600"]
