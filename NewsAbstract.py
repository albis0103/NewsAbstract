import requests
import getpass
import google.generativeai as genai

# 假設您原本的 readnew 函數還在 (如果您用 Jina API 抓網頁的話)
def readnew(url):
    print(f"[*] 正在透過 Jina Reader 抓取網頁內容...")
    jina_url = f"https://r.jina.ai/{url}"
    response = requests.get(jina_url)
    if response.status_code == 200:
        filename = "orig.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"[+] 成功抓取內容並儲存至 {filename}")
        return filename
    else:
        print(f"[-] 抓取失敗")
        return None

# ---------------------------------------------------------
# 改寫為 Gemini API 專用的呼叫函數
# ---------------------------------------------------------
def call_gemini(prompt, filename, api_key):
    print(f"[*] 正在連線至 Gemini API 並上傳新聞內容...")

    # 1. 設定您的 API Key
    genai.configure(api_key=api_key)

    # 2. 讀取檔案內容
    with open(filename, "r", encoding="utf-8") as f:
        file_content = f.read()

    # 3. 組合您的 Prompt 指令與新聞內容
    full_text = f"{prompt}\n\n以下是新聞全文：\n{file_content}"

    # 4. 指定模型 (使用 Gemini 1.5 Pro，非常適合處理超長文本與複雜邏輯)
    model = genai.GenerativeModel('gemini-2.5-pro')

    # 5. 直接發送並等待回傳 (不需要寫迴圈 Polling！)
    print("[*] Gemini 正在分析中，請稍候...")
    
    try:
        response = model.generate_content(full_text)
        print(f"[+] 成功接收到 Gemini 回覆！")
        return response.text
    except Exception as e:
        return f"[-] 呼叫 Gemini 時發生錯誤: {e}"

# ---------------------------------------------------------
# 主程式
# ---------------------------------------------------------
def main():
    # 安全地輸入 Google Gemini API Key
    # (可至 https://aistudio.google.com/app/apikey 免費申請)
    api_key = "AIzaSyDh5ZDxKj_jEgGOLpkfNKx0eZPBGxtGQUo"

    url = input("請輸入新聞網址: ")
    orig_txt_name = readnew(url)

    if orig_txt_name:
        # 您原本設定的專業 Prompt
        prompt = """
        請以資安專家的角度，幫我將這篇新聞生成摘要、初稿，並轉換為固定的信件格式。
        信件請包含以下三個區塊）：
        1. [事件摘要]：(150字)
        2. [威脅與影響分析]：分析此事件對企業或系統的潛在衝擊。(50字)
        3. [防禦與修補建議]：列出具體的可行建議。(50字)
        """

        # 呼叫 Gemini Agent
        news_abs = call_gemini(prompt, orig_txt_name, api_key)

        print("\n================ Gemini 產出結果 ================\n")
        print(news_abs)
        print("\n=================================================\n")

if __name__ == "__main__":
    main()