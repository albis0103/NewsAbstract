#1. assign base immage
FROM python:3.13-slim AS builder
#2.set containner working scope(directory)
WORKDIR /app
RUN pip install --no-cache-dir --upgrade pip
RUN apt-get update && apt-get install -y gcc g++ build-essential libxml2-dev libxslt1-dev

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

#build Rust compile env
#RUN curl https://sh.rustup.rs -sSf | sh -s -- -y
#ENV PATH="/root/.cargo/bin:${PATH}"
#3.construct env copy req.txt and install it
COPY requirements.txt .
RUN pip install --no-cache-dir -v -r requirements.txt

# stage 2.
FROM python:3.13-slim
WORKDIR /app
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
#4.copy all from news-analyzer-py (include model)
COPY . .
#5.deploy the port 8000
EXPOSE 8000

#6. set the container default instruction, set the socket that ip 0.0.0.0:8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
