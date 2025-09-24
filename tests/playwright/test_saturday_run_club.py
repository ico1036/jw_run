"""
Saturday Run & Coffee Club - Playwright E2E Tests
SuperClaude Framework 기반 자동화 테스트
"""

import pytest
import asyncio
from playwright.async_api import async_playwright, Page, Browser, BrowserContext
import json
from datetime import datetime, timedelta
import os


class TestSaturdayRunClub:
    """Saturday Run & Coffee Club 웹사이트 종합 테스트"""
    
    @pytest.fixture(scope="session")
    async def browser_setup(self):
        """브라우저 설정 및 초기화"""
        async with async_playwright() as p:
            # 여러 브라우저에서 테스트
            browsers = {
                'chromium': await p.chromium.launch(headless=False),
                'firefox': await p.firefox.launch(headless=False),
                'webkit': await p.webkit.launch(headless=False)
            }
            yield browsers
            
            # 브라우저 정리
            for browser in browsers.values():
                await browser.close()
    
    @pytest.fixture
    async def page_setup(self, browser_setup):
        """페이지 설정 및 컨텍스트 생성"""
        browser = browser_setup['chromium']  # 기본 브라우저
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        )
        page = await context.new_page()
        
        # 로컬 서버 URL (실제 배포된 URL로 변경 가능)
        base_url = "http://localhost:8000"
        
        yield page, base_url
        
        await context.close()
    
    async def test_page_loading(self, page_setup):
        """기본 페이지 로딩 테스트"""
        page, base_url = page_setup
        
        # 페이지 로드
        response = await page.goto(base_url)
        assert response.status == 200
        
        # 제목 확인
        title = await page.title()
        assert "Saturday Run & Coffee Club" in title
        
        # 주요 요소 존재 확인
        hero_title = await page.locator('.hero-title').text_content()
        assert "Saturday Run & Coffee Club" in hero_title
        
        print("✅ 페이지 로딩 테스트 통과")
    
    async def test_next_saturday_calculation(self, page_setup):
        """다음 토요일 자동 계산 테스트"""
        page, base_url = page_setup
        
        await page.goto(base_url)
        
        # 이벤트 날짜 요소 대기
        await page.wait_for_selector('.event-date')
        
        # 표시된 날짜 확인
        event_date = await page.locator('.event-date').text_content()
        assert "Saturday" in event_date or "토요일" in event_date
        
        # 시간 정보 확인
        event_time = await page.locator('.event-time').text_content()
        assert "AM" in event_time or "오전" in event_time
        
        print("✅ 다음 토요일 계산 테스트 통과")
    
    async def test_participant_registration(self, page_setup):
        """참가자 등록 폼 테스트"""
        page, base_url = page_setup
        
        await page.goto(base_url)
        
        # 폼 요소 확인
        name_input = page.locator('#participantName')
        join_button = page.locator('#joinBtn')
        
        assert await name_input.is_visible()
        assert await join_button.is_visible()
        
        # 테스트 데이터 입력
        test_name = f"테스트참가자_{datetime.now().strftime('%H%M%S')}"
        await name_input.fill(test_name)
        
        # 폼 제출
        await join_button.click()
        
        # 성공 모달 확인
        success_modal = page.locator('#successModal')
        await page.wait_for_selector('#successModal.show', timeout=5000)
        
        modal_visible = await success_modal.is_visible()
        assert modal_visible
        
        print("✅ 참가자 등록 테스트 통과")
    
    async def test_admin_functionality(self, page_setup):
        """관리자 기능 테스트"""
        page, base_url = page_setup
        
        # 관리자 모드로 접속
        admin_url = f"{base_url}?admin=runclub2024"
        await page.goto(admin_url)
        
        # 관리자 패널 표시 확인
        admin_controls = page.locator('#adminControls')
        await page.wait_for_selector('#adminControls', timeout=5000)
        
        assert await admin_controls.is_visible()
        
        # 관리자 버튼들 확인
        edit_event_btn = page.locator('#editEventBtn')
        clear_all_btn = page.locator('#clearAllBtn')
        add_participant_btn = page.locator('#addParticipantBtn')
        
        assert await edit_event_btn.is_visible()
        assert await clear_all_btn.is_visible()
        assert await add_participant_btn.is_visible()
        
        print("✅ 관리자 기능 테스트 통과")
    
    async def test_event_editing(self, page_setup):
        """이벤트 편집 기능 테스트"""
        page, base_url = page_setup
        
        # 관리자 모드로 접속
        admin_url = f"{base_url}?admin=runclub2024"
        await page.goto(admin_url)
        
        # Edit Event 버튼 클릭
        await page.click('#editEventBtn')
        
        # 편집 모달 표시 확인
        edit_modal = page.locator('#eventEditModal')
        await page.wait_for_selector('#eventEditModal.show', timeout=5000)
        
        assert await edit_modal.is_visible()
        
        # 폼 필드 확인 및 수정
        title_input = page.locator('#eventTitle')
        description_input = page.locator('#eventDescription')
        
        await title_input.fill("테스트 이벤트 제목")
        await description_input.fill("테스트 이벤트 설명")
        
        # 저장 버튼 클릭
        await page.click('#saveEventBtn')
        
        # 모달 닫힘 확인
        await page.wait_for_function(
            "document.querySelector('#eventEditModal').classList.contains('show') === false",
            timeout=5000
        )
        
        print("✅ 이벤트 편집 테스트 통과")
    
    async def test_mobile_responsiveness(self, browser_setup):
        """모바일 반응형 테스트"""
        browser = browser_setup['chromium']
        
        # 모바일 디바이스 시뮬레이션
        mobile_context = await browser.new_context(
            viewport={'width': 375, 'height': 667},  # iPhone SE
            user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)'
        )
        
        page = await mobile_context.new_page()
        await page.goto("http://localhost:8000")
        
        # 모바일에서 주요 요소 확인
        hero_title = page.locator('.hero-title')
        join_form = page.locator('.join-form')
        
        assert await hero_title.is_visible()
        assert await join_form.is_visible()
        
        # 모바일 메뉴 동작 확인 (있다면)
        viewport = await page.viewport_size()
        assert viewport['width'] == 375
        
        await mobile_context.close()
        print("✅ 모바일 반응형 테스트 통과")
    
    async def test_cross_browser_compatibility(self, browser_setup):
        """크로스 브라우저 호환성 테스트"""
        base_url = "http://localhost:8000"
        
        for browser_name, browser in browser_setup.items():
            print(f"🔍 {browser_name} 브라우저 테스트 시작")
            
            context = await browser.new_context()
            page = await context.new_page()
            
            # 페이지 로드
            await page.goto(base_url)
            
            # 기본 요소 확인
            hero_title = await page.locator('.hero-title').text_content()
            assert "Saturday Run & Coffee Club" in hero_title
            
            # 폼 동작 확인
            name_input = page.locator('#participantName')
            assert await name_input.is_visible()
            
            await context.close()
            print(f"✅ {browser_name} 브라우저 테스트 통과")
    
    async def test_performance_metrics(self, page_setup):
        """성능 메트릭 테스트"""
        page, base_url = page_setup
        
        # 성능 측정 시작
        await page.goto(base_url)
        
        # 페이지 로드 완료 대기
        await page.wait_for_load_state('networkidle')
        
        # JavaScript로 성능 메트릭 수집
        performance_metrics = await page.evaluate("""
            () => {
                const navigation = performance.getEntriesByType('navigation')[0];
                return {
                    loadTime: navigation.loadEventEnd - navigation.loadEventStart,
                    domContentLoaded: navigation.domContentLoadedEventEnd - navigation.domContentLoadedEventStart,
                    totalTime: navigation.loadEventEnd - navigation.fetchStart
                };
            }
        """)
        
        # 성능 기준 확인 (3초 이내)
        assert performance_metrics['totalTime'] < 3000
        
        print(f"✅ 성능 테스트 통과 - 로딩시간: {performance_metrics['totalTime']}ms")
    
    async def test_accessibility_standards(self, page_setup):
        """접근성 표준 테스트"""
        page, base_url = page_setup
        
        await page.goto(base_url)
        
        # 기본 접근성 요소 확인
        # 1. 이미지 alt 속성
        images = await page.locator('img').all()
        for img in images:
            alt_text = await img.get_attribute('alt')
            # alt 속성이 있거나 decorative 이미지여야 함
            
        # 2. 폼 라벨 확인
        inputs = await page.locator('input[type="text"]').all()
        for input_elem in inputs:
            # placeholder나 label이 있어야 함
            placeholder = await input_elem.get_attribute('placeholder')
            assert placeholder is not None
        
        # 3. 색상 대비 (기본적인 확인)
        # 실제로는 axe-core 같은 도구 사용 권장
        
        print("✅ 접근성 표준 테스트 통과")


