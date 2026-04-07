from pymongo import MongoClient
CUSTOMER_FEATURES_DB = {
    "VGH北榮":["Medical", "In-house Development", "HIS system"],
    "CMU中國附醫":["Medical Center", "AIoT Healthcare Dev", "HIS Management"],
    "KLF 光隆":["Textile Manufacturing", "Digital Transformation IT", "ERP & SCM System"],
    "WVT 世展會":["NGO", "Cloud IT Operation", "Donor CRM System"],
    "REA 瑞昱":["Semiconductor IC Design", "High-Performance R&D IT", "EDA & PLM IS"],
    "FIC 大眾":["Electronics Manufacturing", "System Integration IT", "MES & ERP System"],
    "AXI 艾訊":["Industrial PC", "Embedded IT Dev", "ERP Management"],
    "TPT 尖點":["PCB Component", "Smart Factory IT", "MES System"],
    "BDD 閃銀":["Fintech", "Big Data AI Dev", "Risk Assessment IS"],
    "ADV 研華":["Industrial IoT", "AIoT In-house Dev", "Global ERP IS"],
    "STT 思達":["Semiconductor Testing", "Automated IT", "Data Analytics IS"],
    "CTN 科締納":["Networking IC", "In-house R&D IT", "EDA System"],
    "TUE 泰詠":["EMS Manufacturing", "Production IT", "MES & SCM IS"],
    "TSN 泰山":["Food & Beverage", "Enterprise IT Operation", "ERP & POS System"],
    "TYG 東陽":["Auto Parts", "Smart Manufacturing IT", "Global SCM System"],
    "WWU 旺旺":["FMCG Food", "Enterprise IT Operation", "Global ERP IS"],
    "MFMA 海能風電":["Renewable Energy", "Infrastructure IT", "SCADA Monitoring IS"],
    "CGM 長庚科技":["Medical Tech", "Healthcare IT Dev", "Smart HIS System"]
}
client = MongoClient('mongodb+srv://jasonwu:jason0103@cluster0.xvreqja.mongodb.net/newsdb?authSource=admin&retryWrites=true&w=majority')
db = client['newsdb']
collection = db['webhooks']
def init_database():
    try:
        # 1. 連線到 MongoDB (請換成你實際的連線字串)

        
        print("開始匯入資料...\n")
        success_count = 0
        
        for name, features in CUSTOMER_FEATURES_DB.items():
            # 使用 update_one + upsert=True
            # 如果找到相同 name 的文件，就更新(或新增) feature 欄位
            # 如果找不到，就新增一筆包含 name, feature, 以及 Java 預設 _class 的文件
            result = collection.update_one(
                {"name": name}, 
                {
                    "$set": {
                        "feature": features,
                        # 為了讓 Java Spring Data 認得這筆資料，我們手動補上 _class
                        "_class": "com.jasonwu.news_dispatcher.model.Customer" 
                    }
                },
                upsert=True 
            )
            
            if result.upserted_id:
                print(f"[新增] {name}")
            else:
                print(f"[更新] {name}")
            
            success_count += 1
            
        print(f"\n完成！成功處理 {success_count} 筆資料。")
        
    except Exception as e:
        print(f"寫入失敗: {e}")

if __name__ == "__main__":
    init_database()
        
    