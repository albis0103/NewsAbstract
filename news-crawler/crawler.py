import feedparser
from kafka import KafkaProducer
import json
import requests
import time
import os


broker = os.getenv("KAFKA_BROKER", "localhost:9092")
producer = None
while producer is None:
    try:
        producer = KafkaProducer(
            bootstrap_servers = [broker],
            api_version=(0, 10),  
            value_serializer = lambda v: json.dumps(v).encode('utf-8'),
            request_timeout_ms=10000
        )
    except Exception as e:
        print(f"Kafka not ready (NoBrokersAvailable), retrying in 5s... Error: {e}")
        time.sleep(5)
def FetchRSS(rss_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Accept': 'application/rss+xml, application/xml, text/xml, */*'
    }
    try:
        response = requests.get(rss_url, headers=headers, timeout=10)
        if response.status_code == 200:
            feed = feedparser.parse(response.content)
            if feed.bozo:
                print(feed.bozo_exception)

            #get the entity need field
            for entry in feed.entries:
                news_data = {
                    "title":entry.get("title", ""), 
                    "link":entry.get("link", ""), 
                    "summary":entry.get("summary", ""), 
                    "publish":entry.get("publish", ""), 
                    "categoies":[tag.term for tag in entry.get("tags", [])]
                }

                producer.send("raw-security-news", news_data)
                print(f"send to kafka:{news_data['title']}")
            producer.flush()
        else:
            print(f"web deny access:{response.status_code}")
    except Exception as e:
        print(f"passing{rss_url} error {e}")




def run_crawler_job():
    api_url = os.getenv("API_URL", "http://localhost:8001/api/rss-sources")
    while True:
        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                rss_list = response.json()
                if not rss_list:
                    print("empty for RSS source")
                    return
                print(f"get the {len(rss_list)} RSS sources")
                for item in rss_list:
                    url = item['url']
                    print(f"start process source:{url}")
                    FetchRSS(url)
                print("all RSS source crawler finish")
            else:
                print(f"can't get RSS list, api response:{response.status.code}")
                time.sleep(5)
        except Exception as e:
            print(f"API connection error{e}")
            time.sleep(5)

if __name__ == "__main__":
    run_crawler_job()