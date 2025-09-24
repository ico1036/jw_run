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

// 참가자 데이터 초기화
async function initializeData() {
    try {
        await fs.access(DATA_FILE);
    } catch (error) {
        // 파일이 없으면 빈 배열로 초기화
        await fs.writeFile(DATA_FILE, JSON.stringify([], null, 2));
        console.log('📄 participants.json 초기화 완료');
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

// 참가자 데이터 저장
async function saveParticipants(participants) {
    try {
        await fs.writeFile(DATA_FILE, JSON.stringify(participants, null, 2));
        return true;
    } catch (error) {
        console.error('데이터 저장 에러:', error);
        return false;
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
        console.log('🎉 준비 완료!');
    });
}

startServer().catch(console.error);
