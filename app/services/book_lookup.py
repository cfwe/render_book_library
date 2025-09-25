import httpx
from typing import Optional, Dict, Any
import xml.etree.ElementTree as ET

OPENBD_API_URL = "https://api.openbd.jp/v1/get"
NDL_API_URL = "http://iss.ndl.go.jp/api/opensearch"


def _parse_openbd_response(book_data: Dict[str, Any]) -> Dict[str, Any]:
    """Parses the complex openBD JSON response into a flat dictionary."""
    summary = book_data.get("summary", {})
    onix = book_data.get("onix", {})
    descriptive_detail = onix.get("DescriptiveDetail", {})
    title_detail = descriptive_detail.get("TitleDetail", {}).get("TitleElement", {})

    # 著者名は配列の場合があるので、最初の要素を取得
    authors = summary.get("author", "").split(" ")
    author = authors[0] if authors else ""

    return {
        "isbn": summary.get("isbn"),
        "title": summary.get("title"),
        "author": author,
        "publisher": summary.get("publisher"),
        "page_count": onix.get("DescriptiveDetail", {}).get("Extent", [{}])[0].get("ExtentValue"),
        "size": onix.get("DescriptiveDetail", {}).get("ProductFormDetail"),
    }


def _parse_ndl_response(xml_string: str, isbn: str) -> Optional[Dict[str, Any]]:
    """Parses the NDL OpenSearch XML response into a flat dictionary."""
    try:
        root = ET.fromstring(xml_string)
        # XML Namespace
        ns = {
            'dc': 'http://purl.org/dc/elements/1.1/',
        }
        item = root.find('channel/item')
        if item is None:
            return None

        return {
            "isbn": isbn,
            "title": item.findtext('title'),
            "author": item.findtext('author'),
            "publisher": item.findtext('dc:publisher', namespaces=ns),
            "page_count": None, # NDL API does not provide page_count easily
            "size": None, # NDL API does not provide size easily
        }
    except ET.ParseError:
        return None


async def lookup_book_info_by_isbn(isbn: str) -> Optional[Dict[str, Any]]:
    """
    Fetches book information first from openBD, then falls back to NDL API.
    """
    async with httpx.AsyncClient() as client:
        # 1. Try openBD first
        response = await client.get(OPENBD_API_URL, params={"isbn": isbn})
        if response.status_code == 200:
            data = response.json()
            if data and data[0] is not None:
                return _parse_openbd_response(data[0])

        # 2. Fallback to NDL if openBD fails or returns null
        response = await client.get(NDL_API_URL, params={"isbn": isbn})
        if response.status_code == 200:
            return _parse_ndl_response(response.text, isbn)

    return None
