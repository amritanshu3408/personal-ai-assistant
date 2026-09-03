from typing import Optional
from app.core.tools.base import BaseTool, ToolResult
from app.utils.logger import logger

try:
    from playwright.async_api import async_playwright
    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False


class BrowserOpenUrlTool(BaseTool):
    name = "browser_open_url"
    description = "Open a URL in a headless browser and return page title + text content (truncated)."
    parameters = {
        "type": "object",
        "properties": {
            "url": {"type": "string", "description": "Full URL to open"},
            "wait_ms": {"type": "integer", "default": 2000},
        },
        "required": ["url"],
    }

    async def execute(self, url: str, wait_ms: int = 2000) -> ToolResult:
        if not HAS_PLAYWRIGHT:
            return ToolResult(
                success=True,
                data={"url": url, "note": "Playwright not installed – open manually"},
                message=f"Would open {url}",
            )
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                await page.goto(url, wait_until="domcontentloaded", timeout=30000)
                await page.wait_for_timeout(wait_ms)
                title = await page.title()
                text = await page.inner_text("body")
                await browser.close()
                return ToolResult(
                    success=True,
                    data={"title": title, "text": text[:3000], "url": url},
                    message=f"Opened {url}",
                )
        except Exception as e:
            logger.exception("Browser tool failed")
            return ToolResult(success=False, error=str(e))


class BrowserSearchTool(BaseTool):
    name = "web_search"
    description = "Perform a simple web search (DuckDuckGo lite) and return top results text."
    parameters = {
        "type": "object",
        "properties": {
            "query": {"type": "string"},
            "max_results": {"type": "integer", "default": 5},
        },
        "required": ["query"],
    }

    async def execute(self, query: str, max_results: int = 5) -> ToolResult:
        import httpx
        from urllib.parse import quote_plus

        try:
            url = f"https://html.duckduckgo.com/html/?q={quote_plus(query)}"
            async with httpx.AsyncClient(timeout=15, follow_redirects=True) as client:
                resp = await client.get(url, headers={"User-Agent": "Mozilla/5.0"})
                resp.raise_for_status()
                text = resp.text
            from bs4 import BeautifulSoup

            soup = BeautifulSoup(text, "html.parser")
            results = []
            for a in soup.select("a.result__a")[:max_results]:
                results.append({"title": a.get_text(strip=True), "url": a.get("href")})
            return ToolResult(success=True, data=results, message=f"Search for '{query}'")
        except Exception as e:
            return ToolResult(success=False, error=str(e))


BROWSER_TOOLS = [BrowserOpenUrlTool(), BrowserSearchTool()]
