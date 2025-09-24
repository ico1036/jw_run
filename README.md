# 🚀 SuperClaude Framework 프로젝트

주인님을 위한 SuperClaude Framework 활용 가이드 및 실습 프로젝트입니다.

## 📋 프로젝트 구조

```
jw_run/
├── src/                    # 소스 코드
│   └── superclaude_helper.py  # SuperClaude 도우미 모듈
├── config/                 # 설정 파일
│   └── superclaude_config.json  # SuperClaude 설정
├── examples/               # 사용 예제
│   └── workflow_examples.py    # 워크플로우 예제
├── tests/                  # 테스트 코드
├── docs/                   # 문서
└── main.py                 # 메인 실행 파일
```

## 🛠️ 설치 및 설정

### 1. 환경 설정
```bash
# uv 패키지 매니저 설치 (이미 완료)
curl -Ls https://astral.sh/uv/install.sh | sh

# SuperClaude 설치 (이미 완료)
uv add SuperClaude

# 개발자 프로파일 설정
python3 -m SuperClaude install --profile developer
```

### 2. 프로젝트 실행
```bash
# 의존성 동기화
uv sync

# 예제 실행
uv run python examples/workflow_examples.py

# 도우미 모듈 테스트
uv run python src/superclaude_helper.py
```

## 🎯 주요 기능

### SuperClaude 명령어 체계
- **기획**: `/sc:design` → `/sc:estimate`
- **구현**: `/sc:implement` → `/sc:build`
- **검증**: `/sc:test` → `/sc:analyze`
- **개선**: `/sc:improve` → `/sc:cleanup`
- **문서화**: `/sc:document` → `/sc:explain`

### 페르소나 시스템
- `architect`: 시스템 설계, 아키텍처 결정
- `frontend`: UI/UX, 접근성 개선
- `backend`: API 설계, 인프라 구성
- `analyzer`: 디버깅, 성능 분석
- `security`: 보안 취약점 점검
- `scribe`: 기술 문서 작성

### MCP 서버 통합
- **Context7**: 공식 라이브러리 문서 참조
- **Sequential**: 복잡한 다단계 작업 처리
- **Magic**: 모던 UI 컴포넌트 생성
- **Playwright**: E2E 테스트 자동화

## 📚 워크플로우 예제

### 새 기능 개발
```python
from src.superclaude_helper import SuperClaudeHelper

helper = SuperClaudeHelper()
workflow = helper.get_workflow_commands("development")
# ["/sc:design", "/sc:implement", "/sc:test"]
```

### 버그 수정
```python
debug_workflow = helper.get_workflow_commands("debugging")
# ["/sc:troubleshoot", "/sc:analyze", "/sc:explain", "/sc:implement", "/sc:test"]
```

### 코드 품질 관리
```python
quality_check = helper.get_quality_checklist("pre_commit")
# ["/sc:test", "/sc:cleanup", "/sc:document", "/sc:analyze"]
```

## 🔧 설정 커스터마이징

`config/superclaude_config.json`에서 다음을 설정할 수 있습니다:

- `preferred_personas`: 선호하는 페르소나 목록
- `auto_cleanup`: 자동 정리 기능 활성화
- `token_optimization`: 토큰 최적화 수준
- `mcp_servers`: 사용할 MCP 서버 목록
- `workflow_patterns`: 커스텀 워크플로우 패턴

## 📖 베스트 프랙티스

### DO's ✅
- 명령어를 조합해서 워크플로우 구성
- 정기적으로 `/sc:index`로 프로젝트 상태 파악
- 복잡한 작업은 `/sc:task`로 분해
- MCP 서버를 적극 활용해 외부 도구 연동

### DON'Ts ❌
- 한 번에 너무 많은 작업 시도
- 토큰 관리 없이 긴 대화 진행
- 페르소나 자동 선택만 의존
- 테스트 없이 `/sc:implement` 실행

## 🚨 트러블슈팅

### 일반적인 문제 해결
- **MCP 서버 연결 실패**: 수동으로 재시작
- **페르소나 선택 오류**: 명시적 지정
- **토큰 한계 도달**: `/sc:cleanup` 실행
- **명령어 미작동**: `--interactive` 모드로 재설치

## 📞 지원

문제가 발생하면 주인님께 즉시 보고드리겠습니다. 🙇‍♂️
