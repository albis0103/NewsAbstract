from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, HttpUrl
from kafka import KafkaConsumer
import os
import threading
import json
from typing import List
import time


app = FastAPI(title='Dashboard API')
#set CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # 開發階段先允許所有來源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# setting mongodb atlas connection setting
MONGO_URI = "mongodb+srv://jasonwu:jason0103@cluster0.xvreqja.mongodb.net/newsdb?authSource=admin&retryWrites=true&w=majority"
client = AsyncIOMotorClient(MONGO_URI)
db = client['newsdb']
rss_collection = db['rss_source']

#data model (pydantic)
class RssSource(BaseModel):
    url:str
    name:str = "Custom RSS"
    is_active: bool = True
class RssSourceResponse(BaseModel):
    url:str



latest_news = []
def consume_kafka():
    # from backgrond, get the news from kafka persistently
    kafkabroker = os.getenv("KAFKA_BROKER", "localhost:9092")
    while True:
        consumer = None
        try:
            consumer = KafkaConsumer(
                'raw-security-news', #set Topic from crawler
                bootstrap_servers=[kafkabroker], 
                auto_offset_reset='earliest',
                value_deserializer=lambda x : json.loads(x.decode('utf-8'))
            )
            
            #push latest news to queue
            for message in consumer:
                latest_news.insert(0, message.value)
                # avoid buffer overflow
                if len(latest_news)>50:
                    latest_news.pop()
        except Exception as e:
            print(f"Kafka connect ERROR!:{e}")
            time.sleep(5)
        finally:
            if consumer is not None:
                consumer.close()
            time.sleep(5)
    
#when fastapi start new thread to run consume_kafka 
@app.on_event("startup")
def startup_event():
    thread = threading.Thread(target=consume_kafka,daemon=True )
    thread.start()

@app.get("/")
def root():
    return {"message":"Secops Dashboard api is running"}

@app.get("/api/news")
def get_latest_news():
    return{
        "status":"success", 
        "count":len(latest_news),
        "data":latest_news
    }

@app.get("/api/rss-sources", response_model=List[RssSourceResponse])
async def get_rss_resource():
    sources = []
    cursor = rss_collection.find({"is_active":True})
    async for doc in cursor:
        sources.append(RssSourceResponse(url=doc["url"]))
    return sources

@app.post("/api/rss-sources")
async def add_rss_source(source:RssSource):
    existing = await rss_collection.find_one({"url":source.url})
    if existing:
        return {"status":"error", "message":"RSS already existed!"}
    await rss_collection.insert_one(source.dict())
    return {"status":"success", "message":"insert RSS source successful"}

@app.delete("/api/rss-sources")
async def delete_rss_resource(source:RssSource):
    res = await rss_collection.delete_one({"url":source.url})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="source not found")
    return {"status":"success", "message":"Successfully deleted"}