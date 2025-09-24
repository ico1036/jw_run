# 🚀 Saturday Run & Coffee Club - Setup Guide

## 주인장을 위한 5분 설정 가이드

### 1단계: GitHub Repository 생성 (2분)

1. **GitHub에 로그인** → [github.com](https://github.com)

2. **새 Repository 생성**
   - Repository name: `saturday-run-coffee-club`
   - Public으로 설정
   - README 체크 해제 (이미 있음)

3. **파일 업로드**
   ```bash
   # 터미널에서 실행
   cd saturday-run-coffee-club
   git init
   git add .
   git commit -m "Initial commit: Saturday Run & Coffee Club"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/saturday-run-coffee-club.git
   git push -u origin main
   ```

### 2단계: GitHub Pages 활성화 (1분)

1. **Repository Settings** → **Pages**
2. **Source**: Deploy from a branch
3. **Branch**: main / (root)
4. **Save** 클릭

✅ **완료!** 5-10분 후 사이트가 활성화됩니다:
`https://YOUR_USERNAME.github.io/saturday-run-coffee-club`

### 3단계: 첫 이벤트 공지 (2분)

#### 방법 A: 기본 모드 (추천)
- 웹사이트가 자동으로 다음 토요일을 표시합니다
- 참여자는 폼으로 신청하고 로컬에 저장됩니다

#### 방법 B: GitHub Issues 연동 (고급)
1. **Issues 탭** → **New Issue**
2. **Title**: "Saturday Run & Coffee - [날짜]"
3. **Labels**: "event" 추가
4. **Description**:
   ```markdown
   ## 이번 주 토요일 모임 🏃‍♂️☕
   
   **일시**: 2024년 X월 X일 토요일 오전 8시
   **장소**: [만날 장소]
   **코스**: 5km 러닝 + 카페
   
   참여하실 분들은 웹사이트에서 신청해주세요!
   ```

### 4단계: 커스터마이징 (선택사항)

#### 기본 정보 수정
`index.html` 파일에서:
- 클럽 이름
- 만날 장소
- 연락처 정보

#### 색상 변경
`css/style.css`의 `:root` 섹션에서 색상 변수 수정

#### GitHub API 연동 (고급)
`js/app.js`에서:
```javascript
this.config = {
    owner: 'YOUR_ACTUAL_USERNAME', // 실제 GitHub 사용자명으로 변경
    repo: 'saturday-run-coffee-club',
    apiUrl: 'https://api.github.com'
};
```

## 🎯 주간 운영 루틴

### 매주 화요일 (이벤트 공지)
1. GitHub Issues에 새 이벤트 생성
2. 소셜미디어/단톡방에 웹사이트 링크 공유

### 매주 금요일 (참여자 확인)
1. 웹사이트에서 참여자 수 확인
2. 필요시 개별 연락

### 토요일 당일
1. 참여자 명단 확인
2. 즐거운 러닝 & 커피 타임! ☕

## 🆘 문제 해결

### 웹사이트가 안 보여요
- GitHub Pages 설정 확인
- 5-10분 대기 (배포 시간)
- Repository가 Public인지 확인

### 참여 신청이 안 돼요
- 브라우저 콘솔 에러 확인
- 폼 필드 모두 입력했는지 확인
- 인터넷 연결 상태 확인

### 디자인을 바꾸고 싶어요
- `css/style.css` 파일 수정
- 색상 변수부터 시작하는 것을 추천

## 📞 지원

더 궁금한 점이 있으시면:
1. GitHub Issues에 질문 등록
2. README.md 파일 참고
3. 개발자에게 직접 문의

---

*단순함이 미학입니다. 복잡하게 생각하지 마세요! 🌟*
