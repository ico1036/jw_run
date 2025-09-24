/**
 * Saturday Run & Coffee Club - 초단순 서버
 * SuperClaude 설계: 최소한의 API로 실시간 참가자 공유
 */

const express = require('express');
const cors = require('cors');
const fs = require('fs').promises;
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;
const DATA_FILE = path.join(__dirname, 'participants.json');

// 미들웨어
app.use(cors());
app.use(express.json());
app.use(express.static('.'));  // 현재 디렉토리의 정적 파일 서빙

// 참가자 데이터 초기화 (GitHub DB 연동)
async function initializeData() {
    try {
        const stats = await fs.stat(DATA_FILE);
        console.log(`✅ 기존 데이터 파일 확인됨 (${stats.size} bytes)`);
    } catch (error) {
        console.log('📄 participants.json 파일 없음 - GitHub에서 복구 시도...');
        
        // GitHub에서 데이터 복구 시도
        try {
            const githubData = await loadFromGitHub();
            if (githubData && githubData.length > 0) {
                await fs.writeFile(DATA_FILE, JSON.stringify(githubData, null, 2));
                console.log(`🔄 GitHub에서 ${githubData.length}명의 참가자 복구됨`);
            } else {
                console.log('📄 GitHub에도 데이터 없음 - 새로 시작');
            }
        } catch (githubError) {
            console.log('⚠️ GitHub 복구 실패:', githubError.message);
        }
    }
    
    // 이벤트 설정도 GitHub에서 복구 시도
    try {
        await loadEventConfigFromGitHub();
    } catch (error) {
        console.log('⚠️ 이벤트 설정 복구 실패:', error.message);
    }
}

// 참가자 데이터 읽기
async function readParticipants() {
    try {
        const data = await fs.readFile(DATA_FILE, 'utf8');
        return JSON.parse(data);
    } catch (error) {
        console.error('데이터 읽기 에러:', error);
        return [];
    }
}

// 참가자 데이터 저장 (GitHub DB 백업 포함)
async function saveParticipants(participants) {
    try {
        // 로컬 파일 저장
        await fs.writeFile(DATA_FILE, JSON.stringify(participants, null, 2));
        
        // GitHub에 백업 (비동기로 실행, 실패해도 로컬 저장은 성공)
        saveToGitHub(participants).catch(error => {
            console.log('⚠️ GitHub 백업 실패 (로컬 저장은 성공):', error.message);
        });
        
        return true;
    } catch (error) {
        console.error('데이터 저장 에러:', error);
        return false;
    }
}

// GitHub에서 데이터 로드
async function loadFromGitHub() {
    const GITHUB_OWNER = 'ico1036';
    const GITHUB_REPO = 'jw_run';
    
    try {
        const response = await fetch(
            `https://api.github.com/repos/${GITHUB_OWNER}/${GITHUB_REPO}/contents/saturday-run-coffee-club/participants.json`,
            {
                headers: {
                    'Accept': 'application/vnd.github.v3+json',
                    'User-Agent': 'Saturday-Run-Club'
                }
            }
        );
        
        if (!response.ok) {
            if (response.status === 404) {
                console.log('📄 GitHub에 participants.json 파일 없음');
                return [];
            }
            throw new Error(`GitHub API 오류: ${response.status}`);
        }
        
        const fileData = await response.json();
        const content = Buffer.from(fileData.content, 'base64').toString('utf8');
        const participants = JSON.parse(content);
        
        console.log(`📥 GitHub에서 ${participants.length}명의 참가자 로드됨`);
        return participants;
        
    } catch (error) {
        console.error('GitHub 로드 실패:', error.message);
        return [];
    }
}

// GitHub에 데이터 저장
async function saveToGitHub(participants) {
    const GITHUB_TOKEN = process.env.GITHUB_TOKEN;
    const GITHUB_OWNER = 'ico1036';
    const GITHUB_REPO = 'jw_run';
    
    if (!GITHUB_TOKEN) {
        console.log('💡 GITHUB_TOKEN 환경변수가 없어 GitHub 백업 건너뜀');
        return;
    }
    
    try {
        const content = JSON.stringify(participants, null, 2);
        const encodedContent = Buffer.from(content).toString('base64');
        
        // 기존 파일 SHA 가져오기
        let sha = null;
        try {
            const getResponse = await fetch(
                `https://api.github.com/repos/${GITHUB_OWNER}/${GITHUB_REPO}/contents/saturday-run-coffee-club/participants.json`,
                {
                    headers: {
                        'Authorization': `token ${GITHUB_TOKEN}`,
                        'Accept': 'application/vnd.github.v3+json'
                    }
                }
            );
            if (getResponse.ok) {
                const fileData = await getResponse.json();
                sha = fileData.sha;
            }
        } catch (e) {
            // 파일이 없으면 새로 생성
        }
        
        // GitHub에 파일 업데이트/생성
        const updateResponse = await fetch(
            `https://api.github.com/repos/${GITHUB_OWNER}/${GITHUB_REPO}/contents/saturday-run-coffee-club/participants.json`,
            {
                method: 'PUT',
                headers: {
                    'Authorization': `token ${GITHUB_TOKEN}`,
                    'Accept': 'application/vnd.github.v3+json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: `🔄 자동 백업: ${participants.length}명의 참가자 (${new Date().toISOString()})`,
                    content: encodedContent,
                    ...(sha && { sha })
                })
            }
        );
        
        if (updateResponse.ok) {
            console.log(`💾 GitHub 백업 성공: ${participants.length}명의 참가자`);
        } else {
            throw new Error(`GitHub API 오류: ${updateResponse.status}`);
        }
        
    } catch (error) {
        throw new Error(`GitHub 백업 실패: ${error.message}`);
    }
}

