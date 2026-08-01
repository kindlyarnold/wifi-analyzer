# Stage 1: Builder
FROM debian:bookworm-slim AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    nmap \
    hydra \
    openssh-client \
    curl \
    python3-minimal \
    && rm -rf /var/lib/apt/lists/*

# Stage 2: Runtime
FROM debian:bookworm-slim

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    nmap \
    hydra \
    openssh-client \
    curl \
    iputils-ping \
    net-tools \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy WiFi analyzer script
COPY wifi_analyzer.py .
RUN chmod +x wifi_analyzer.py

# Create output directory
RUN mkdir -p /output && chmod 777 /output

# Create non-privileged user
RUN useradd -m -u 1001 analyzer && \
    chown -R analyzer:analyzer /app /output

USER analyzer

ENTRYPOINT ["python3", "wifi_analyzer.py"]
CMD ["-h"]
