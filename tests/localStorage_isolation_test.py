"""
localStorage 격리 문제 입증 테스트
SuperClaude 아키텍처 분석
"""

import asyncio
from playwright.async_api import async_playwright
from datetime import datetime


class LocalStorageIsolationTest:
    """localStorage 격리 문제 테스트"""
    
    def __init__(self):
        self.test_url = "http://localhost:8001"
        self.results = {}
    
    async def test_browser_isolation(self):
        """브라우저간 localStorage 격리 테스트"""
        print("🔍 SuperClaude localStorage 격리 문제 분석")
        print("="*60)
        
        async with async_playwright() as p:
            # 여러 브라우저 컨텍스트 생성
            browsers = {
                'chrome_user1': await p.chromium.launch(headless=False),
                'chrome_user2': await p.chromium.launch(headless=False),
                'firefox_user': await p.firefox.launch(headless=False)
            }
            
            try:
                # 각 브라우저에서 테스트
                for browser_name, browser in browsers.items():
                    print(f"\n🌐 {browser_name} 테스트...")
                    await self.test_single_browser(browser, browser_name)
                
                # 결과 분석
                self.analyze_isolation_results()
                
            finally:
                for browser in browsers.values():
                    await browser.close()
    
    async def test_single_browser(self, browser, browser_name):
        """단일 브라우저 테스트"""
        context = await browser.new_context()
        page = await context.new_page()
        
        try:
            # 페이지 로드
            await page.goto(self.test_url)
            await page.wait_for_load_state('networkidle')
            await asyncio.sleep(2)
            
            # 초기 참가자 수 확인
            initial_count = await page.locator('#participantCount').text_content()
            print(f"   📊 초기 참가자 수: {initial_count}")
            
            # 참가자 등록
            test_name = f"{browser_name}_참가자_{datetime.now().strftime('%H%M%S')}"
            await page.fill('#participantName', test_name)
            await page.click('#joinBtn')
            
            # 등록 후 대기
            await asyncio.sleep(3)
            
            # 최종 참가자 수 확인
            final_count = await page.locator('#participantCount').text_content()
            
            # localStorage 데이터 확인
            storage_data = await page.evaluate("""
                () => {
                    const data = localStorage.getItem('saturday-run-participants');
                    return data ? JSON.parse(data) : [];
                }
            """)
            
            self.results[browser_name] = {
                'initial_count': int(initial_count),
                'final_count': int(final_count),
                'storage_participants': len(storage_data),
                'test_name': test_name,
                'participants': storage_data
            }
            
            print(f"   ✅ 등록 완료: {test_name}")
            print(f"   📈 참가자 수 변화: {initial_count} → {final_count}")
            print(f"   💾 localStorage 참가자: {len(storage_data)}명")
            
        finally:
            await context.close()
    
    def analyze_isolation_results(self):
        """격리 결과 분석"""
        print("\n" + "="*60)
        print("📊 SuperClaude 격리 문제 분석 결과")
        print("="*60)
        
        total_registered = sum(r['storage_participants'] for r in self.results.values())
        
        print(f"🔢 전체 등록된 참가자 수: {total_registered}명")
        print(f"🌐 테스트한 브라우저 수: {len(self.results)}개")
        
        print("\n📋 브라우저별 결과:")
        for browser, result in self.results.items():
            print(f"   {browser}:")
            print(f"     - 보이는 참가자 수: {result['final_count']}명")
            print(f"     - 실제 저장된 수: {result['storage_participants']}명")
            print(f"     - 등록한 참가자: {result['test_name']}")
        
        # 문제점 진단
        print("\n🚨 발견된 문제점:")
        
        if len(set(r['final_count'] for r in self.results.values())) > 1:
            print("   ❌ 브라우저마다 다른 참가자 수를 보여줌")
            print("   ❌ localStorage 격리로 인한 데이터 분리")
            print("   ❌ 실제 커뮤니티 기능 작동하지 않음")
        
        if all(r['final_count'] == r['storage_participants'] for r in self.results.values()):
            print("   ❌ 각 브라우저는 자신이 등록한 참가자만 봄")
            print("   ❌ 다른 사용자의 참가를 전혀 알 수 없음")
        
        print("\n💡 SuperClaude 해결책 필요:")
        print("   1. 공유 데이터베이스 구축")
        print("   2. 실시간 동기화 시스템")
        print("   3. 진정한 커뮤니티 기능 구현")


async def main():
    """메인 테스트 실행"""
    tester = LocalStorageIsolationTest()
    await tester.test_browser_isolation()


if __name__ == "__main__":
    asyncio.run(main())


