import sys
import os
import requests
from google import genai  # 使用新版 SDK
from dotenv import load_dotenv

# 載入 .env 檔案
load_dotenv()

# ---------------------------------------------------------
# 負責抓取網頁內容
# ---------------------------------------------------------
def readnew(url):
    jina_url = f"https://r.jina.ai/{url}"
    try:
        response = requests.get(jina_url, timeout=10) # 建議加上 timeout 防止掛掉
        if response.status_code == 200:
            return response.text
        return None
    except Exception:
        return None

# ---------------------------------------------------------
# 負責呼叫 Gemini API
# ---------------------------------------------------------
def call_gemini(prompt, article_text, api_key):
    client = genai.Client(api_key=api_key)
    
    full_text = f"{prompt}\n\n以下是新聞全文：\n{article_text}"
    
    try:
        # 推薦使用 2.0-flash，速度快且對資安摘要效果極佳
        response = client.models.generate_content(
            model='gemini-2.5-pro', 
            contents=full_text
        )
        return response.text
    except Exception as e:
        return f"❌ 呼叫 Gemini 時發生錯誤: {e}"

# ---------------------------------------------------------
# 生成摘要
# ---------------------------------------------------------
def generate_summary(url, api_key):
    article_text = readnew(url)
    if not article_text:
        return "❌ 網頁抓取失敗，請確認網址或爬蟲限制。"
        
    prompt = """
    請以資安專家的角度閱讀新聞，並生成固定的信件格式。
    包含三個區塊：
    1. [事件摘要]：簡述重點(200字內)。
    2. [威脅與影響分析]：分析此事件對企業或系統的潛在衝擊。(50字)
    3. [防禦與修補建議]：列出具體的可行建議。(50字)
    """
    return call_gemini(prompt, article_text, api_key)

# ---------------------------------------------------------
# 4. 主程式 (系統進入點)
# ---------------------------------------------------------
def main():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        #此為測試網址
        target_url = "https://www.ithome.com.tw/news/161000"
        print("❌ 系統錯誤：找不到 API Key，請檢查 .env 檔案。", file=sys.stderr)
        sys.exit(1)
#python3 ai_service.py https://examplenews.com 長度 = 2
    if len(sys.argv) < 2:
        print("❌ 缺少參數！請提供 URL。", file=sys.stderr)
        sys.exit(1)
        
    target_url = sys.argv[1]
    final_result = generate_summary(target_url, api_key)
    print(final_result)

if __name__ == "__main__":
    main()