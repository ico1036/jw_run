"""
SuperClaude + Playwright MCP를 활용한 "I'm In" 버튼 실제 동작 테스트
주인님의 요청에 따른 상세 디버깅 테스트
"""

import asyncio
from playwright.async_api import async_playwright
import json
from datetime import datetime
import os


class ImInButtonDebugger:
    """I'm In 버튼 상세 디버깅 클래스"""
    
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.test_results = {}
        self.screenshots_dir = "tests/debug_screenshots"
        os.makedirs(self.screenshots_dir, exist_ok=True)
    
    async def take_screenshot(self, page, name):
        """스크린샷 촬영"""
        timestamp = datetime.now().strftime("%H%M%S")
        filename = f"{self.screenshots_dir}/{timestamp}_{name}.png"
        await page.screenshot(path=filename, full_page=True)
        print(f"📸 스크린샷 저장: {filename}")
        return filename
    
    async def test_page_loading(self, page):
        """페이지 로딩 상태 확인"""
        print("🔍 1단계: 페이지 로딩 테스트")
        
        try:
            # 페이지 로드
            response = await page.goto(self.base_url)
            print(f"   📄 HTTP 상태: {response.status}")
            
            # 페이지 제목 확인
            title = await page.title()
            print(f"   📝 페이지 제목: {title}")
            
            # 스크린샷 촬영
            await self.take_screenshot(page, "01_page_loaded")
            
            self.test_results['page_loading'] = {
                'status': response.status,
                'title': title,
                'success': response.status == 200
            }
            
            print("   ✅ 페이지 로딩 완료")
            return True
            
        except Exception as e:
            print(f"   ❌ 페이지 로딩 실패: {e}")
            self.test_results['page_loading'] = {'error': str(e), 'success': False}
            return False
    
    async def test_form_elements(self, page):
        """폼 요소들 존재 및 상태 확인"""
        print("🔍 2단계: 폼 요소 확인")
        
        try:
            # 이름 입력 필드 확인
            name_input = page.locator('#participantName')
            name_input_count = await name_input.count()
            name_input_visible = await name_input.is_visible() if name_input_count > 0 else False
            
            print(f"   📝 이름 입력 필드: {name_input_count}개 발견, 표시됨: {name_input_visible}")
            
            # I'm In 버튼 확인
            join_button = page.locator('#joinBtn')
            join_button_count = await join_button.count()
            join_button_visible = await join_button.is_visible() if join_button_count > 0 else False
            join_button_enabled = await join_button.is_enabled() if join_button_count > 0 else False
            
            print(f"   🔘 I'm In 버튼: {join_button_count}개 발견, 표시됨: {join_button_visible}, 활성화: {join_button_enabled}")
            
            # 버튼 텍스트 확인
            if join_button_count > 0:
                button_text = await join_button.text_content()
                print(f"   📄 버튼 텍스트: '{button_text}'")
            
            # 폼 요소 스크린샷
            await self.take_screenshot(page, "02_form_elements")
            
            # 폼 전체 확인
            join_form = page.locator('#joinForm')
            form_count = await join_form.count()
            form_visible = await join_form.is_visible() if form_count > 0 else False
            
            print(f"   📋 폼 요소: {form_count}개 발견, 표시됨: {form_visible}")
            
            self.test_results['form_elements'] = {
                'name_input': {'count': name_input_count, 'visible': name_input_visible},
                'join_button': {'count': join_button_count, 'visible': join_button_visible, 'enabled': join_button_enabled},
                'form': {'count': form_count, 'visible': form_visible},
                'success': name_input_count > 0 and join_button_count > 0 and form_count > 0
            }
            
            print("   ✅ 폼 요소 확인 완료")
            return True
            
        except Exception as e:
            print(f"   ❌ 폼 요소 확인 실패: {e}")
            self.test_results['form_elements'] = {'error': str(e), 'success': False}
            return False
    
    async def test_javascript_console(self, page):
        """JavaScript 콘솔 에러 확인"""
        print("🔍 3단계: JavaScript 콘솔 에러 확인")
        
        console_messages = []
        errors = []
        
        # 콘솔 메시지 수집
        def handle_console(msg):
            console_messages.append({
                'type': msg.type,
                'text': msg.text,
                'location': msg.location
            })
            print(f"   🖥️ 콘솔 [{msg.type}]: {msg.text}")
        
        # 페이지 에러 수집
        def handle_page_error(error):
            errors.append(str(error))
            print(f"   ❌ 페이지 에러: {error}")
        
        page.on('console', handle_console)
        page.on('pageerror', handle_page_error)
        
        # 페이지 새로고침해서 초기 로딩 에러 확인
        await page.reload()
        await page.wait_for_load_state('networkidle')
        
        self.test_results['javascript_console'] = {
            'console_messages': console_messages,
            'errors': errors,
            'success': len(errors) == 0
        }
        
        if errors:
            print(f"   ⚠️ {len(errors)}개의 JavaScript 에러 발견")
        else:
            print("   ✅ JavaScript 에러 없음")
        
        return len(errors) == 0
    
    async def test_form_submission(self, page):
        """실제 폼 제출 테스트"""
        print("🔍 4단계: 실제 'I'm In' 버튼 클릭 테스트")
        
        try:
            # 테스트 데이터 준비
            test_name = f"테스트참가자_{datetime.now().strftime('%H%M%S')}"
            print(f"   👤 테스트 참가자명: {test_name}")
            
            # 이름 입력
            name_input = page.locator('#participantName')
            await name_input.fill(test_name)
            
            filled_value = await name_input.input_value()
            print(f"   ✏️ 입력된 값: '{filled_value}'")
            
            # 입력 후 스크린샷
            await self.take_screenshot(page, "03_name_filled")
            
            # I'm In 버튼 클릭
            join_button = page.locator('#joinBtn')
            print("   🖱️ 'I'm In' 버튼 클릭 중...")
            
            # 클릭 전 버튼 상태 재확인
            button_visible = await join_button.is_visible()
            button_enabled = await join_button.is_enabled()
            print(f"   🔍 클릭 전 버튼 상태 - 표시됨: {button_visible}, 활성화: {button_enabled}")
            
            if not button_visible or not button_enabled:
                raise Exception("버튼이 클릭 가능한 상태가 아닙니다")
            
            # 실제 클릭
            await join_button.click()
            print("   ✅ 버튼 클릭 완료")
            
            # 클릭 후 스크린샷
            await self.take_screenshot(page, "04_button_clicked")
            
            # 성공 모달 확인 (5초 대기)
            print("   ⏳ 성공 모달 대기 중...")
            try:
                success_modal = page.locator('#successModal')
                await success_modal.wait_for(state='visible', timeout=5000)
                
                modal_visible = await success_modal.is_visible()
                print(f"   🎉 성공 모달 표시됨: {modal_visible}")
                
                # 모달 내용 확인
                if modal_visible:
                    modal_text = await success_modal.text_content()
                    print(f"   📄 모달 내용: {modal_text[:100]}...")
                
                # 모달 스크린샷
                await self.take_screenshot(page, "05_success_modal")
                
                # 모달 닫기
                close_button = page.locator('.modal-btn')
                if await close_button.count() > 0:
                    await close_button.click()
                    print("   ✅ 모달 닫기 완료")
                
            except Exception as modal_error:
                print(f"   ⚠️ 모달 확인 실패: {modal_error}")
                modal_visible = False
            
            # localStorage 확인
            participants_data = await page.evaluate("""
                () => {
                    const data = localStorage.getItem('saturday-run-participants');
                    return data ? JSON.parse(data) : null;
                }
            """)
            
            print(f"   💾 localStorage 데이터: {len(participants_data) if participants_data else 0}명의 참가자")
            
            if participants_data:
                latest_participant = participants_data[-1] if participants_data else None
                if latest_participant:
                    print(f"   👤 최신 참가자: {latest_participant.get('name', 'N/A')}")
            
            # 참가자 목록 UI 확인
            participant_count = page.locator('#participantCount')
            displayed_count = await participant_count.text_content()
            print(f"   📊 화면 표시 참가자 수: {displayed_count}")
            
            # 최종 스크린샷
            await self.take_screenshot(page, "06_final_state")
            
            self.test_results['form_submission'] = {
                'test_name': test_name,
                'filled_value': filled_value,
                'button_clicked': True,
                'modal_visible': modal_visible,
                'localStorage_data': participants_data,
                'displayed_count': displayed_count,
                'success': modal_visible and participants_data is not None
            }
            
            if modal_visible and participants_data:
                print("   🎉 'I'm In' 버튼 정상 작동 확인!")
                return True
            else:
                print("   ⚠️ 일부 기능에 문제가 있을 수 있습니다")
                return False
                
        except Exception as e:
            print(f"   ❌ 폼 제출 테스트 실패: {e}")
            await self.take_screenshot(page, "error_form_submission")
            self.test_results['form_submission'] = {'error': str(e), 'success': False}
            return False
    
    async def test_admin_mode_interference(self, page):
        """관리자 모드가 일반 기능에 영향을 주는지 확인"""
        print("🔍 5단계: 관리자 모드 간섭 확인")
        
        try:
            # 관리자 모드로 접속
            admin_url = f"{self.base_url}?admin=runclub2024"
            await page.goto(admin_url)
            
            # 관리자 패널이 표시되는지 확인
            admin_controls = page.locator('#adminControls')
            admin_visible = await admin_controls.is_visible()
            print(f"   🔧 관리자 패널 표시됨: {admin_visible}")
            
            # 일반 폼이 여전히 작동하는지 확인
            name_input = page.locator('#participantName')
            join_button = page.locator('#joinBtn')
            
            input_visible = await name_input.is_visible()
            button_visible = await join_button.is_visible()
            
            print(f"   📝 관리자 모드에서 일반 폼 표시됨: 입력필드={input_visible}, 버튼={button_visible}")
            
            # 관리자 모드 스크린샷
            await self.take_screenshot(page, "07_admin_mode")
            
            self.test_results['admin_mode_test'] = {
                'admin_panel_visible': admin_visible,
                'form_still_visible': input_visible and button_visible,
                'success': admin_visible and input_visible and button_visible
            }
            
            print("   ✅ 관리자 모드 간섭 확인 완료")
            return True
            
        except Exception as e:
            print(f"   ❌ 관리자 모드 테스트 실패: {e}")
            self.test_results['admin_mode_test'] = {'error': str(e), 'success': False}
            return False
    
    async def run_comprehensive_test(self):
        """종합 테스트 실행"""
        print("🚀 SuperClaude + Playwright MCP 'I'm In' 버튼 종합 테스트 시작")
        print("=" * 70)
        
        async with async_playwright() as p:
            # 브라우저 시작 (headless=False로 실제 확인 가능)
            browser = await p.chromium.launch(headless=False, slow_mo=1000)
            context = await browser.new_context(
                viewport={'width': 1920, 'height': 1080}
            )
            page = await context.new_page()
            
            try:
                # 각 테스트 단계 실행
                await self.test_page_loading(page)
                await asyncio.sleep(1)
                
                await self.test_javascript_console(page)
                await asyncio.sleep(1)
                
                await self.test_form_elements(page)
                await asyncio.sleep(1)
                
                await self.test_form_submission(page)
                await asyncio.sleep(2)
                
                await self.test_admin_mode_interference(page)
                await asyncio.sleep(1)
                
                # 결과 분석
                self.analyze_results()
                
            finally:
                await browser.close()
        
        print("=" * 70)
        print("🎉 종합 테스트 완료!")
    
    def analyze_results(self):
        """테스트 결과 분석 및 리포트"""
        print("\n" + "=" * 70)
        print("📊 SuperClaude 테스트 결과 분석")
        print("=" * 70)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results.values() if result.get('success', False))
        
        print(f"전체 테스트: {total_tests}개")
        print(f"통과: {passed_tests}개")
        print(f"실패: {total_tests - passed_tests}개")
        print(f"성공률: {(passed_tests/total_tests*100):.1f}%")
        
        print("\n📋 상세 결과:")
        for test_name, result in self.test_results.items():
            status = "✅ 통과" if result.get('success', False) else "❌ 실패"
            print(f"  {test_name}: {status}")
            
            if not result.get('success', False) and 'error' in result:
                print(f"    오류: {result['error']}")
        
        # 핵심 기능 확인
        form_submission_success = self.test_results.get('form_submission', {}).get('success', False)
        
        if form_submission_success:
            print("\n🎉 결론: 'I'm In' 버튼이 정상적으로 작동합니다!")
        else:
            print("\n⚠️ 결론: 'I'm In' 버튼에 문제가 있습니다.")
            self.suggest_fixes()
    
    def suggest_fixes(self):
        """문제 해결 제안"""
        print("\n🔧 SuperClaude 문제 해결 제안:")
        
        # JavaScript 에러가 있는 경우
        js_result = self.test_results.get('javascript_console', {})
        if js_result.get('errors'):
            print("  1. JavaScript 에러 수정 필요:")
            for error in js_result['errors']:
                print(f"     - {error}")
        
        # 폼 요소 문제
        form_result = self.test_results.get('form_elements', {})
        if not form_result.get('success', False):
            print("  2. 폼 요소 확인 필요:")
            print("     - HTML ID가 올바른지 확인 (#participantName, #joinBtn)")
            print("     - CSS가 요소를 가리고 있지 않은지 확인")
        
        # 폼 제출 문제
        submission_result = self.test_results.get('form_submission', {})
        if not submission_result.get('success', False):
            print("  3. 폼 제출 로직 확인 필요:")
            print("     - JavaScript 이벤트 리스너 연결 확인")
            print("     - localStorage 저장 로직 확인")
            print("     - 성공 모달 표시 로직 확인")


async def main():
    """메인 실행 함수"""
    debugger = ImInButtonDebugger()
    await debugger.run_comprehensive_test()


if __name__ == "__main__":
    asyncio.run(main())
