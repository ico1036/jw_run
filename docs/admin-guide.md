# 🔧 Saturday Run & Coffee Club - 관리자 가이드

## 🚀 관리자 모드 접속

### URL 접속 방법
```
일반 사용자: https://ico1036.github.io/jw_run
관리자 모드: https://ico1036.github.io/jw_run?admin=runclub2024
```

**관리자 비밀키**: `runclub2024`

## 🎯 관리자 기능 개요

관리자 모드에서는 다음 기능들을 사용할 수 있습니다:

### 📋 관리자 패널
- **🗑️ Clear All**: 모든 참가자 삭제
- **📋 Export List**: 참가자 명단 텍스트 파일로 다운로드
- **➕ Add Participant**: 새 참가자 직접 추가

### 👥 개별 참가자 관리
- 각 참가자 이름 옆에 **[×]** 삭제 버튼 표시
- 클릭 한 번으로 개별 참가자 삭제

## 🛠️ 사용법 가이드

### 1. 관리자 모드 활성화
```
1. 웹사이트 URL 뒤에 ?admin=runclub2024 추가
2. 페이지 새로고침
3. 참가자 섹션에 관리자 패널 표시 확인
```

### 2. 참가자 추가
```
1. [➕ Add Participant] 버튼 클릭
2. 이름 입력 폼 표시
3. 참가자 이름 입력
4. [Add] 버튼 클릭
5. 즉시 목록에 추가됨
```

### 3. 개별 참가자 삭제
```
1. 참가자 이름 옆 [×] 버튼 클릭
2. 삭제 확인 대화상자
3. 확인 시 즉시 삭제
```

### 4. 전체 참가자 삭제
```
1. [🗑️ Clear All] 버튼 클릭
2. 삭제 확인 대화상자
3. 확인 시 모든 참가자 삭제
```

### 5. 참가자 명단 내보내기
```
1. [📋 Export List] 버튼 클릭
2. 텍스트 파일 자동 다운로드
3. 파일명: saturday-run-participants-YYYY-MM-DD.txt
```

## 💾 데이터 저장 방식

### localStorage 기반
- **저장 위치**: 브라우저 로컬 스토리지
- **키**: `saturday-run-participants`
- **형식**: JSON 배열

### 데이터 구조
```json
[
  {
    "name": "홍길동",
    "timestamp": "2024-09-24T12:00:00.000Z"
  },
  {
    "name": "김철수",
    "timestamp": "2024-09-24T12:05:00.000Z"
  }
]
```

## 🔒 보안 고려사항

### 간단한 인증
- URL 파라미터 기반 인증
- 비밀키: `runclub2024`
- 브라우저 개발자 도구에서 확인 가능

### 권장사항
```
1. 관리자 URL을 공개하지 마세요
2. 필요시 비밀키 변경 (js/app.js에서 수정)
3. 관리 작업 후 일반 URL로 이동
```

## 🚨 주의사항

### 데이터 백업
- localStorage는 브라우저별로 독립적
- 정기적으로 Export 기능으로 백업 권장
- 브라우저 데이터 삭제 시 참가자 목록 손실

### 브라우저 호환성
- 모던 브라우저에서만 동작
- Internet Explorer 미지원
- 모바일 브라우저 완전 지원

## 🔧 고급 관리

### 브라우저 개발자 도구 사용
```javascript
// F12 → Console 탭에서 실행

// 현재 참가자 확인
console.log(JSON.parse(localStorage.getItem('saturday-run-participants')));

// 수동 데이터 수정
let participants = JSON.parse(localStorage.getItem('saturday-run-participants')) || [];
participants.push({name: '새참가자', timestamp: new Date().toISOString()});
localStorage.setItem('saturday-run-participants', JSON.stringify(participants));

// 전체 삭제
localStorage.removeItem('saturday-run-participants');
```

## 📞 문제 해결

### 관리자 패널이 안 보여요
1. URL에 `?admin=runclub2024` 정확히 입력했는지 확인
2. 페이지 새로고침
3. 브라우저 캐시 삭제 후 재시도

### 참가자가 삭제되지 않아요
1. 브라우저 JavaScript 활성화 확인
2. 개발자 도구 Console에서 에러 확인
3. 페이지 새로고침 후 재시도

### 데이터가 사라졌어요
1. 같은 브라우저에서 접속했는지 확인
2. 시크릿 모드가 아닌지 확인
3. 브라우저 데이터가 삭제되었을 가능성

---

**관리자 비밀키**: `runclub2024`  
**관리자 URL**: `?admin=runclub2024`

*주인님의 Saturday Run & Coffee Club 관리를 위한 완벽한 도구입니다! 🏃‍♂️☕*


