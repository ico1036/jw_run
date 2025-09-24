/**
 * Saturday Run & Coffee Club - JavaScript Application
 * GitHub API Integration for Event Management
 */

class SaturdayRunClub {
    constructor() {
        // GitHub Configuration (주인장이 설정해야 할 부분)
        this.config = {
            owner: 'YOUR_GITHUB_USERNAME', // 주인장의 GitHub 사용자명
            repo: 'saturday-run-coffee-club', // Repository 이름
            apiUrl: 'https://api.github.com'
        };
        
        this.currentEvent = null;
        this.participants = [];
        
        this.init();
    }
    
    init() {
        this.loadCurrentEvent();
        this.setupEventListeners();
        this.updateNextSaturday();
    }
    
    setupEventListeners() {
        const joinForm = document.getElementById('joinForm');
        if (joinForm) {
            joinForm.addEventListener('submit', (e) => this.handleJoinSubmission(e));
        }
    }
    
    // 다음 토요일 날짜 계산
    getNextSaturday() {
        const today = new Date();
        const dayOfWeek = today.getDay();
        const daysUntilSaturday = (6 - dayOfWeek) % 7;
        const nextSaturday = new Date(today);
        
        if (daysUntilSaturday === 0 && today.getHours() >= 10) {
            // 토요일이고 오전 10시 이후라면 다음 주 토요일
            nextSaturday.setDate(today.getDate() + 7);
        } else {
            nextSaturday.setDate(today.getDate() + daysUntilSaturday);
        }
        
        return nextSaturday;
    }
    
    // 다음 토요일 정보 업데이트
    updateNextSaturday() {
        const nextSaturday = this.getNextSaturday();
        const options = { 
            weekday: 'long', 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric' 
        };
        
        const eventCard = document.getElementById('eventCard');
        if (eventCard) {
            eventCard.innerHTML = `
                <div class="event-date">${nextSaturday.toLocaleDateString('en-US', options)}</div>
                <div class="event-time">8:00 AM - 11:00 AM</div>
                <div class="event-details">
                    <p>Join us for our weekly 5km run followed by specialty coffee and productive activities. 
                    Meet at the usual starting point and bring your positive energy!</p>
                </div>
            `;
        }
    }
    
    // GitHub Issues API를 통해 현재 이벤트 로드
    async loadCurrentEvent() {
        try {
            const response = await fetch(`${this.config.apiUrl}/repos/${this.config.owner}/${this.config.repo}/issues?labels=event&state=open&sort=created&direction=desc&per_page=1`);
            
            if (!response.ok) {
                throw new Error('Failed to fetch events');
            }
            
            const issues = await response.json();
            
            if (issues.length > 0) {
                this.currentEvent = issues[0];
                this.loadParticipants();
            } else {
                // 이벤트가 없으면 기본 다음 토요일 정보 표시
                this.updateNextSaturday();
                this.updateParticipantsDisplay();
            }
        } catch (error) {
            console.log('GitHub API not configured or unavailable, using default event');
            this.updateNextSaturday();
            this.updateParticipantsDisplay();
        }
    }
    
    // 참여자 목록 로드 (GitHub Issue Comments)
    async loadParticipants() {
        if (!this.currentEvent) return;
        
        try {
            const response = await fetch(`${this.config.apiUrl}/repos/${this.config.owner}/${this.config.repo}/issues/${this.currentEvent.number}/comments`);
            
            if (!response.ok) {
                throw new Error('Failed to fetch participants');
            }
            
            const comments = await response.json();
            this.participants = comments.map(comment => this.parseParticipantFromComment(comment));
            this.updateParticipantsDisplay();
        } catch (error) {
            console.log('Failed to load participants:', error);
            this.updateParticipantsDisplay();
        }
    }
    
    // 댓글에서 참여자 정보 파싱
    parseParticipantFromComment(comment) {
        const body = comment.body;
        const lines = body.split('\n');
        
        let name = 'Anonymous';
        let contact = '';
        let message = '';
        
        lines.forEach(line => {
            if (line.startsWith('Name:')) {
                name = line.replace('Name:', '').trim();
            }
        });
        
        return { name, timestamp: comment.created_at };
    }
    
