"""
SuperClaude Framework 메인 실행 파일
주인님을 위한 SuperClaude 활용 데모
"""

from src.superclaude_helper import SuperClaudeHelper


def main():
    """메인 함수 - SuperClaude Framework 데모"""
    print("🚀 SuperClaude Framework 시작")
    print("주인님을 위한 개발 도우미가 준비되었습니다.\n")
    
    helper = SuperClaudeHelper()
    
    # 설정 정보 출력
    print("=== 현재 설정 ===")
    print(f"선호 페르소나: {helper.config.get('preferred_personas', [])}")
    print(f"자동 정리: {'활성화' if helper.is_auto_cleanup_enabled() else '비활성화'}")
    print(f"MCP 서버: {helper.get_mcp_servers()}")
    
    # 워크플로우 예제
    print("\n=== 사용 가능한 워크플로우 ===")
    workflows = ["development", "debugging", "refactoring"]
    
    for workflow in workflows:
        commands = helper.get_workflow_commands(workflow)
        if commands:
            print(f"{workflow}: {' → '.join(commands)}")
    
    # 페르소나 추천 예제
    print("\n=== 페르소나 추천 예제 ===")
    tasks = [
        "React 컴포넌트 개발",
        "API 서버 구축",
        "시스템 아키텍처 설계"
    ]
    
    for task in tasks:
        persona = helper.suggest_persona(task)
        print(f"{task} → {persona}")
    
    print("\n주인님, SuperClaude Framework가 준비되었습니다! 🙇‍♂️")


def hello() -> str:
    """기존 hello 함수 유지"""
    return "Hello from SuperClaude Framework!"


if __name__ == "__main__":
    main()