// API 라우트들

// 참가자 목록 조회
app.get('/api/participants', async (req, res) => {
    try {
        const participants = await readParticipants();
        
        // 이번 주 토요일 참가자만 필터링 (단순화)
        const thisWeekParticipants = participants.filter(p => {
            const participantDate = new Date(p.timestamp);
            const now = new Date();
            const weekAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
            return participantDate > weekAgo;
        });
        
        console.log(`📊 참가자 조회: ${thisWeekParticipants.length}명`);
        res.json({
            success: true,
            participants: thisWeekParticipants,
            count: thisWeekParticipants.length
        });
    } catch (error) {
        console.error('참가자 조회 에러:', error);
        res.status(500).json({
            success: false,
            error: 'Failed to fetch participants'
        });
    }
});

// 참가자 등록
app.post('/api/participants', async (req, res) => {
    try {
        const { name } = req.body;
        
        if (!name || name.trim().length === 0) {
            return res.status(400).json({
                success: false,
                error: 'Name is required'
            });
        }
        
        const participants = await readParticipants();
        
        // 중복 확인 (이름 기준, 단순화)
        const existingParticipant = participants.find(p => 
            p.name.toLowerCase() === name.trim().toLowerCase()
        );
        
        if (existingParticipant) {
            // 기존 참가자 타임스탬프 업데이트
            existingParticipant.timestamp = new Date().toISOString();
            console.log(`🔄 참가자 업데이트: ${name}`);
        } else {
            // 새 참가자 추가
            const newParticipant = {
                id: Date.now().toString(),
                name: name.trim(),
                timestamp: new Date().toISOString()
            };
            participants.push(newParticipant);
            console.log(`➕ 새 참가자 등록: ${name}`);
        }
        
        const saved = await saveParticipants(participants);
        
        if (saved) {
            // 최신 참가자 목록 반환
            const thisWeekParticipants = participants.filter(p => {
                const participantDate = new Date(p.timestamp);
                const now = new Date();
                const weekAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
                return participantDate > weekAgo;
            });
            
            res.json({
                success: true,
                message: 'Participant registered successfully',
                participants: thisWeekParticipants,
                count: thisWeekParticipants.length
            });
        } else {
            res.status(500).json({
                success: false,
                error: 'Failed to save participant'
            });
        }
    } catch (error) {
        console.error('참가자 등록 에러:', error);
        res.status(500).json({
            success: false,
            error: 'Failed to register participant'
        });
    }
});

// 관리자 기능: 모든 참가자 삭제
app.delete('/api/participants', async (req, res) => {
    try {
        const { admin_key } = req.body;
        
        if (admin_key !== 'runclub2024') {
            return res.status(403).json({
                success: false,
                error: 'Unauthorized'
            });
        }
        
        await saveParticipants([]);
        console.log('🗑️ 모든 참가자 삭제됨 (관리자)');
        
        res.json({
            success: true,
            message: 'All participants cleared',
            participants: [],
            count: 0
        });
    } catch (error) {
        console.error('참가자 삭제 에러:', error);
        res.status(500).json({
            success: false,
            error: 'Failed to clear participants'
        });
    }
});

// 이벤트 설정 조회 API
app.get('/api/event-config', async (req, res) => {
    try {
        const eventConfig = await loadEventConfigFromGitHub();
        
        if (eventConfig) {
            res.json({
                success: true,
                config: eventConfig
            });
        } else {
            res.json({
                success: true,
                config: null,
                message: 'No event config found'
            });
        }
        
    } catch (error) {
        console.error('이벤트 설정 조회 에러:', error);
        res.status(500).json({
            success: false,
            error: 'Failed to load event config'
        });
    }
});

