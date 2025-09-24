"""
파비콘 테스트 스크립트
Playwright로 파비콘이 제대로 로드되는지 확인
"""

import asyncio
from playwright.async_api import async_playwright
from datetime import datetime


async def test_favicon():
    """파비콘 로딩 테스트"""
    print("🎨 파비콘 테스트 시작")
    print("="*40)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=1000)
        context = await browser.new_context()
        page = await context.new_page()
        
        try:
            print("1️⃣ 로컬 서버 접속...")
            await page.goto("http://localhost:8001")
            await page.wait_for_load_state('networkidle')
            await asyncio.sleep(3)
            
            # 파비콘 요소 확인
            favicon_links = await page.evaluate("""
                () => {
                    const links = document.querySelectorAll('link[rel*="icon"]');
                    return Array.from(links).map(link => ({
                        rel: link.rel,
                        href: link.href,
                        type: link.type,
                        sizes: link.sizes?.value || 'none'
                    }));
                }
            """)
            
            print("2️⃣ 파비콘 링크 확인:")
            for link in favicon_links:
                print(f"   📎 {link['rel']}: {link['href']}")
                print(f"      타입: {link['type']}, 크기: {link['sizes']}")
            
            # 파비콘 파일 존재 확인
            print("\n3️⃣ 파비콘 파일 로딩 테스트...")
            
            favicon_urls = [
                "http://localhost:8001/images/favicon.svg",
                "http://localhost:8001/images/favicon-simple.svg",
                "http://localhost:8001/site.webmanifest"
            ]
            
            for url in favicon_urls:
                try:
                    response = await page.goto(url)
                    status = "✅" if response.status == 200 else "❌"
                    print(f"   {status} {url}: {response.status}")
                except Exception as e:
                    print(f"   ❌ {url}: 에러 - {e}")
            
            # 스크린샷
            await page.goto("http://localhost:8001")
            await page.wait_for_load_state('networkidle')
            await page.screenshot(path='favicon_test.png', full_page=True)
            print("\n📸 스크린샷 저장: favicon_test.png")
            
            print("\n🎉 파비콘 테스트 완료!")
            print("💡 브라우저 탭에서 파비콘을 확인하세요!")
            
        finally:
            await browser.close()


async def main():
    await test_favicon()


if __name__ == "__main__":
    asyncio.run(main())


