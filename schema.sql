-- AI mock interviewer Database Schema

-- Create database (uncomment if needed)
-- CREATE DATABASE ai_mock_interviewer;
-- USE ai_mock_interviewer;

-- Sessions table - stores each mock interview session
CREATE TABLE sessions (
    id VARCHAR(36) PRIMARY KEY DEFAULT (UUID()),
    domain VARCHAR(100) NOT NULL, -- e.g., "Data Scientist", "Software Engineer"
    interview_type ENUM('HR', 'Behavioral', 'Technical', 'Coding', 'All') NOT NULL DEFAULT 'All',
    resume_text TEXT, -- parsed resume content
    job_description TEXT, -- job description text
    total_score DECIMAL(3,1) NULL, -- overall session score (0-10)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Questions table - stores generated questions with predicted answers
CREATE TABLE questions (
    id VARCHAR(36) PRIMARY KEY DEFAULT (UUID()),
    session_id VARCHAR(36) NOT NULL,
    question_text TEXT NOT NULL,
    predicted_answer TEXT, -- ideal/expected answer
    question_type VARCHAR(50), -- category of question (sql, dsa, behavioural, technical, hr)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE
);

-- User answers table - stores user responses to questions
CREATE TABLE user_answers (
    id VARCHAR(36) PRIMARY KEY DEFAULT (UUID()),
    session_id VARCHAR(36) NOT NULL,
    question_id VARCHAR(36) NOT NULL,
    answer_text TEXT NOT NULL,
    time_spent_seconds INT NULL, -- time taken to answer (if tracked)
    
    FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE,
    FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE,
    UNIQUE KEY unique_session_question_answer (session_id, question_id)
);

-- Evaluations table - stores overall session evaluation
CREATE TABLE evaluations (
    id VARCHAR(36) PRIMARY KEY DEFAULT (UUID()),
    session_id VARCHAR(36) NOT NULL,
    total_score DECIMAL(3,1) NOT NULL, -- overall session score (0-10)
    overall_feedback TEXT, -- general feedback for the entire session
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE,
    UNIQUE KEY unique_session_evaluation (session_id)
);

