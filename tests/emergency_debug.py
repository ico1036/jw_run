"""
긴급 디버깅: 실제 에러 상황 재현 및 분석
SuperClaude + Playwright MCP 총동원
"""

import asyncio
from playwright.async_api import async_playwright
import json
from datetime import datetime


class EmergencyDebugger:
    """긴급 상황 디버거"""
    
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.errors_captured = []
        self.console_logs = []
        self.network_failures = []
    
    async def capture_real_error(self):
        """실제 에러 상황 캡처"""
        print("🚨 긴급 디버깅 시작 - 실제 에러 상황 재현")
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False, slow_mo=500)
            context = await browser.new_context()
            page = await context.new_page()
            
            # 에러 캡처 설정
            page.on('console', lambda msg: self.console_logs.append({
                'type': msg.type,
                'text': msg.text,
                'timestamp': datetime.now().isoformat()
            }))
            
            page.on('pageerror', lambda error: self.errors_captured.append({
                'error': str(error),
                'timestamp': datetime.now().isoformat()
            }))
            
            page.on('requestfailed', lambda request: self.network_failures.append({
                'url': request.url,
                'failure': request.failure,
                'timestamp': datetime.now().isoformat()
            }))
            
            try:
                # 페이지 로드
                print("📄 페이지 로딩...")
                await page.goto(self.base_url)
                await page.wait_for_load_state('networkidle')
                
                # 스크린샷
                await page.screenshot(path='tests/debug_screenshots/emergency_01_loaded.png')
                
                # 폼 입력
                print("✏️ 테스트 데이터 입력...")
                test_name = f"긴급테스트_{datetime.now().strftime('%H%M%S')}"
                await page.fill('#participantName', test_name)
                
                # 입력 후 스크린샷
                await page.screenshot(path='tests/debug_screenshots/emergency_02_filled.png')
                
                # 버튼 클릭 전 JavaScript 상태 확인
                js_state = await page.evaluate("""
                    () => {
                        const app = window.app || {};
                        return {
                            appExists: !!window.app,
                            configOwner: app.config ? app.config.owner : 'undefined',
                            participantsLength: app.participants ? app.participants.length : 'undefined'
                        };
                    }
                """)
                print(f"🔍 JavaScript 상태: {js_state}")
                
                # 실제 버튼 클릭
                print("🖱️ 'I'm In' 버튼 클릭...")
                await page.click('#joinBtn')
                
                # 클릭 후 대기
                await asyncio.sleep(3)
                
                # 에러 메시지 확인
                try:
                    # alert 대화상자 처리
                    page.on('dialog', lambda dialog: asyncio.create_task(self.handle_dialog(dialog)))
                    await asyncio.sleep(2)
                except:
                    pass
                
                # 최종 스크린샷
                await page.screenshot(path='tests/debug_screenshots/emergency_03_after_click.png')
                
                # localStorage 상태 확인
                local_storage = await page.evaluate("""
                    () => {
                        return {
                            participants: localStorage.getItem('saturday-run-participants'),
                            eventConfig: localStorage.getItem('saturday-run-event-config')
                        };
                    }
                """)
                print(f"💾 localStorage 상태: {local_storage}")
                
            finally:
                await browser.close()
        
        # 결과 분석
        self.analyze_captured_errors()
    
    async def handle_dialog(self, dialog):
        """alert 대화상자 처리"""
        print(f"🚨 Alert 감지: {dialog.message}")
        self.errors_captured.append({
            'type': 'alert',
            'message': dialog.message,
            'timestamp': datetime.now().isoformat()
        })
        await dialog.accept()
    
    def analyze_captured_errors(self):
        """캡처된 에러 분석"""
        print("\n" + "="*60)
        print("🔍 에러 분석 결과")
        print("="*60)
        
        print(f"📊 캡처된 콘솔 로그: {len(self.console_logs)}개")
        for log in self.console_logs:
            print(f"  [{log['type']}] {log['text']}")
        
        print(f"\n🚨 캡처된 에러: {len(self.errors_captured)}개")
        for error in self.errors_captured:
            print(f"  {error}")
        
        print(f"\n🌐 네트워크 실패: {len(self.network_failures)}개")
        for failure in self.network_failures:
            print(f"  {failure['url']}: {failure['failure']}")
        
        # 근본 원인 진단
        self.diagnose_root_cause()
    
    def diagnose_root_cause(self):
        """근본 원인 진단"""
        print("\n🎯 SuperClaude 근본 원인 진단:")
        
        # alert 메시지 확인
        alert_errors = [e for e in self.errors_captured if e.get('type') == 'alert']
        if alert_errors:
            for alert in alert_errors:
                if 'error submitting your registration' in alert.get('message', ''):
                    print("  ✅ 확인: 등록 에러 메시지 발생")
                    print("  🔍 원인: submitParticipation 메서드에서 예외 발생")
        
        # 네트워크 에러 확인
        github_api_failures = [f for f in self.network_failures if 'api.github.com' in f['url']]
        if github_api_failures:
            print("  ✅ 확인: GitHub API 호출 실패")
            print("  🔍 원인: GitHub API 설정 문제")
        
        # 콘솔 에러 확인
        js_errors = [l for l in self.console_logs if l['type'] == 'error']
        if js_errors:
            print("  ✅ 확인: JavaScript 에러 발생")
            for error in js_errors:
                print(f"    - {error['text']}")


async def main():
    debugger = EmergencyDebugger()
    await debugger.capture_real_error()


if __name__ == "__main__":
    asyncio.run(main())


