FROM ghcr.io/astral-sh/uv:0.9.1

WORKDIR /app

# Build TA-Lib
RUN apt-get update && \
    apt-get install -y --no-install-recommends wget gcc build-essential && \
    rm -rf /var/lib/apt/lists/* && \
    wget https://github.com/ta-lib/ta-lib/releases/download/v0.6.4/ta-lib-0.6.4-src.tar.gz && \
    tar -xzf ta-lib-0.6.4-src.tar.gz && \
    cd ta-lib-0.6.4 && \
    ./configure --prefix=/usr && \
    make && \
    make install && \
    cd .. && \
    rm -rf ta-lib-0.6.4 ta-lib-0.6.4-src.tar.gz

COPY pyproject.toml uv.lock .python-version ./

# RUN uv sync && .venv/Scripts/activate.sh