// 이벤트 설정 저장 API
app.post('/api/event-config', async (req, res) => {
    try {
        const { admin_key, config } = req.body;
        
        if (admin_key !== 'runclub2024') {
            return res.status(403).json({
                success: false,
                error: 'Unauthorized'
            });
        }
        
        if (!config) {
            return res.status(400).json({
                success: false,
                error: 'Event config is required'
            });
        }
        
        // GitHub에 이벤트 설정 저장
        try {
            await saveEventConfigToGitHub(config);
            console.log('📝 이벤트 설정 GitHub 저장 완료');
            
            res.json({
                success: true,
                message: 'Event config saved successfully'
            });
        } catch (error) {
            console.error('이벤트 설정 저장 실패:', error);
            res.status(500).json({
                success: false,
                error: 'Failed to save event config'
            });
        }
        
    } catch (error) {
        console.error('이벤트 설정 API 에러:', error);
        res.status(500).json({
            success: false,
            error: 'Failed to process event config'
        });
    }
});

// GitHub에서 이벤트 설정 로드
async function loadEventConfigFromGitHub() {
    const GITHUB_OWNER = 'ico1036';
    const GITHUB_REPO = 'jw_run';
    
    try {
        const response = await fetch(
            `https://api.github.com/repos/${GITHUB_OWNER}/${GITHUB_REPO}/contents/saturday-run-coffee-club/event-config.json`,
            {
                headers: {
                    'Accept': 'application/vnd.github.v3+json',
                    'User-Agent': 'Saturday-Run-Club'
                }
            }
        );
        
        if (!response.ok) {
            if (response.status === 404) {
                console.log('📄 GitHub에 event-config.json 파일 없음');
                return null;
            }
            throw new Error(`GitHub API 오류: ${response.status}`);
        }
        
        const fileData = await response.json();
        const content = Buffer.from(fileData.content, 'base64').toString('utf8');
        const eventConfig = JSON.parse(content);
        
        console.log(`📥 GitHub에서 이벤트 설정 로드됨: ${eventConfig.title}`);
        
        // 클라이언트에서 접근할 수 있도록 파일로 저장 (선택사항)
        // 또는 메모리에 저장해서 API로 제공
        
        return eventConfig;
        
    } catch (error) {
        console.error('GitHub 이벤트 설정 로드 실패:', error.message);
        return null;
    }
}

// GitHub에 이벤트 설정 저장
async function saveEventConfigToGitHub(config) {
    const GITHUB_TOKEN = process.env.GITHUB_TOKEN;
    const GITHUB_OWNER = 'ico1036';
    const GITHUB_REPO = 'jw_run';
    
    if (!GITHUB_TOKEN) {
        console.log('💡 GITHUB_TOKEN 환경변수가 없어 이벤트 설정 GitHub 백업 건너뜀');
        return;
    }
    
    try {
        const content = JSON.stringify(config, null, 2);
        const encodedContent = Buffer.from(content).toString('base64');
        
        // 기존 파일 SHA 가져오기
        let sha = null;
        try {
            const getResponse = await fetch(
                `https://api.github.com/repos/${GITHUB_OWNER}/${GITHUB_REPO}/contents/saturday-run-coffee-club/event-config.json`,
                {
                    headers: {
                        'Authorization': `token ${GITHUB_TOKEN}`,
                        'Accept': 'application/vnd.github.v3+json'
                    }
                }
            );
            if (getResponse.ok) {
                const fileData = await getResponse.json();
                sha = fileData.sha;
            }
        } catch (e) {
            // 파일이 없으면 새로 생성
        }
        
        // GitHub에 파일 업데이트/생성
        const updateResponse = await fetch(
            `https://api.github.com/repos/${GITHUB_OWNER}/${GITHUB_REPO}/contents/saturday-run-coffee-club/event-config.json`,
            {
                method: 'PUT',
                headers: {
                    'Authorization': `token ${GITHUB_TOKEN}`,
                    'Accept': 'application/vnd.github.v3+json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: `📝 이벤트 설정 업데이트: ${config.title} (${new Date().toISOString()})`,
                    content: encodedContent,
                    ...(sha && { sha })
                })
            }
        );
        
        if (updateResponse.ok) {
            console.log(`📝 이벤트 설정 GitHub 백업 성공: ${config.title}`);
        } else {
            throw new Error(`GitHub API 오류: ${updateResponse.status}`);
        }
        
    } catch (error) {
        throw new Error(`이벤트 설정 GitHub 백업 실패: ${error.message}`);
    }
}

// 서버 시작
async function startServer() {
    await initializeData();
    
    app.listen(PORT, () => {
        console.log('🚀 Saturday Run & Coffee Club 서버 시작!');
        console.log(`📡 서버 주소: http://localhost:${PORT}`);
        console.log(`📊 API 엔드포인트:`);
        console.log(`   GET  /api/participants - 참가자 목록 조회`);
        console.log(`   POST /api/participants - 참가자 등록`);
        console.log(`   DELETE /api/participants - 모든 참가자 삭제 (관리자)`);
        console.log(`   GET  /api/event-config - 이벤트 설정 조회`);
        console.log(`   POST /api/event-config - 이벤트 설정 저장 (관리자)`);
        console.log('🎉 준비 완료!');
    });
}

startServer().catch(console.error);