    // 참여자 목록 UI 업데이트
    updateParticipantsDisplay() {
        const countElement = document.getElementById('participantCount');
        const listElement = document.getElementById('participantsList');
        
        if (countElement) {
            countElement.textContent = this.participants.length;
        }
        
        if (listElement) {
            if (this.participants.length === 0) {
                listElement.innerHTML = '<p class="no-participants">No participants yet. Be the first to join!</p>';
            } else {
                const participantItems = this.participants.map(participant => 
                    `<div class="participant-item">
                        <strong>${this.escapeHtml(participant.name)}</strong>
                    </div>`
                ).join('');
                
                listElement.innerHTML = participantItems;
            }
        }
    }
    
    // 참여 신청 처리
    async handleJoinSubmission(event) {
        event.preventDefault();
        
        const formData = new FormData(event.target);
        const participantData = {
            name: formData.get('name')
        };
        
        // 폼 검증
        if (!participantData.name) {
            alert('Please enter your name.');
            return;
        }
        
        // 버튼 비활성화
        const submitBtn = document.getElementById('joinBtn');
        const originalText = submitBtn.innerHTML;
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span>Submitting...</span>';
        
        try {
            await this.submitParticipation(participantData);
            this.showSuccessModal();
            event.target.reset();
            
            // 참여자 목록 새로고침
            setTimeout(() => {
                this.loadParticipants();
            }, 1000);
            
        } catch (error) {
            console.error('Failed to submit participation:', error);
            alert('Sorry, there was an error submitting your registration. Please try again or contact the organizer directly.');
        } finally {
            // 버튼 복원
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalText;
        }
    }
    
    // GitHub API를 통한 참여 신청 제출
    async submitParticipation(participantData) {
        // GitHub API 설정이 안 되어 있으면 로컬 저장
        if (this.config.owner === 'YOUR_GITHUB_USERNAME') {
            this.addParticipantLocally(participantData);
            return;
        }
        
        const commentBody = `Name: ${participantData.name}

---
*Registered via Saturday Run & Coffee Club website*`;
        
        const response = await fetch(`${this.config.apiUrl}/repos/${this.config.owner}/${this.config.repo}/issues/${this.currentEvent.number}/comments`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `token ${this.getGitHubToken()}` // Personal Access Token 필요
            },
            body: JSON.stringify({
                body: commentBody
            })
        });
        
        if (!response.ok) {
            throw new Error('Failed to submit to GitHub');
        }
    }
    
    // 로컬 참여자 추가 (GitHub API 미설정 시)
    addParticipantLocally(participantData) {
        const participant = {
            ...participantData,
            timestamp: new Date().toISOString()
        };
        
        this.participants.push(participant);
        this.updateParticipantsDisplay();
        
        // 로컬 스토리지에 저장
        localStorage.setItem('saturday-run-participants', JSON.stringify(this.participants));
    }
    
    // 로컬 스토리지에서 참여자 로드
    loadParticipantsFromLocal() {
        const stored = localStorage.getItem('saturday-run-participants');
        if (stored) {
            this.participants = JSON.parse(stored);
            this.updateParticipantsDisplay();
        }
    }
    
    // GitHub Personal Access Token (실제 구현 시 보안 고려 필요)
    getGitHubToken() {
        // 실제로는 서버사이드에서 처리하거나 GitHub Actions 사용 권장
        return process.env.GITHUB_TOKEN || '';
    }
    
    // 성공 모달 표시
    showSuccessModal() {
        const modal = document.getElementById('successModal');
        if (modal) {
            modal.classList.add('show');
        }
    }
    
    // HTML 이스케이프
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// 모달 닫기 함수
function closeModal() {
    const modal = document.getElementById('successModal');
    if (modal) {
        modal.classList.remove('show');
    }
}

// 애플리케이션 초기화
document.addEventListener('DOMContentLoaded', () => {
    new SaturdayRunClub();
});

// 모달 외부 클릭 시 닫기
document.addEventListener('click', (e) => {
    const modal = document.getElementById('successModal');
    if (modal && e.target === modal) {
        closeModal();
    }
});
