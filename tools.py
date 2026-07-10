from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os
from dotenv import load_dotenv
from rich import print
load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query : str) -> str:
    """Search the web for recent and reliable infomation on a topic. Returns Titles, URLs and snippets""" # doc string
    result = tavily.search(query = query,max_results = 5)

    out = []
    for r in result['result']:
        out.append(f"Title : {r['title']}\n URL : {r['url']}\n Snippet : {r['content'][:300]}\n")
    return "\n-----\n".join(out)

@tool
def scrape_url(url : str) -> str:
    """Scrape and return the text content from a given URL for deeper reading."""
    try:
        response = requests.get(url,timeout=8,headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.text, 'html.parser')
        for tag in soup(['script', 'style', 'footer', 'nav',]):
            tag.decompose()
        return soup.get_text(separator='\n', strip=True)[:3000]  # Limit to first 3000 characters
    except Exception as e:
        return f"Could not scrape URL: {str(e)}"
    print(scrape_url("https://www.nature.com/articles/s41586-020-2649-2"))