import httpx
from typing import List, Dict, Any

class TrendResearch:
    @staticmethod
    def get_hacker_news_top(limit: int = 10) -> List[Dict[str, Any]]:
        results = []
        try:
            with httpx.Client(timeout=6.0) as client:
                res = client.get("https://hacker-news.firebaseio.com/v0/topstories.json")
                if res.status_code == 200:
                    story_ids = res.json()[:limit]
                    for sid in story_ids:
                        s_res = client.get(f"https://hacker-news.firebaseio.com/v0/item/{sid}.json")
                        if s_res.status_code == 200:
                            data = s_res.json()
                            if data and "title" in data:
                                results.append({
                                    "title": data.get("title"),
                                    "url": data.get("url", ""),
                                    "score": data.get("score", 0),
                                    "comments": data.get("descendants", 0)
                                })
        except Exception as e:
            print(f"HN fetch error: {e}")
        return results

    @staticmethod
    def get_arxiv_recent(query: str = "artificial intelligence", max_results: int = 5) -> List[Dict[str, Any]]:
        results = []
        try:
            url = f"http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results={max_results}"
            with httpx.Client(timeout=8.0) as client:
                res = client.get(url)
                if res.status_code == 200:
                    # Basic XML extract
                    import xml.etree.ElementTree as ET
                    root = ET.fromstring(res.text)
                    for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
                        title = entry.find("{http://www.w3.org/2005/Atom}title")
                        summary = entry.find("{http://www.w3.org/2005/Atom}summary")
                        results.append({
                            "title": title.text.strip().replace("\n", " ") if title is not None else "",
                            "summary": summary.text.strip()[:200] if summary is not None else ""
                        })
        except Exception as e:
            print(f"Arxiv fetch error: {e}")
        return results
