
import React, { useState, useEffect } from 'react';
import questionsData from './data/questions.json';

const Intro = ({ onStart }) => (
  <div className="container fade-in">
    <div className="glass-card" style={{ padding: '4rem', textAlign: 'center', marginTop: '5vh', position: 'relative' }}>

      {/* Cheering Image and Bubble */}
      <div style={{ position: 'relative', display: 'inline-block', marginBottom: '2rem' }}>
        <div style={{
          position: 'absolute',
          top: '-20px',
          right: '-110px',
          background: 'white',
          color: '#1e293b',
          padding: '12px 24px',
          borderRadius: '20px',
          fontWeight: 'bold',
          fontSize: '1.2rem',
          boxShadow: '0 8px 25px rgba(0,0,0,0.3)',
          zIndex: 10,
          animation: 'bounce-custom 2s infinite',
          whiteSpace: 'nowrap'
        }}>
          영지 화이팅!! 💙
          <div style={{
            content: '""',
            position: 'absolute',
            bottom: '-12px',
            left: '30px',
            borderWidth: '12px 12px 0',
            borderStyle: 'solid',
            borderColor: 'white transparent transparent',
            display: 'block',
            width: 0
          }}></div>
        </div>

        <div style={{
          width: '160px',
          height: '160px',
          borderRadius: '50%',
          overflow: 'hidden',
          border: '5px solid var(--primary)',
          boxShadow: '0 0 25px rgba(99, 102, 241, 0.6)',
          background: '#e2e8f0',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center'
        }}>
          <img src="/cheer.png" alt="Cheer" style={{
            width: '100%',
            height: '100%',
            objectFit: 'cover',
            objectPosition: 'center 10%' // focuses towards top to capture face
          }} onError={(e) => {
            e.target.style.display = 'none';
            e.target.parentElement.innerHTML = '<div style="font-size:4rem;">🏃‍♂️</div>';
          }} />
        </div>
      </div>

      <h1 style={{ fontSize: '3rem', marginBottom: '1rem', background: 'linear-gradient(135deg, #fff, #94a3b8)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', lineHeight: '1.2' }}>
        효진쌤의 <br />간호조무사 CBT 실전모의고사 💉
      </h1>
      <p style={{ color: 'var(--text-dim)', marginBottom: '3rem', fontSize: '1.2rem' }}>
        30년 경력의 베테랑이 엄선한 2025 최신 트렌드 반영 문항! <br />
        실전과 동일하게 105문제가 랜덤하게 출제됩니다. ✨
      </p>
      <button className="btn-primary" style={{ fontSize: '1.5rem', padding: '1.2rem 3rem' }} onClick={onStart}>
        시험 시작하기 🚀
      </button>
    </div>
  </div>
);

