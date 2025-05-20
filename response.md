# Response
## What is this project about?
This project is a backend API server built with <ins>**FastAPI**</ins> and <ins>**PostgreSQL**</ins>, designed to support frontend features such as:
- Listing pharmacies open at a given time and weekday
- Searching for mask products by name
- Computing the sales performance of masks at a pharmacy
## A. Required Information
### A.1. Requirement Completion API List
- ✅ List all pharmacies open at a specific time and on a day of the week if requested.
  - Implemented at ***Get_Open_Pharmacies*** API, file located at path: `/app/api/pharmacies_open.py`
- ✅ List all masks sold by a given pharmacy, sorted by mask name or price.
  - Implemented at ***Get_Pharmacy_Masks_Sort*** API, file located at path: `/app/api/pharmacies_mask_sort.py`
- ✅ List all pharmacies with more or less than x mask products within a price range.
  - Implemented at ***Filter_Pharmacies_By_Mask_Count*** API, file located at path: `/app/api/pharmacies_mask_filter.py`
- ✅ The top x users by total transaction amount of masks within a date range.
  - Implemented at ***Get_Top_Users_By_Transaction_Count*** API, file located at path: `/app/api/users_transaction_top.py`
- ✅ The total number of masks and dollar value of transactions within a date range.
  - Implemented at ***Get_Sales_Summary*** API, file located at path: `/app/api/sales_summary.py`
- ✅ Search for pharmacies or masks by name, ranked by relevance to the search term.
  - Implemented at ***Relevance_Search*** API, file located at path: `/app/api/relevance_search.py`
- ✅ Process a user purchases a mask from a pharmacy, and handle all relevant data changes in an atomic transaction.
  - Implemented at ***Purchase_Mask*** API, file located at path: `/app/api/purchase.py`
### A.2. API Document
> {baseURL} = http://127.0.0.1:8000  
> <sup>*</sup> mean params is required

1. ***Get_Open_Pharmacies*** API  [GET]
   - `{baseURL}/pharmacies/open`
   - params: hour(str), minute(str),weekday(str)
   - return example:
     ```json
     {
      "time": "18:20",
      "weekday": "Tue",
      "open_pharmacies": []
     }
     ```
2. ***Get_Pharmacy_Masks_Sort*** API  [GET]
   - `{baseURL}/pharmacies/masks`
   - params: <sup>*</sup>pharmacy_id(int), sort_by(str), order(str)
   - return example:
     ```json
     {
      "pharmacy_id": 1,
      "pharmacy_name": "DFW Wellness",
      "sort_by": "price",
      "order": "descending",
      "masks": [
          {
            "name": "MaskT (green) (10 per pack)",
            "price": 41.86
          },
          {
            "name": "Second Smile (black) (10 per pack)",
            "price": 31.98
          },
          {
            "name": "True Barrier (green) (3 per pack)",
            "price": 13.7
          }
        ]    
      }
     ```
     
3. ***Filter_Pharmacies_By_Mask_Count*** API [GET]
   - `{baseURL}/pharmacies/filter-mask-price`
   -  params: <sup>*</sup>min_price(float), <sup>*</sup>max_price(float), <sup>*</sup>threshold(int), <sup>*</sup>comparison(str)
   -  return example:
      ```json
      [
        {
          "id": 9,
          "name": "Centrico",
          "mask_count": 5
        },
        {
          "id": 15,
          "name": "HealthMart",
          "mask_count": 3
        }
      ]
      ```
4. ***Get_Top_Users_By_Transaction_Count*** API  [GET]
   - `{baseURL}/users/top-users-by-transaction-amount`
   - params: start_date(str), end_date(str), top_n(int)
   - return example:
     ```json
      [
        {
          "user_id": 1,
          "name": "Yvonne Guerrero",
          "transaction_count": 13
        },
        {
          "user_id": 9,
          "name": "Marilyn Cruz",
          "transaction_count": 9
        }
      ]
     ```
5. ***Get_Sales_Summary*** API  [GET]
   - `{baseURL}/sales/sales-summary`
   - params: start_date(str), end_date(str)
   - return example:
     ```json
      {
        "total_mask_sales": 107,
        "total_transaction_value": 1945.42
      }
     ```
6. ***Relevance_Search*** API  [GET]
   - `{baseURL}/search/`
   - params: <sup>*</sup>keyword(str), target(str), limit(int)
   - return example:
     ```json
      [
        {
          "type": "pharmacy",
          "id": 7,
          "name": "Health Warehouse",
          "relevance": 0.4
        },
        {
          "type": "pharmacy",
          "id": 15,
          "name": "HealthMart",
          "relevance": 0.375
        },
        {
          "type": "pharmacy",
          "id": 6,
          "name": "Health Mart",
          "relevance": 0.3529
        }
      ]
     ```
7. ***Purchase_Mask*** API  [POST]
   - `{baseURL}/users/`
   - body example:
     ```json
     {
       "pharmacy_id": 0,
       "mask_id": 0,
       "Date": "2025-05-20T11:31:23.736Z",
       "user_id": 0
     }
     ```
   - return example:
     ```json
      {
        "message": "購買成功",
        "user": "Yvonne Guerrero",
        "mask": "True Barrier (green) (3 per pack)",
        "pharmacy": "DFW Wellness",
        "Amount": 13.7,
        "Date": "2025-05-20 10:32:38"
      }
     ```

