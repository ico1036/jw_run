/**
 * Saturday Run & Coffee Club - JavaScript Application
 * GitHub API Integration for Event Management
 */

class SaturdayRunClub {
    constructor() {
        // GitHub Configuration (주인장이 설정해야 할 부분)
        this.config = {
            owner: 'ico1036', // 주인장의 GitHub 사용자명
            repo: 'jw_run', // Repository 이름
            apiUrl: 'https://api.github.com'
        };
        
        this.currentEvent = null;
        this.participants = [];
        this.isAdminMode = false;
        this.adminKey = 'runclub2024'; // 관리자 비밀키
        
        this.init();
    }
    
    init() {
        this.checkAdminMode();
        this.loadCurrentEvent();
        this.setupEventListeners();
        this.updateNextSaturday();
        this.loadParticipantsFromLocal();
    }
    
    setupEventListeners() {
        const joinForm = document.getElementById('joinForm');
        if (joinForm) {
            joinForm.addEventListener('submit', (e) => this.handleJoinSubmission(e));
        }
        
        // Admin event listeners
        this.setupAdminEventListeners();
    }
    
    setupAdminEventListeners() {
        // Clear All button
        const clearAllBtn = document.getElementById('clearAllBtn');
        if (clearAllBtn) {
            clearAllBtn.addEventListener('click', () => this.clearAllParticipants());
        }
        
        // Export button
        const exportBtn = document.getElementById('exportBtn');
        if (exportBtn) {
            exportBtn.addEventListener('click', () => this.exportParticipants());
        }
        
        // Add Participant button
        const addParticipantBtn = document.getElementById('addParticipantBtn');
        if (addParticipantBtn) {
            addParticipantBtn.addEventListener('click', () => this.showQuickAddForm());
        }
        
        // Quick Add Form buttons
        const confirmAddBtn = document.getElementById('confirmAddBtn');
        if (confirmAddBtn) {
            confirmAddBtn.addEventListener('click', () => this.confirmAddParticipant());
        }
        
        const cancelAddBtn = document.getElementById('cancelAddBtn');
        if (cancelAddBtn) {
            cancelAddBtn.addEventListener('click', () => this.hideQuickAddForm());
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
                const participantItems = this.participants.map((participant, index) => 
                    `<div class="participant-item">
                        <span class="participant-name"><strong>${this.escapeHtml(participant.name)}</strong></span>
                        <button class="participant-delete" onclick="app.removeParticipant(${index})" title="Remove participant">×</button>
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
    
    // 관리자 모드 체크
    checkAdminMode() {
        const urlParams = new URLSearchParams(window.location.search);
        const adminParam = urlParams.get('admin');
        
        if (adminParam === this.adminKey) {
            this.isAdminMode = true;
            this.showAdminControls();
            document.body.classList.add('admin-mode');
            console.log('🔧 Admin mode activated');
        }
    }
    
    // 관리자 컨트롤 표시
    showAdminControls() {
        const adminControls = document.getElementById('adminControls');
        if (adminControls) {
            adminControls.style.display = 'block';
        }
    }
    
    // 모든 참가자 삭제
    clearAllParticipants() {
        if (confirm('정말로 모든 참가자를 삭제하시겠습니까?')) {
            this.participants = [];
            localStorage.removeItem('saturday-run-participants');
            this.updateParticipantsDisplay();
            this.showNotification('모든 참가자가 삭제되었습니다.', 'success');
        }
    }
    
    // 참가자 목록 내보내기
    exportParticipants() {
        if (this.participants.length === 0) {
            this.showNotification('내보낼 참가자가 없습니다.', 'warning');
            return;
        }
        
        const participantNames = this.participants.map(p => p.name).join('\n');
        const blob = new Blob([participantNames], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        
        const a = document.createElement('a');
        a.href = url;
        a.download = `saturday-run-participants-${new Date().toISOString().split('T')[0]}.txt`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        
        this.showNotification('참가자 목록이 다운로드되었습니다.', 'success');
    }
    
    // 빠른 추가 폼 표시
    showQuickAddForm() {
        const quickAddForm = document.getElementById('quickAddForm');
        if (quickAddForm) {
            quickAddForm.style.display = 'block';
            document.getElementById('quickAddName').focus();
        }
    }
    
    // 빠른 추가 폼 숨기기
    hideQuickAddForm() {
        const quickAddForm = document.getElementById('quickAddForm');
        if (quickAddForm) {
            quickAddForm.style.display = 'none';
            document.getElementById('quickAddName').value = '';
        }
    }
    
    // 참가자 추가 확인
    confirmAddParticipant() {
        const nameInput = document.getElementById('quickAddName');
        const name = nameInput.value.trim();
        
        if (!name) {
            this.showNotification('이름을 입력해주세요.', 'warning');
            return;
        }
        
        // 중복 체크
        if (this.participants.some(p => p.name.toLowerCase() === name.toLowerCase())) {
            this.showNotification('이미 등록된 참가자입니다.', 'warning');
            return;
        }
        
        const participant = {
            name: name,
            timestamp: new Date().toISOString()
        };
        
        this.participants.push(participant);
        localStorage.setItem('saturday-run-participants', JSON.stringify(this.participants));
        this.updateParticipantsDisplay();
        this.hideQuickAddForm();
        this.showNotification(`${name}님이 추가되었습니다.`, 'success');
    }
    
    // 개별 참가자 삭제
    removeParticipant(index) {
        if (index >= 0 && index < this.participants.length) {
            const participant = this.participants[index];
            if (confirm(`${participant.name}님을 삭제하시겠습니까?`)) {
                this.participants.splice(index, 1);
                localStorage.setItem('saturday-run-participants', JSON.stringify(this.participants));
                this.updateParticipantsDisplay();
                this.showNotification(`${participant.name}님이 삭제되었습니다.`, 'success');
            }
        }
    }
    
    // 알림 표시
    showNotification(message, type = 'info') {
        // 간단한 알림 (alert 대신 사용)
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 12px 20px;
            border-radius: 8px;
            color: white;
            font-weight: 500;
            z-index: 1000;
            transition: all 0.3s ease;
            background: ${type === 'success' ? '#28A745' : type === 'warning' ? '#FFC107' : '#007BFF'};
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.style.opacity = '0';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 3000);
    }
}

// 모달 닫기 함수
function closeModal() {
    const modal = document.getElementById('successModal');
    if (modal) {
        modal.classList.remove('show');
    }
}

// 전역 app 변수 (관리자 기능에서 사용)
let app;

// 애플리케이션 초기화
document.addEventListener('DOMContentLoaded', () => {
    app = new SaturdayRunClub();
});

// 모달 외부 클릭 시 닫기
document.addEventListener('click', (e) => {
    const modal = document.getElementById('successModal');
    if (modal && e.target === modal) {
        closeModal();
    }
});
