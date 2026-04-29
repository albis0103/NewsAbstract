from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import json 

load_dotenv()

from news_summary import generate_summary
from similarity import get_customer_feature, calculate_customer_similarity, model

app = FastAPI(title="news-nlp-api")

#define the receive JSON format from frontend
class NewsUrlRequest(BaseModel):
    url:str
class SimilarityRequest(BaseModel):
    keyword:str
#Api Endpoint 1 : news summary
@app.post("/api/v1/summarize")
def summarize_api(req : NewsUrlRequest):
    apikey = os.getenv("GEMINI_API_KEY")
    if not apikey:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY is not set in .env")
    
    result = generate_summary(req.url, api_key=apikey)
    
    if result.startswith("❌"):
        raise HTTPException(status_code=400, detail=result)
    
    return {"stdout": result}
#APi Endpoint 2 : customer similarity
@app.post("/api/v1/similarity")
def similarity_api(req : SimilarityRequest):
    try:
        news_keyword = [k.strip() for k in req.keyword.split(',') if k.split()]

        results = {}

        db_customer_feature = get_customer_feature()
        for customer_name, features in db_customer_feature.items():
            final_similarity = calculate_customer_similarity(features, news_keyword=news_keyword, model=model)
            results[customer_name] = round(float(final_similarity), 4)
        return {"stdout" : json.dumps(results, ensure_ascii=False)}
    except Exception as e :
        raise HTTPException(status_code=500, detail=str(e))

#state monitor endpoint(let to check container be health)
@app.get("/health")
def health_check():
    return{"status" : "running", "word2vec_model_loaded" : model is not None}
