"""
SuperClaude Framework Helper Module
주인님을 위한 SuperClaude 명령어 및 워크플로우 도우미
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional


class SuperClaudeHelper:
    """SuperClaude Framework 활용을 위한 도우미 클래스"""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        초기화
        Args:
            config_path: 설정 파일 경로 (기본값: config/superclaude_config.json)
        """
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "superclaude_config.json"
        
        self.config_path = Path(config_path)
        self.config = self._load_config()
    
    def _load_config(self) -> Dict:
        """설정 파일 로드"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict:
        """기본 설정 반환"""
        return {
            "preferred_personas": ["architect", "backend"],
            "auto_cleanup": True,
            "token_optimization": "moderate",
            "mcp_servers": ["Context7", "Sequential"]
        }
    
    def get_workflow_commands(self, workflow_type: str) -> List[str]:
        """
        워크플로우 타입에 따른 명령어 시퀀스 반환
        
        Args:
            workflow_type: 워크플로우 타입 (development, debugging, refactoring 등)
        
        Returns:
            명령어 리스트
        """
        workflows = self.config.get("workflow_patterns", {})
        return workflows.get(workflow_type, [])
    
    def get_quality_checklist(self, check_type: str) -> List[str]:
        """
        품질 체크리스트 반환
        
        Args:
            check_type: 체크 타입 (pre_commit, code_review 등)
        
        Returns:
            체크리스트 명령어 리스트
        """
        checklists = self.config.get("quality_checklist", {})
        return checklists.get(check_type, [])
    
    def suggest_persona(self, task_description: str) -> str:
        """
        작업 설명에 따른 페르소나 추천
        
        Args:
            task_description: 작업 설명
        
        Returns:
            추천 페르소나
        """
        task_lower = task_description.lower()
        
        if any(keyword in task_lower for keyword in ["ui", "frontend", "react", "vue", "angular"]):
            return "frontend"
        elif any(keyword in task_lower for keyword in ["api", "backend", "server", "database"]):
            return "backend"
        elif any(keyword in task_lower for keyword in ["architecture", "design", "system"]):
            return "architect"
        elif any(keyword in task_lower for keyword in ["debug", "error", "bug", "analyze"]):
            return "analyzer"
        elif any(keyword in task_lower for keyword in ["security", "vulnerability", "auth"]):
            return "security"
        elif any(keyword in task_lower for keyword in ["document", "readme", "guide"]):
            return "scribe"
        else:
            return self.config.get("preferred_personas", ["architect"])[0]
    
    def format_command_sequence(self, commands: List[str]) -> str:
        """
        명령어 시퀀스를 포맷팅하여 반환
        
        Args:
            commands: 명령어 리스트
        
        Returns:
            포맷팅된 명령어 문자열
        """
        if not commands:
            return "명령어가 없습니다."
        
        formatted = "SuperClaude 명령어 시퀀스:\n"
        for i, cmd in enumerate(commands, 1):
            formatted += f"{i}. {cmd}\n"
        
        return formatted
    
    def get_mcp_servers(self) -> List[str]:
        """설정된 MCP 서버 목록 반환"""
        return self.config.get("mcp_servers", [])
    
    def is_auto_cleanup_enabled(self) -> bool:
        """자동 정리 기능 활성화 여부 확인"""
        return self.config.get("auto_cleanup", False)


# 편의 함수들
def get_development_workflow() -> List[str]:
    """개발 워크플로우 명령어 반환"""
    helper = SuperClaudeHelper()
    return helper.get_workflow_commands("development")


def get_debugging_workflow() -> List[str]:
    """디버깅 워크플로우 명령어 반환"""
    helper = SuperClaudeHelper()
    return helper.get_workflow_commands("debugging")


def get_pre_commit_checklist() -> List[str]:
    """커밋 전 체크리스트 반환"""
    helper = SuperClaudeHelper()
    return helper.get_quality_checklist("pre_commit")


if __name__ == "__main__":
    # 테스트 코드
    helper = SuperClaudeHelper()
    
    print("=== SuperClaude Framework Helper 테스트 ===")
    print(f"개발 워크플로우: {helper.get_workflow_commands('development')}")
    print(f"디버깅 워크플로우: {helper.get_workflow_commands('debugging')}")
    print(f"UI 작업 추천 페르소나: {helper.suggest_persona('React 컴포넌트 개발')}")
    print(f"백엔드 작업 추천 페르소나: {helper.suggest_persona('API 서버 구축')}")
