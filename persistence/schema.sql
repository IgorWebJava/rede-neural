-- Esquema de Banco de Dados Soberano V12
CREATE DATABASE IF NOT EXISTS sovereign_neural_db;
USE sovereign_neural_db;

-- Tabela de Modelos e Pesos
CREATE TABLE IF NOT EXISTS neural_models (
    id INT AUTO_INCREMENT PRIMARY KEY,
    version_tag VARCHAR(50) NOT NULL,
    weights_blob LONGBLOB NOT NULL,
    architecture_json JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Reputação de Enxame
CREATE TABLE IF NOT EXISTS swarm_reputation (
    agent_id VARCHAR(100) PRIMARY KEY,
    score FLOAT DEFAULT 1.0,
    credits FLOAT DEFAULT 10.0,
    total_contributions INT DEFAULT 0,
    last_seen DATETIME
);

-- Tabela de Logs Éticos (Ledger)
CREATE TABLE IF NOT EXISTS ethics_ledger (
    id INT AUTO_INCREMENT PRIMARY KEY,
    event_type VARCHAR(50),
    details JSON,
    prev_hash VARCHAR(64),
    current_hash VARCHAR(64),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Histórico de Chat
CREATE TABLE IF NOT EXISTS chat_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_input TEXT,
    response TEXT,
    modality VARCHAR(20),
    explanation_json JSON,
    prediction_val FLOAT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
