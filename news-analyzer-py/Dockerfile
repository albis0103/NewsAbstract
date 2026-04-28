#1. assign base immage
FROM python:3.10-slim
MAINTAINER JasonWu

#2.set containner working scope(directory)
WORKDIR /app

#3.construct env copy req.txt and install it
RUN pip install fastapi, uvicorn
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#4.copy all from news-analyzer-py (include model)
COPY . .
#5.deploy the port 8000
EXPOSE 8080

#6. set the container default instruction
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