### A.3. Environment Setting
使用Python在MacOS虛擬環境中使用 **FastAPI + SQLAlchemy + PostgreSQL** 框架開發此網頁後端專案，其中PostgreSQL透過docker容器化部署。

首先，建立一個設定檔`.env`及[docker-compose.yml](docker-compose.yml)作為資料庫連線資訊：
> 兩檔案的使用者名稱、密碼、資料庫名稱等設定需一致
```env
# .env example
POSTGRES_USER=steven
POSTGRES_PASSWORD=secret
POSTGRES_DB=phantom_mask
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

DATABASE_URL=postgresql+asyncpg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}
```

並安裝docker將PostgreSQL在容器中運行：
```bash
$ brew install docker
$ docker-compose up -d
```
可查看容器運行狀態是否正常：
```bash
$ docker ps -a
```
因為有設定volume外部掛載，所以容器重新啟動不會導致資料消失，且自動執行`init.sql`初始化資料表。

再來，執行`requirements.txt`一次安裝API開發的依賴項及函示庫：
```bash
$ pip install -r requirements.txt
```
使用支援ASGI協議的Uvicorn啟動網頁伺服器：
```bash
$ uvicorn app.main:app --reload
```
`main.py`會呼叫`etl.loader.init_db()`自動將/data/*.json的內容轉換建立資料表，啟動成功會看到類似以下資訊：
```
資料庫有資料，已初始化完成
2025-05-20 17:05:38,244 INFO sqlalchemy.engine.Engine ROLLBACK
INFO:     Application startup complete.
INFO:     127.0.0.1:62030 - "GET /docs HTTP/1.1" 200 OK
```
可至瀏覽器輸入URL (http://127.0.0.1:8000) ，會看到頁面顯示：
```
{"message":"API is up and running!"}
```

最後，FastAPI 內建提供了 Swagger UI 位於 (http://127.0.0.1:8000/docs) ，會根據寫的程式（路由、參數、Schema）自動產生 API 測試介面。


### A.4. Project Path Structure

專案根目錄`/phantom_mask`內的檔案結構：
```bash
.
├── .gitignore                           # Git忽略清單，排除 .env, .DS_Store, *.pyc 等敏感或暫存檔案
├── README.md
├── app
│   ├── api                              # API router 各功能實現
│   │   ├── pharmacies_mask_filter.py
│   │   ├── pharmacies_mask_sort.py
│   │   ├── pharmacies_open.py
│   │   ├── purchase.py
│   │   ├── relevance_search.py
│   │   ├── sales_summary.py
│   │   └── users_transaction_top.py
│   ├── db
│   │   ├── database.py                 # 設定 SQLAlchemy 資料庫連線與 Session
│   │   └── models.py                   # 定義資料表結構（Pharmacy、User、Mask、Purchase 等）
│   ├── etl
│   │   └── loader.py                   # 載入 JSON 檔案並寫入資料庫的 ETL 程式
│   ├── func
│   │   └── is_open.py                  # 判斷藥局是否在特定時間營業的功能，處理`openingHours`欄位的各種格式
│   ├── main.py                         # 建立應用實例、引入router、啟動服務
│   └── schemas                         # Pydantic 資料驗證 Schema，資料模型請求/回應格式定義
│       ├── mask.py
│       ├── pharmacy.py
│       ├── purchase.py
│       └── user.py
├── data
│   ├── pharmacies.json
│   └── users.json
├── docker-compose.yml                  # 定義資料庫容器，用於一鍵啟動服務
├── init.sql                            # 初始 SQL 指令，可用於建立資料表或預設資料
├── requirements.txt                    # Python 相依套件清單，供 pip 安裝使用
└── response.md

8 directories, 24 files
```



## B. Bonus Information

### B.1. Dockerized
我使用 docker-compose.yml 完成資料庫端的容器化設定，確保在不同環境下都能與DB一致部署與測試。[docker-compose.yml](docker-compose.yml).

```bash
$ docker-compose up -d

# go inside the container
$ docker exec -it phantom_mask-db-1 bash
$ psql -h 127.0.0.1 -U steven -d phantom_mask
$ \dt
```
若已執行過`main.py`，能看到初始化的資料表：
```bash
$ \dt

              List of relations
 Schema |       Name        | Type  | Owner
--------+-------------------+-------+--------
 public | masks             | table | steven
 public | pharmacies        | table | steven
 public | purchaseHistories | table | steven
 public | users             | table | steven
(4 rows)
```

### B.3. Demo Site Url
我另外將網頁後端APIs服務部署在**Render**上，並連接其提供的PostgreSQL雲端資料庫。

若您無法成功在本機運行此專案，可點擊網址 [[Render](https://phantom-mask-h7k4.onrender.com)]

The **FastAPI Swagger UI** demo site is ready on (https://phantom-mask-h7k4.onrender.com/docs#/); you can try any APIs on this demo site.

- --
