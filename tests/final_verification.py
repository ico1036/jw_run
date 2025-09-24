"""
최종 검증 테스트 - 수정 후 완전한 동작 확인
SuperClaude + Playwright MCP 최종 검증
"""

import asyncio
from playwright.async_api import async_playwright
import json
from datetime import datetime


class FinalVerificationTest:
    """최종 검증 테스트"""
    
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.test_results = {}
        self.success_count = 0
        self.total_tests = 0
    
    async def test_complete_user_journey(self):
        """완전한 사용자 여정 테스트"""
        print("🚀 최종 검증 테스트 시작 - 완전한 사용자 여정")
        print("="*60)
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False, slow_mo=1000)
            context = await browser.new_context()
            page = await context.new_page()
            
            # 콘솔 로그 수집
            console_logs = []
            page.on('console', lambda msg: console_logs.append(f"[{msg.type}] {msg.text}"))
            
            # 에러 수집
            errors = []
            page.on('pageerror', lambda error: errors.append(str(error)))
            
            try:
                # 1. 페이지 로드 테스트
                await self.test_page_load(page)
                
                # 2. JavaScript 초기화 확인
                await self.test_js_initialization(page)
                
                # 3. 폼 요소 확인
                await self.test_form_elements(page)
                
                # 4. 실제 참가자 등록 (여러 명)
                await self.test_multiple_registrations(page)
                
                # 5. 데이터 지속성 확인
                await self.test_data_persistence(page)
                
                # 6. 관리자 모드 확인
                await self.test_admin_mode(page)
                
                # 결과 출력
                print(f"\n📊 최종 결과: {self.success_count}/{self.total_tests} 테스트 통과")
                
                if console_logs:
                    print("\n🖥️ 콘솔 로그:")
                    for log in console_logs[-10:]:  # 최근 10개만
                        print(f"  {log}")
                
                if errors:
                    print("\n🚨 JavaScript 에러:")
                    for error in errors:
                        print(f"  {error}")
                
                # 최종 판정
                success_rate = (self.success_count / self.total_tests) * 100
                if success_rate >= 90:
                    print(f"\n🎉 성공! {success_rate:.1f}% 테스트 통과 - 문제 해결됨!")
                    return True
                else:
                    print(f"\n⚠️ 주의: {success_rate:.1f}% 테스트 통과 - 추가 수정 필요")
                    return False
                    
            finally:
                await browser.close()
    
    async def test_page_load(self, page):
        """페이지 로드 테스트"""
        self.total_tests += 1
        print("1️⃣ 페이지 로드 테스트...")
        
        try:
            response = await page.goto(self.base_url)
            assert response.status == 200
            
            title = await page.title()
            assert "Saturday Run & Coffee Club" in title
            
            await page.screenshot(path='tests/debug_screenshots/final_01_loaded.png')
            
            self.success_count += 1
            print("   ✅ 페이지 로드 성공")
            
        except Exception as e:
            print(f"   ❌ 페이지 로드 실패: {e}")
    
    async def test_js_initialization(self, page):
        """JavaScript 초기화 확인"""
        self.total_tests += 1
        print("2️⃣ JavaScript 초기화 확인...")
        
        try:
            # 초기화 대기
            await page.wait_for_load_state('networkidle')
            await asyncio.sleep(2)
            
            # app 객체 확인
            js_state = await page.evaluate("""
                () => {
                    return {
                        appExists: !!window.app,
                        appType: typeof window.app,
                        configExists: !!(window.app && window.app.config),
                        participantsExists: !!(window.app && window.app.participants)
                    };
                }
            """)
            
            print(f"   🔍 JavaScript 상태: {js_state}")
            
            assert js_state['appExists'], "app 객체가 존재하지 않음"
            assert js_state['configExists'], "config 객체가 존재하지 않음"
            
            self.success_count += 1
            print("   ✅ JavaScript 초기화 성공")
            
        except Exception as e:
            print(f"   ❌ JavaScript 초기화 실패: {e}")
    
    async def test_form_elements(self, page):
        """폼 요소 확인"""
        self.total_tests += 1
        print("3️⃣ 폼 요소 확인...")
        
        try:
            name_input = page.locator('#participantName')
            join_button = page.locator('#joinBtn')
            
            assert await name_input.is_visible(), "이름 입력 필드가 보이지 않음"
            assert await join_button.is_visible(), "참가 버튼이 보이지 않음"
            assert await join_button.is_enabled(), "참가 버튼이 비활성화됨"
            
            self.success_count += 1
            print("   ✅ 폼 요소 확인 성공")
            
        except Exception as e:
            print(f"   ❌ 폼 요소 확인 실패: {e}")
    
    async def test_multiple_registrations(self, page):
        """여러 참가자 등록 테스트"""
        self.total_tests += 1
        print("4️⃣ 여러 참가자 등록 테스트...")
        
        try:
            test_participants = [
                f"테스트참가자1_{datetime.now().strftime('%H%M%S')}",
                f"테스트참가자2_{datetime.now().strftime('%H%M%S')}",
                f"테스트참가자3_{datetime.now().strftime('%H%M%S')}"
            ]
            
            for i, participant_name in enumerate(test_participants):
                print(f"   👤 참가자 {i+1} 등록: {participant_name}")
                
                # 이름 입력
                await page.fill('#participantName', participant_name)
                
                # 버튼 클릭
                await page.click('#joinBtn')
                
                # 성공 모달 대기
                try:
                    await page.wait_for_selector('#successModal.show', timeout=5000)
                    print(f"      ✅ 성공 모달 표시됨")
                    
                    # 모달 닫기
                    await page.click('.modal-btn')
                    await page.wait_for_selector('#successModal:not(.show)', timeout=3000)
                    
                except Exception as modal_error:
                    print(f"      ❌ 모달 에러: {modal_error}")
                    raise
                
                # 잠시 대기
                await asyncio.sleep(1)
            
            # 참가자 수 확인
            participant_count = await page.locator('#participantCount').text_content()
            print(f"   📊 최종 참가자 수: {participant_count}")
            
            # localStorage 확인
            stored_data = await page.evaluate("""
                () => {
                    const data = localStorage.getItem('saturday-run-participants');
                    return data ? JSON.parse(data) : [];
                }
            """)
            
            print(f"   💾 localStorage 참가자 수: {len(stored_data)}")
            
            assert len(stored_data) >= len(test_participants), "참가자 데이터가 제대로 저장되지 않음"
            
            await page.screenshot(path='tests/debug_screenshots/final_02_registrations.png')
            
            self.success_count += 1
            print("   🎉 여러 참가자 등록 성공!")
            
        except Exception as e:
            print(f"   ❌ 참가자 등록 실패: {e}")
            await page.screenshot(path='tests/debug_screenshots/final_error_registration.png')
    
    async def test_data_persistence(self, page):
        """데이터 지속성 확인"""
        self.total_tests += 1
        print("5️⃣ 데이터 지속성 확인...")
        
        try:
            # 페이지 새로고침
            await page.reload()
            await page.wait_for_load_state('networkidle')
            await asyncio.sleep(2)
            
            # 참가자 수가 유지되는지 확인
            participant_count = await page.locator('#participantCount').text_content()
            count_num = int(participant_count)
            
            assert count_num > 0, "페이지 새로고침 후 참가자 데이터가 사라짐"
            
            self.success_count += 1
            print(f"   ✅ 데이터 지속성 확인 성공 (참가자 {count_num}명 유지)")
            
        except Exception as e:
            print(f"   ❌ 데이터 지속성 확인 실패: {e}")
    
    async def test_admin_mode(self, page):
        """관리자 모드 확인"""
        self.total_tests += 1
        print("6️⃣ 관리자 모드 확인...")
        
        try:
            # 관리자 모드로 이동
            admin_url = f"{self.base_url}?admin=runclub2024"
            await page.goto(admin_url)
            await page.wait_for_load_state('networkidle')
            
            # 관리자 패널 확인
            admin_controls = page.locator('#adminControls')
            assert await admin_controls.is_visible(), "관리자 패널이 표시되지 않음"
            
            # 일반 폼도 여전히 작동하는지 확인
            name_input = page.locator('#participantName')
            assert await name_input.is_visible(), "관리자 모드에서 일반 폼이 보이지 않음"
            
            await page.screenshot(path='tests/debug_screenshots/final_03_admin.png')
            
            self.success_count += 1
            print("   ✅ 관리자 모드 확인 성공")
            
        except Exception as e:
            print(f"   ❌ 관리자 모드 확인 실패: {e}")


async def main():
    """최종 검증 실행"""
    tester = FinalVerificationTest()
    success = await tester.test_complete_user_journey()
    
    if success:
        print("\n" + "="*60)
        print("🎉 최종 검증 완료 - 모든 문제 해결됨!")
        print("✅ 일반 사용자가 참가자 등록을 정상적으로 할 수 있습니다!")
        print("="*60)
    else:
        print("\n" + "="*60)
        print("⚠️ 추가 수정이 필요합니다.")
        print("="*60)
    
    return success


if __name__ == "__main__":
    asyncio.run(main())


