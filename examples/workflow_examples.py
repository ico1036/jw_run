"""
SuperClaude Framework 워크플로우 예제
주인님을 위한 실제 사용 예제들
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.superclaude_helper import SuperClaudeHelper


def example_new_feature_development():
    """새 기능 개발 워크플로우 예제"""
    print("=== 새 기능 개발 워크플로우 ===")
    
    helper = SuperClaudeHelper()
    
    # 1. 기획 단계
    design_commands = ["/sc:design", "/sc:estimate"]
    print("1. 기획 단계:")
    for cmd in design_commands:
        print(f"   {cmd}")
    
    # 2. 구현 단계
    impl_commands = helper.get_workflow_commands("development")
    print("\n2. 구현 단계:")
    for cmd in impl_commands:
        print(f"   {cmd}")
    
    # 3. 품질 검증
    quality_commands = helper.get_quality_checklist("pre_commit")
    print("\n3. 품질 검증:")
    for cmd in quality_commands:
        print(f"   {cmd}")


def example_bug_fixing():
    """버그 수정 워크플로우 예제"""
    print("=== 버그 수정 워크플로우 ===")
    
    helper = SuperClaudeHelper()
    
    # 디버깅 워크플로우
    debug_commands = helper.get_workflow_commands("debugging")
    print("디버깅 프로세스:")
    for i, cmd in enumerate(debug_commands, 1):
        print(f"   {i}. {cmd}")
    
    # 추천 페르소나
    persona = helper.suggest_persona("API 에러 디버깅")
    print(f"\n추천 페르소나: {persona}")


def example_code_refactoring():
    """코드 리팩토링 워크플로우 예제"""
    print("=== 코드 리팩토링 워크플로우 ===")
    
    helper = SuperClaudeHelper()
    
    # 리팩토링 워크플로우
    refactor_commands = helper.get_workflow_commands("refactoring")
    print("리팩토링 프로세스:")
    for i, cmd in enumerate(refactor_commands, 1):
        print(f"   {i}. {cmd}")


def example_persona_selection():
    """페르소나 선택 예제"""
    print("=== 페르소나 선택 예제 ===")
    
    helper = SuperClaudeHelper()
    
    tasks = [
        "React 컴포넌트 UI 개선",
        "FastAPI 백엔드 API 개발", 
        "시스템 아키텍처 설계",
        "성능 문제 분석",
        "보안 취약점 점검",
        "기술 문서 작성"
    ]
    
    for task in tasks:
        persona = helper.suggest_persona(task)
        print(f"작업: {task} → 추천 페르소나: {persona}")


def example_mcp_server_usage():
    """MCP 서버 활용 예제"""
    print("=== MCP 서버 활용 예제 ===")
    
    helper = SuperClaudeHelper()
    servers = helper.get_mcp_servers()
    
    print("설정된 MCP 서버들:")
    for server in servers:
        print(f"   - {server}")
    
    print("\nMCP 서버별 활용 시나리오:")
    scenarios = {
        "Context7": "공식 라이브러리 문서 참조 시",
        "Sequential": "복잡한 다단계 작업 처리",
        "Magic": "모던 UI 컴포넌트 생성",
        "Playwright": "E2E 테스트 자동화"
    }
    
    for server, scenario in scenarios.items():
        if server in servers:
            print(f"   {server}: {scenario}")


def example_git_workflow():
    """Git 워크플로우 통합 예제"""
    print("=== Git 워크플로우 통합 ===")
    
    git_workflow = [
        "/sc:git status",    # 변경사항 확인
        "/sc:test",          # 테스트 실행
        "/sc:cleanup",       # 코드 정리
        "/sc:document",      # 문서 업데이트
        "/sc:git commit"     # 커밋 작성
    ]
    
    print("커밋 전 체크리스트:")
    for i, cmd in enumerate(git_workflow, 1):
        print(f"   {i}. {cmd}")


if __name__ == "__main__":
    print("SuperClaude Framework 워크플로우 예제 모음\n")
    
    example_new_feature_development()
    print("\n" + "="*50 + "\n")
    
    example_bug_fixing()
    print("\n" + "="*50 + "\n")
    
    example_code_refactoring()
    print("\n" + "="*50 + "\n")
    
    example_persona_selection()
    print("\n" + "="*50 + "\n")
    
    example_mcp_server_usage()
    print("\n" + "="*50 + "\n")
    
    example_git_workflow()
