import sys
import os
import requests
from google import genai  # 使用新版 SDK
from dotenv import load_dotenv
from pathlib import Path

sys.stdout.reconfigure(encoding = 'utf-8')#強制utf編碼
# 取得目前這個程式碼檔案的路徑，並找到它旁邊的 .env
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)


# 負責抓取網頁內容
def readnew(url):
    jina_url = f"https://r.jina.ai/{url}"
    jina_api_key = os.getenv("JINA_API_KEY")
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36", 
        "Authorization":f"Bearer {jina_api_key}"
    }
    try:
        response = requests.get(jina_url,headers = headers, timeout=20) # 加上 timeout 
        if response.status_code == 200:
            return response.text
        return None
    except Exception:
        return None


# 負責呼叫 Gemini API
def call_gemini(prompt, api_key):
    client = genai.Client(api_key=api_key)
    
    try:
        # 推薦使用 2.0-flash，速度快且對資安摘要效果極佳
        response = client.models.generate_content(
            model='gemini-2.5-flash', 
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"❌ 呼叫 Gemini 時發生錯誤: {e}"


# 生成摘要
def generate_summary(url, api_key):
    article_text = readnew(url)
    if not article_text:
        return "❌ 網頁抓取失敗，請確認網址或爬蟲限制。"
        
    prompt = """請以資安專家的角度閱讀新聞，以純文字依照下列結構生成一份「技術情報摘要」。請確保用詞精確（例如：Passkey、Entra ID、FIDO2），並嚴格遵守以下格式：

1. [標題]：簡潔標記新聞核心重點。

2. [關鍵字]：取 5-8 個最能代表本文精髓的關鍵字（Hashtag）

3. [發生時間]：
   - 正式發布：(標註具體日期)
   - 預計部署：(標註部署時程或預計影響時間)

4. [影響範圍]：
   - 作業系統版本：(註明受影響或支援的系統)
   - 適用對象：(說明適用的使用者等級或特定的企業驗證環境)

5. [潛在影響]：
   - 深入分析該功能的核心價值。需包含技術原理（如：Challenge-Response、數位簽章）、防禦能力（如：防範釣魚、MitM 攻擊）以及對無密碼（Passwordless）趨勢的推動。

6. [重點整理]：(整段式表達, max:160字)
   - 使用此功能的必要條件：(以列點方式說明硬體、軟體或帳號設定要求)
   - 操作流程簡述：(描述使用者端的操作路徑，如選單路徑或驗證方式)

7. [新聞網址]：(放入來源連結, 整段式表達, max:160字)
    """
    full_text = f"{prompt}\n\n以下是新聞全文：\n{article_text}"
    return call_gemini(full_text, api_key)

# ---------------------------------------------------------
# 4. 主程式 (系統進入點)
# ---------------------------------------------------------
def main():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
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