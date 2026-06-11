from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from render_html import render_report

app = FastAPI(title='render-service')

class EventModel(BaseModel):
    title: list[str]
    date: list[str] = []
    scope: list[str] = []
    impact: list[str] = []
    summary: list[str] = []
    url: str = '#'
class RenderRequest(EventModel):
    events: list[EventModel]
    


@app('/render')
def render_api(req:RenderRequest):
    if len(req) != 3:
        raise HTTPException(status_code=400, detail='3 events is required !!!')
    events = [e.model_dump() for e in req.events]
    html = render_report(events)
    return{
        'html':html
    }



@app('/health')
def health():
    return{
        'status':'running'
    }