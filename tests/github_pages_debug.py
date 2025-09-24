"""
GitHub Pages 실제 문제 진단
SuperClaude + Playwright MCP로 실제 원인 파악
"""

import asyncio
from playwright.async_api import async_playwright
from datetime import datetime


class GitHubPagesDebugger:
    """GitHub Pages 문제 진단기"""
    
    def __init__(self):
        self.github_url = "https://ico1036.github.io/jw_run"
        self.local_url = "http://localhost:8000"
        self.console_logs = []
        self.errors = []
        self.network_failures = []
    
    async def compare_environments(self):
        """로컬 vs GitHub Pages 환경 비교"""
        print("🔍 SuperClaude 환경 비교 분석 시작")
        print("="*60)
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False, slow_mo=1000)
            
            # 로컬 환경 테스트
            print("1️⃣ 로컬 환경 테스트...")
            local_result = await self.test_environment(browser, self.local_url, "LOCAL")
            
            # GitHub Pages 환경 테스트
            print("\n2️⃣ GitHub Pages 환경 테스트...")
            github_result = await self.test_environment(browser, self.github_url, "GITHUB")
            
            # 결과 비교
            print("\n3️⃣ 환경 비교 분석...")
            self.compare_results(local_result, github_result)
            
            await browser.close()
    
    async def test_environment(self, browser, url, env_name):
        """특정 환경에서 테스트"""
        context = await browser.new_context()
        page = await context.new_page()
        
        console_logs = []
        errors = []
        network_failures = []
        
        # 이벤트 리스너 설정
        page.on('console', lambda msg: console_logs.append({
            'type': msg.type,
            'text': msg.text,
            'timestamp': datetime.now().isoformat()
        }))
        
        page.on('pageerror', lambda error: errors.append({
            'error': str(error),
            'timestamp': datetime.now().isoformat()
        }))
        
        page.on('requestfailed', lambda request: network_failures.append({
            'url': request.url,
            'failure': request.failure,
            'timestamp': datetime.now().isoformat()
        }))
        
        result = {
            'env': env_name,
            'url': url,
            'console_logs': console_logs,
            'errors': errors,
            'network_failures': network_failures
        }
        
        try:
            print(f"   📄 {env_name} 페이지 로딩...")
            await page.goto(url)
            await page.wait_for_load_state('networkidle')
            await asyncio.sleep(3)
            
            # JavaScript 상태 확인
            js_state = await page.evaluate("""
                () => {
                    return {
                        appExists: !!window.app,
                        appType: typeof window.app,
                        configExists: !!(window.app && window.app.config),
                        participantsExists: !!(window.app && window.app.participants),
                        participantsCount: window.app ? window.app.participants.length : 'undefined',
                        localStorageSupported: typeof(Storage) !== "undefined",
                        localStorageData: localStorage.getItem('saturday-run-participants'),
                        location: window.location.href,
                        protocol: window.location.protocol
                    };
                }
            """)
            
            result['js_state'] = js_state
            print(f"   🔍 {env_name} JavaScript 상태: {js_state}")
            
            # 참가자 등록 테스트
            print(f"   👤 {env_name} 참가자 등록 테스트...")
            test_name = f"{env_name}_테스트_{datetime.now().strftime('%H%M%S')}"
            
            await page.fill('#participantName', test_name)
            await page.click('#joinBtn')
            
            # 결과 확인
            await asyncio.sleep(3)
            
            # 성공 모달 확인
            try:
                modal_visible = await page.locator('#successModal.show').is_visible()
                result['modal_shown'] = modal_visible
                print(f"   🎉 {env_name} 성공 모달: {modal_visible}")
            except:
                result['modal_shown'] = False
            
            # localStorage 확인
            final_storage = await page.evaluate("""
                () => {
                    const data = localStorage.getItem('saturday-run-participants');
                    return data ? JSON.parse(data) : [];
                }
            """)
            
            result['final_storage'] = final_storage
            result['storage_count'] = len(final_storage) if final_storage else 0
            print(f"   💾 {env_name} 최종 저장된 참가자: {result['storage_count']}명")
            
            # 스크린샷
            await page.screenshot(path=f'tests/debug_screenshots/{env_name.lower()}_test.png')
            
        except Exception as e:
            print(f"   ❌ {env_name} 테스트 실패: {e}")
            result['test_error'] = str(e)
        
        finally:
            await context.close()
        
        return result
    
    def compare_results(self, local_result, github_result):
        """결과 비교 분석"""
        print("📊 SuperClaude 비교 분석 결과:")
        print("-" * 60)
        
        # JavaScript 상태 비교
        local_js = local_result.get('js_state', {})
        github_js = github_result.get('js_state', {})
        
        print("🔍 JavaScript 상태 비교:")
        for key in ['appExists', 'configExists', 'participantsExists', 'localStorageSupported']:
            local_val = local_js.get(key, 'N/A')
            github_val = github_js.get(key, 'N/A')
            status = "✅" if local_val == github_val else "❌"
            print(f"   {key}: LOCAL={local_val}, GITHUB={github_val} {status}")
        
        # 저장 결과 비교
        local_count = local_result.get('storage_count', 0)
        github_count = github_result.get('storage_count', 0)
        
        print(f"\n💾 저장 결과 비교:")
        print(f"   LOCAL: {local_count}명 저장")
        print(f"   GITHUB: {github_count}명 저장")
        
        if local_count > 0 and github_count == 0:
            print("   🚨 GitHub Pages에서 localStorage 저장 실패!")
        elif local_count == github_count:
            print("   ✅ 두 환경 모두 정상 작동")
        
        # 에러 비교
        local_errors = local_result.get('errors', [])
        github_errors = github_result.get('errors', [])
        
        if github_errors and not local_errors:
            print(f"\n🚨 GitHub Pages 전용 에러 발견:")
            for error in github_errors:
                print(f"   - {error['error']}")
        
        # 콘솔 로그 비교
        github_logs = github_result.get('console_logs', [])
        error_logs = [log for log in github_logs if log['type'] == 'error']
        
        if error_logs:
            print(f"\n🚨 GitHub Pages 콘솔 에러:")
            for log in error_logs:
                print(f"   - {log['text']}")
        
        # 최종 진단
        self.final_diagnosis(local_result, github_result)
    
    def final_diagnosis(self, local_result, github_result):
        """최종 진단 및 해결책 제시"""
        print("\n" + "="*60)
        print("🎯 SuperClaude 최종 진단")
        print("="*60)
        
        local_works = local_result.get('storage_count', 0) > 0
        github_works = github_result.get('storage_count', 0) > 0
        
        if local_works and not github_works:
            print("❌ 문제 확인: GitHub Pages에서 기능이 작동하지 않음")
            print("\n🔍 가능한 원인:")
            print("   1. HTTPS vs HTTP 프로토콜 차이")
            print("   2. 도메인 차이로 인한 localStorage 격리")
            print("   3. GitHub Pages의 보안 정책")
            print("   4. 파일 경로 문제")
            print("   5. 캐시 문제")
            
            print("\n💡 해결책:")
            print("   1. Vercel로 배포 (권장)")
            print("   2. Netlify로 배포")
            print("   3. GitHub Pages 설정 수정")
            
        elif local_works and github_works:
            print("✅ 두 환경 모두 정상 작동")
            print("   문제가 일시적이었거나 이미 해결됨")
            
        else:
            print("⚠️ 두 환경 모두 문제 있음")
            print("   코드 자체에 문제가 있을 수 있음")


async def main():
    """메인 실행"""
    debugger = GitHubPagesDebugger()
    await debugger.compare_environments()


if __name__ == "__main__":
    asyncio.run(main())