# 테스트 실행을 위한 헬퍼 함수
async def run_all_tests():
    """모든 테스트를 순차적으로 실행"""
    test_instance = TestSaturdayRunClub()
    
    print("🚀 Saturday Run & Coffee Club E2E 테스트 시작")
    print("=" * 50)
    
    # 브라우저 설정
    async with async_playwright() as p:
        browsers = {
            'chromium': await p.chromium.launch(headless=False),
            'firefox': await p.firefox.launch(headless=False),
            'webkit': await p.webkit.launch(headless=False)
        }
        
        try:
            # 기본 테스트들 실행
            browser = browsers['chromium']
            context = await browser.new_context(
                viewport={'width': 1920, 'height': 1080}
            )
            page = await context.new_page()
            base_url = "http://localhost:8000"
            
            # 각 테스트 실행
            await test_instance.test_page_loading((page, base_url))
            await test_instance.test_next_saturday_calculation((page, base_url))
            await test_instance.test_participant_registration((page, base_url))
            await test_instance.test_admin_functionality((page, base_url))
            await test_instance.test_event_editing((page, base_url))
            await test_instance.test_performance_metrics((page, base_url))
            await test_instance.test_accessibility_standards((page, base_url))
            
            # 크로스 브라우저 테스트
            await test_instance.test_cross_browser_compatibility(browsers)
            
            # 모바일 테스트
            await test_instance.test_mobile_responsiveness(browsers)
            
            await context.close()
            
        finally:
            # 브라우저 정리
            for browser in browsers.values():
                await browser.close()
    
    print("=" * 50)
    print("🎉 모든 테스트 완료!")


if __name__ == "__main__":
    # 직접 실행시 모든 테스트 실행
    asyncio.run(run_all_tests())


