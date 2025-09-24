"""
GitHub Pages 수정 후 최종 테스트
SuperClaude + Playwright MCP 최종 검증
"""

import asyncio
from playwright.async_api import async_playwright
from datetime import datetime


async def final_github_test():
    """GitHub Pages 수정 후 최종 테스트"""
    print("🚀 GitHub Pages 수정 후 최종 검증")
    print("="*50)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=1000)
        context = await browser.new_context()
        page = await context.new_page()
        
        console_logs = []
        errors = []
        
        # 이벤트 리스너
        page.on('console', lambda msg: console_logs.append(f"[{msg.type}] {msg.text}"))
        page.on('pageerror', lambda error: errors.append(str(error)))
        
        try:
            print("1️⃣ GitHub Pages 접속...")
            await page.goto("https://ico1036.github.io/jw_run")
            await page.wait_for_load_state('networkidle')
            await asyncio.sleep(5)  # 충분한 로딩 시간
            
            # JavaScript 상태 확인
            js_state = await page.evaluate("""
                () => {
                    return {
                        appExists: !!window.app,
                        appType: typeof window.app,
                        configExists: !!(window.app && window.app.config),
                        participantsExists: !!(window.app && window.app.participants),
                        participantsCount: window.app ? window.app.participants.length : 'undefined',
                        localStorageSupported: typeof(Storage) !== "undefined"
                    };
                }
            """)
            
            print(f"2️⃣ JavaScript 상태: {js_state}")
            
            if js_state['appExists']:
                print("   ✅ app 객체 정상 생성됨!")
                
                # 참가자 등록 테스트
                print("3️⃣ 참가자 등록 테스트...")
                test_name = f"GitHub테스트_{datetime.now().strftime('%H%M%S')}"
                
                await page.fill('#participantName', test_name)
                await page.click('#joinBtn')
                
                # 결과 확인
                await asyncio.sleep(3)
                
                # 성공 모달 확인
                try:
                    modal_visible = await page.locator('#successModal.show').is_visible()
                    print(f"   🎉 성공 모달: {modal_visible}")
                except:
                    modal_visible = False
                
                # localStorage 확인
                stored_data = await page.evaluate("""
                    () => {
                        const data = localStorage.getItem('saturday-run-participants');
                        return data ? JSON.parse(data) : [];
                    }
                """)
                
                # 참가자 수 확인
                participant_count = await page.locator('#participantCount').text_content()
                
                print(f"   💾 저장된 참가자: {len(stored_data)}명")
                print(f"   📊 화면 표시: {participant_count}명")
                
                # 최종 판정
                if len(stored_data) > 0 and int(participant_count) > 0:
                    print("\n🎉 성공! GitHub Pages에서 완벽하게 작동합니다!")
                    print(f"✅ 테스트 참가자 '{test_name}' 등록 완료")
                    return True
                else:
                    print("\n❌ 여전히 문제가 있습니다.")
                    return False
            else:
                print("   ❌ app 객체가 생성되지 않음")
                return False
                
        except Exception as e:
            print(f"❌ 테스트 실패: {e}")
            return False
        
        finally:
            if console_logs:
                print("\n🖥️ 콘솔 로그:")
                for log in console_logs[-5:]:  # 최근 5개만
                    print(f"  {log}")
            
            if errors:
                print("\n🚨 에러:")
                for error in errors:
                    print(f"  {error}")
            
            await browser.close()


async def main():
    success = await final_github_test()
    
    if success:
        print("\n" + "="*50)
        print("🎉 GitHub Pages 문제 완전 해결!")
        print("✅ https://ico1036.github.io/jw_run 정상 작동")
        print("✅ 참가자 등록 기능 완벽 작동")
        print("="*50)
    else:
        print("\n" + "="*50)
        print("⚠️ GitHub Pages 문제 지속")
        print("💡 Vercel 배포를 권장합니다")
        print("="*50)


if __name__ == "__main__":
    asyncio.run(main())


