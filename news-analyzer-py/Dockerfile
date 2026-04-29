#1. assign base immage
FROM python:3.13
MAINTAINER JasonWu

#2.set containner working scope(directory)
WORKDIR /app
RUN pip install --no-cache-dir --upgrade pip
RUN apt-get update && apt-get install -y gcc g++ build-essential
#3.construct env copy req.txt and install it

#build Rust compile env
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

COPY requirements.txt .
RUN pip install --no-cache-dir -v -r requirements.txt

#4.copy all from news-analyzer-py (include model)
COPY . .
#5.deploy the port 8000
EXPOSE 8000

#6. set the container default instruction, set the socket that ip 0.0.0.0:8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
