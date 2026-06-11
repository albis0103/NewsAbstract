from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from render_html import render_report
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title='render-service')
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class EventModel(BaseModel):
    title: list[str]
    date: list[str] = []
    scope: list[str] = []
    impact: list[str] = []
    summary: list[str] = []
    url: str = '#'
class RenderRequest(BaseModel):
    events: list[EventModel]
    


@app.post('/render')
async def render_api(req:RenderRequest):
    if len(req.events) != 3:
        raise HTTPException(status_code=400, detail='3 events is required !!!')
    events = [e.model_dump() for e in req.events]
    html = render_report(events)
    return{
        'html':html
    }



@app.get('/health')
def health():
    return{
        'status':'running'
    }