const CBTExam = ({ questions, onFinish }) => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [selectedAnswers, setSelectedAnswers] = useState({});
  const [showFeedback, setShowFeedback] = useState(false);
  const [wrongNotes, setWrongNotes] = useState([]);
  const [timeLeft, setTimeLeft] = useState(60); // 1 minute per question
  const [showDrawer, setShowDrawer] = useState(false); // Mobile drawer state

  useEffect(() => {
    if (showFeedback) return;

    const timer = setInterval(() => {
      setTimeLeft(prev => {
        if (prev <= 1) {
          clearInterval(timer);
          handleTimeOut();
          return 0;
        }
        return prev - 1;
      });
    }, 1000);
    return () => clearInterval(timer);
  }, [showFeedback, currentIndex]);

  const handleTimeOut = () => {
    if (!showFeedback) {
      handleSelect(-1); // -1 signifies a timeout
    }
  };

  const currentQ = questions[currentIndex];

  const handleSelect = (choiceIdx) => {
    if (showFeedback) return;

    const isCorrect = choiceIdx === currentQ.answer;
    setSelectedAnswers({ ...selectedAnswers, [currentIndex]: choiceIdx });
    setShowFeedback(true);

    if (!isCorrect) {
      setWrongNotes(prev => {
        if (!prev.includes(currentQ.id)) return [...prev, currentQ.id];
        return prev;
      });
    }
  };

  const nextQuestion = () => {
    if (currentIndex < questions.length - 1) {
      setCurrentIndex(currentIndex + 1);
      setShowFeedback(false);
      setTimeLeft(60);
    } else {
      onFinish(selectedAnswers, wrongNotes);
    }
  };

  const formatTime = (seconds) => {
    const m = Math.floor(seconds / 60);
    const s = seconds % 60;
    return `${m}:${s < 10 ? '0' : ''}${s}`;
  };

  return (
    <div className="container fade-in" style={{ padding: '1rem' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
        <h2 style={{ color: 'var(--secondary)' }}>CBT 실전 모의고사 📝</h2>
        <div style={{ display: 'flex', gap: '0.5rem' }}>
          <button className="btn-secondary" onClick={() => setShowDrawer(!showDrawer)}>
            {showDrawer ? '닫기 ✖️' : '문항보기 📋'}
          </button>
        </div>
      </div>

      <div className={`cbt-layout ${showDrawer ? 'drawer-open' : ''}`}>
        <div className={`nav-panel glass-card ${showDrawer ? 'visible' : ''}`}>
          <h3 style={{ marginBottom: '1rem' }}>문항 탐색기</h3>
          <div className="nav-grid">
            {questions.map((_, idx) => (
              <button
                key={idx}
                className={`nav-item ${currentIndex === idx ? 'active' : ''} ${selectedAnswers[idx] !== undefined ? 'solved' : ''}`}
                onClick={() => { setCurrentIndex(idx); setShowFeedback(false); setShowDrawer(false); setTimeLeft(60); }}
              >
                {idx + 1}
              </button>
            ))}
          </div>
        </div>

        <div className="question-area glass-card">
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '1rem', color: 'var(--text-dim)', fontSize: '0.9rem' }}>
            <span>{currentQ.category} | {currentIndex + 1} / {questions.length}</span>
            <span style={{ color: timeLeft <= 10 ? '#ef4444' : 'var(--text-dim)', fontWeight: 'bold' }}>
              남은 시간: {timeLeft}초
            </span>
          </div>
          <h2 style={{ fontSize: '1.5rem', lineHeight: '1.4', marginBottom: '1.5rem' }}>
            {currentQ.question}
          </h2>

          <div className="choices-list">
            {currentQ.choices.map((choice, idx) => (
              <button
                key={idx}
                className={`choice-btn ${selectedAnswers[currentIndex] === idx + 1 ? 'selected' : ''}`}
                onClick={() => handleSelect(idx + 1)}
              >
                {choice}
              </button>
            ))}
          </div>

          {showFeedback && (
            <div className={`feedback ${selectedAnswers[currentIndex] === currentQ.answer ? 'correct' : 'wrong'}`}>
              <h3 style={{ marginBottom: '0.8rem' }}>
                {selectedAnswers[currentIndex] === currentQ.answer
                  ? '✅ 정답입니다!'
                  : selectedAnswers[currentIndex] === -1
                    ? '⏰ 시간 초과!'
                    : '❌ 아쉬워요!'}
              </h3>
              <div style={{ marginBottom: '1.5rem', padding: '1rem', background: 'rgba(255, 255, 255, 0.05)', borderRadius: '12px', border: '1px solid var(--glass-border)' }}>
                <p style={{ fontSize: '1.1rem', marginBottom: '0.5rem' }}>
                  <strong>🎯 정답: {currentQ.choices[currentQ.answer - 1]}</strong>
                </p>
                <p style={{ color: 'var(--text-dim)', lineHeight: '1.5' }}>{currentQ.explanation}</p>
              </div>
              <div style={{ background: 'rgba(99, 102, 241, 0.1)', padding: '1rem', borderRadius: '12px', borderLeft: '5px solid var(--primary)' }}>
                <strong>💡 효진쌤의 암기 비법:</strong> {currentQ.tip}
              </div>
              <button className="btn-primary" style={{ marginTop: '1.5rem', width: '100%' }} onClick={nextQuestion}>
                {currentIndex === questions.length - 1 ? '결과 확인하기' : '다음 문제로'}
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

const Result = ({ score, total, wrongQuestions, onRestart, onReviewWrong }) => {
  const percentage = Math.round((score / total) * 100);
  const isPass = percentage >= 60;

  return (
    <div className="container fade-in">
      <div className="glass-card" style={{ padding: '3rem', textAlign: 'center' }}>
        <h1 style={{ fontSize: '3rem', marginBottom: '1rem' }}>
          {isPass ? '축하합니다! 합격 🎊' : '조금 더 힘내봐요! 불합격 😭'}
        </h1>
        <div style={{ fontSize: '5rem', fontWeight: 'bold', color: isPass ? '#22c55e' : '#ef4444', margin: '2rem 0' }}>
          {score} / {total} 점
        </div>
        <p style={{ color: 'var(--text-dim)', fontSize: '1.2rem', marginBottom: '3rem' }}>
          정답률: {percentage}% (60% 이상 합격)
        </p>

        <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center' }}>
          <button className="btn-primary" onClick={onRestart}>다시 도전하기 🔄️</button>
          {wrongQuestions.length > 0 && (
            <button className="btn-primary" style={{ background: 'var(--secondary)' }} onClick={onReviewWrong}>
              틀린 문제만 다시 풀기 📖 ({wrongQuestions.length}문항)
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

function App() {
  const [mode, setMode] = useState('intro');
  const [activeQuestions, setActiveQuestions] = useState([]);
  const [finalScore, setFinalScore] = useState(0);
  const [wrongNoteIds, setWrongNoteIds] = useState([]);

  const startNewExam = () => {
    // 전체 문제 DB를 복사합니다.
    const pool = [...questionsData];

    // 피셔-예이츠(Fisher-Yates) 셔플 알고리즘으로 완벽한 무작위 섞기 수행
    for (let i = pool.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [pool[i], pool[j]] = [pool[j], pool[i]];
    }

    // 가장 앞의 105문제를 추출하여 모의고사 생성 (중복 절대 없음)
    const shuffled = pool.slice(0, 105);

    setActiveQuestions(shuffled);
    setMode('quiz');
    setFinalScore(0);
    setWrongNoteIds([]);
  };

  const finishExam = (answers, wrongIds) => {
    let score = 0;
    activeQuestions.forEach((q, idx) => {
      if (answers[idx] === q.answer) score++;
    });
    setFinalScore(score);
    setWrongNoteIds(wrongIds);
    setMode('result');
  };

  const startWrongReview = () => {
    const wrongQ = questionsData.filter(q => wrongNoteIds.includes(q.id));
    setActiveQuestions(wrongQ);
    setMode('quiz');
  };

  return (
    <div className="App">
      {mode === 'intro' && <Intro onStart={startNewExam} />}
      {mode === 'quiz' && <CBTExam questions={activeQuestions} onFinish={finishExam} />}
      {mode === 'result' && (
        <Result
          score={finalScore}
          total={activeQuestions.length}
          wrongQuestions={wrongNoteIds}
          onRestart={startNewExam}
          onReviewWrong={startWrongReview}
        />
      )}
    </div>
  );
}

export default App;
