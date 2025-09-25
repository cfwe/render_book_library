import httpx
from bs4 import BeautifulSoup
from typing import Optional, Dict
import re


async def scrape_bookoff_online_price(isbn: str) -> Optional[Dict[str, int]]:
    """
    Fetches the used book price and list price from the Book-Off Online website by scraping.

    Args:
        isbn: The ISBN code of the book.

    Returns:
        A dictionary with 'market_price' and 'list_price' if found, otherwise None.
    """
    # The API is now protected, so we scrape the HTML page instead.
    search_url = f"https://shopping.bookoff.co.jp/search/keyword/{isbn}"
    headers = {
        # A general-purpose User-Agent is less likely to be blocked.
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(search_url, headers=headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "lxml")

            # Find the main price tag.
            market_price_tag = soup.select_one("p.productItem__price") or soup.select_one("span.item-price__price")

            if not market_price_tag:
                return None

            price_text = market_price_tag.get_text(separator=" ", strip=True)
            difference = 0

            # "定価より...円" の差額を抽出
            if "定価より" in price_text:
                diff_match = re.search(r"定価より(.*)円", price_text)
                if diff_match:
                    difference = int(diff_match.group(1).replace(",", ""))

            # 中古価格を抽出
            market_price_match = re.search(r"(\d{1,3}(?:,\d{3})*|\d+)(?=\s*円)", price_text)
            if not market_price_match:
                return None

            market_price = int(market_price_match.group(1).replace(",", ""))
            # 定価を計算
            list_price = market_price + difference

            return {"market_price": market_price, "list_price": list_price}

        except (httpx.HTTPStatusError, ValueError, TypeError, AttributeError):
            return None
