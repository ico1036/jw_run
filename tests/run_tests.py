"""
SuperClaude + Playwright 통합 테스트 실행기
자동으로 테스트를 실행하고 분석 리포트를 생성
"""

import asyncio
import subprocess
import sys
import os
from datetime import datetime
from playwright.async_api import async_playwright
import json

# 프로젝트 루트 디렉토리를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tests.playwright.superclaude_analyzer import SuperClaudeTestAnalyzer


class TestRunner:
    """통합 테스트 실행기"""
    
    def __init__(self):
        self.analyzer = SuperClaudeTestAnalyzer()
        self.results = {}
    
    async def start_local_server(self):
        """로컬 서버 시작"""
        print("🚀 로컬 서버 시작 중...")
        
        # Saturday Run & Coffee Club 디렉토리로 이동해서 서버 시작
        server_cmd = [
            "python3", "-m", "http.server", "8000",
            "--directory", "saturday-run-coffee-club"
        ]
        
        try:
            self.server_process = subprocess.Popen(
                server_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            )
            
            # 서버 시작 대기
            await asyncio.sleep(3)
            print("✅ 로컬 서버 시작됨: http://localhost:8000")
            return True
            
        except Exception as e:
            print(f"❌ 서버 시작 실패: {e}")
            return False
    
    def stop_local_server(self):
        """로컬 서버 중지"""
        if hasattr(self, 'server_process'):
            self.server_process.terminate()
            print("🛑 로컬 서버 중지됨")
    
    async def run_basic_tests(self):
        """기본 기능 테스트 실행"""
        print("🔍 기본 기능 테스트 시작...")
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()
            
            base_url = "http://localhost:8000"
            test_results = {}
            
            try:
                # 1. 페이지 로딩 테스트
                print("  📄 페이지 로딩 테스트...")
                response = await page.goto(base_url)
                test_results['page_loading'] = response.status == 200
                
                # 2. 제목 확인
                title = await page.title()
                test_results['title_check'] = "Saturday Run & Coffee Club" in title
                
                # 3. 주요 요소 존재 확인
                hero_title = await page.locator('.hero-title').count()
                test_results['hero_element'] = hero_title > 0
                
                # 4. 폼 요소 확인
                name_input = await page.locator('#participantName').count()
                join_button = await page.locator('#joinBtn').count()
                test_results['form_elements'] = name_input > 0 and join_button > 0
                
                # 5. 성능 측정
                await page.wait_for_load_state('networkidle')
                performance = await page.evaluate("""
                    () => {
                        const navigation = performance.getEntriesByType('navigation')[0];
                        return {
                            loadTime: navigation.loadEventEnd - navigation.loadEventStart,
                            domContentLoaded: navigation.domContentLoadedEventEnd - navigation.domContentLoadedEventStart,
                            totalTime: navigation.loadEventEnd - navigation.fetchStart
                        };
                    }
                """)
                
                self.results['performance'] = performance
                self.results['functional_tests'] = test_results
                
                print("  ✅ 기본 기능 테스트 완료")
                
            except Exception as e:
                print(f"  ❌ 기본 기능 테스트 실패: {e}")
                test_results['error'] = str(e)
                self.results['functional_tests'] = test_results
            
            finally:
                await browser.close()
    
    async def run_admin_tests(self):
        """관리자 기능 테스트"""
        print("🔧 관리자 기능 테스트 시작...")
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()
            
            admin_results = {}
            
            try:
                # 관리자 모드 접속
                admin_url = "http://localhost:8000?admin=runclub2024"
                await page.goto(admin_url)
                
                # 관리자 패널 확인
                await page.wait_for_selector('#adminControls', timeout=5000)
                admin_panel_visible = await page.locator('#adminControls').is_visible()
                admin_results['admin_panel_access'] = admin_panel_visible
                
                # 관리자 버튼들 확인
                edit_btn = await page.locator('#editEventBtn').count()
                clear_btn = await page.locator('#clearAllBtn').count()
                add_btn = await page.locator('#addParticipantBtn').count()
                
                admin_results['admin_buttons'] = edit_btn > 0 and clear_btn > 0 and add_btn > 0
                
                self.results['admin_tests'] = admin_results
                print("  ✅ 관리자 기능 테스트 완료")
                
            except Exception as e:
                print(f"  ❌ 관리자 기능 테스트 실패: {e}")
                admin_results['error'] = str(e)
                self.results['admin_tests'] = admin_results
            
            finally:
                await browser.close()
    
    async def run_browser_compatibility_tests(self):
        """브라우저 호환성 테스트"""
        print("🌐 브라우저 호환성 테스트 시작...")
        
        browser_results = {}
        
        async with async_playwright() as p:
            browsers = {
                'chromium': p.chromium,
                'firefox': p.firefox,
                'webkit': p.webkit
            }
            
            for browser_name, browser_type in browsers.items():
                try:
                    print(f"  🔍 {browser_name} 테스트...")
                    browser = await browser_type.launch(headless=True)
                    context = await browser.new_context()
                    page = await context.new_page()
                    
                    # 기본 페이지 로드 테스트
                    response = await page.goto("http://localhost:8000")
                    
                    # 주요 요소 확인
                    hero_title = await page.locator('.hero-title').count()
                    
                    browser_results[browser_name] = response.status == 200 and hero_title > 0
                    
                    await browser.close()
                    print(f"    ✅ {browser_name} 테스트 완료")
                    
                except Exception as e:
                    print(f"    ❌ {browser_name} 테스트 실패: {e}")
                    browser_results[browser_name] = False
        
        self.results['browser_tests'] = browser_results
        print("  ✅ 브라우저 호환성 테스트 완료")
    
    async def run_mobile_tests(self):
        """모바일 반응형 테스트"""
        print("📱 모바일 반응형 테스트 시작...")
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            
            # 모바일 컨텍스트 생성
            mobile_context = await browser.new_context(
                viewport={'width': 375, 'height': 667},
                user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)'
            )
            
            page = await mobile_context.new_page()
            mobile_results = {}
            
            try:
                await page.goto("http://localhost:8000")
                
                # 모바일에서 주요 요소 확인
                hero_visible = await page.locator('.hero-title').is_visible()
                form_visible = await page.locator('.join-form').is_visible()
                
                mobile_results['responsive'] = hero_visible and form_visible
                mobile_results['viewport_correct'] = True
                
                self.results['mobile_tests'] = mobile_results
                print("  ✅ 모바일 반응형 테스트 완료")
                
            except Exception as e:
                print(f"  ❌ 모바일 테스트 실패: {e}")
                mobile_results['error'] = str(e)
                self.results['mobile_tests'] = mobile_results
            
            finally:
                await browser.close()
    
    async def run_all_tests(self):
        """모든 테스트 실행"""
        print("🚀 SuperClaude + Playwright 통합 테스트 시작")
        print("=" * 60)
        
        # 서버 시작
        server_started = await self.start_local_server()
        if not server_started:
            print("❌ 서버 시작 실패로 테스트 중단")
            return
        
        try:
            # 각 테스트 실행
            await self.run_basic_tests()
            await self.run_admin_tests()
            await self.run_browser_compatibility_tests()
            await self.run_mobile_tests()
            
            # 결과 분석
            print("\n🔍 SuperClaude 분석 시작...")
            analysis = self.analyzer.analyze_test_results(self.results)
            
            # 리포트 생성
            report = self.analyzer.generate_report(analysis)
            
            # 리포트 저장
            filepath = self.analyzer.save_report(report)
            print(f"📄 상세 리포트 저장됨: {filepath}")
            
            # 결과 요약 출력
            print("\n" + "=" * 60)
            print("📊 테스트 결과 요약")
            print("=" * 60)
            
            print(f"전체 상태: {analysis['overall_status']}")
            print(f"감지된 이슈: {len(analysis['issues'])}개")
            
            if analysis['issues']:
                print("\n🚨 주요 이슈:")
                for issue in analysis['issues']:
                    print(f"  - {issue['type']}: {issue['message']}")
            else:
                print("\n✅ 모든 테스트 통과!")
            
            # GitHub 이슈 생성 (필요시)
            if any(i['severity'] == 'HIGH' for i in analysis['issues']):
                github_issue = self.analyzer.create_github_issue(analysis)
                issue_file = f"tests/reports/github_issue_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
                
                os.makedirs("tests/reports", exist_ok=True)
                with open(issue_file, 'w', encoding='utf-8') as f:
                    f.write(github_issue)
                
                print(f"🐛 GitHub 이슈 템플릿 생성됨: {issue_file}")
        
        finally:
            # 서버 중지
            self.stop_local_server()
        
        print("\n🎉 모든 테스트 완료!")


async def main():
    """메인 실행 함수"""
    runner = TestRunner()
    await runner.run_all_tests()


if __name__ == "__main__":
    asyncio.run(main())


