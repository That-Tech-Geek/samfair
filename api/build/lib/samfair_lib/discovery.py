import asyncio
try:
    from playwright.async_api import async_playwright
except ImportError:
    async_playwright = None

async def discover_aedts(url: str, creds: dict = None):
    # Mocking if playwright is not installed properly or running headless in restricted env
    if not async_playwright:
        return [
            {"name": "mock-ai-screen", "endpoint": "http://localhost:8000/mock/predict"},
            {"name": "legacy-rule-engine", "endpoint": "http://localhost:8000/mock/predict-legacy"}
        ]
        
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            # Simple fallback to a dummy list if URL is unreachable or just for hackathon speed
            try:
                await page.goto(url, timeout=5000)
                # Extract elements with data-aedt attribute
                tools = await page.evaluate('''() => {
                    const els = Array.from(document.querySelectorAll('[data-aedt]'));
                    return els.map(e => ({
                        name: e.dataset.aedt, 
                        endpoint: e.dataset.endpoint
                    }));
                }''')
                await browser.close()
                if tools:
                    return tools
            except Exception as e:
                print(f"Playwright navigation failed, using mock data. Error: {e}")
            
            await browser.close()
    except Exception as e:
        pass
        
    return [
        {"name": "AI Screen (Resumes)", "endpoint": "http://localhost:8000/mock/predict"}
    ]
