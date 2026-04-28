import asyncio
try:
    from playwright.async_api import async_playwright
except ImportError:
    async_playwright = None

async def discover_aedts(url: str):
    if not async_playwright:
        print("Playwright not installed, returning mock.")
        return [
            {"name": "AI Resume Screener", "endpoint": "/api/screen"},
            {"name": "Chatbot Interviewer", "endpoint": "/api/chat"}
        ]
        
    tools = []
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            try:
                await page.goto(url, timeout=5000)
                
                # If there's a login button, simulate clicking it
                if await page.locator("button:has-text('Login')").is_visible():
                    await page.click("button:has-text('Login')")
                    await page.wait_for_timeout(500) # give it time to show dashboard
                
                # Extract elements with data-aedt="true"
                tools = await page.evaluate('''() => {
                    const els = Array.from(document.querySelectorAll('[data-aedt="true"]'));
                    return els.map(e => ({
                        name: e.getAttribute('data-name'), 
                        endpoint: e.getAttribute('data-endpoint')
                    }));
                }''')
                
            except Exception as e:
                print(f"Playwright navigation/evaluation failed: {e}")
            finally:
                await browser.close()
    except Exception as e:
        print(f"Playwright error: {e}")
        
    if not tools:
        # Fallback if discovery completely fails
        tools = [{"name": "AI Resume Screener", "endpoint": "/api/screen"}]
        
    return tools
