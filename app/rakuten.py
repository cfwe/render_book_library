import os
import httpx

RAKUTEN_BOOKS_API_URL = "https://app.rakuten.co.jp/services/api/BooksBook/Search/20170404"
RAKUTEN_APP_ID = os.getenv("RAKUTEN_APP_ID")

async def get_book_market_price_from_rakuten(isbn: str) -> int | None:
    """
    楽天ブックス書籍検索APIを叩いて、ISBNコードから書籍の価格を取得する。
    価格はitemPrice（税込み書籍価格）を取得する。
    """
    if not RAKUTEN_APP_ID:
        print("Warning: RAKUTEN_APP_ID is not set. Skipping market price fetch.")
        return None

    params = {
        "format": "json",
        "isbn": isbn,
        "applicationId": RAKUTEN_APP_ID,
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(RAKUTEN_BOOKS_API_URL, params=params)
        response.raise_for_status()
        data = response.json()

        if data["count"] > 0 and "Items" in data and data["Items"]:
            return data["Items"][0]["Item"]["itemPrice"]
        return None
    
    
    # 9784053049032, 550, 1320
    # 4910066630553, 440, 1320
    # 9784789846691, 3960, 3960
    # 9784274233159, 4070, 6160
    # 9784501117207, 3135, 3740
    # 9784488025694, 1375, 1870
    # 9784103330639, 550, 2090