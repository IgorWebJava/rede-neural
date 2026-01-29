import sqlite3
import json
import pickle
import os

class SovereignDBManager:
    """
    Gerenciador de Banco de Dados Soberano (RULE 01 & 09).
    V12: CRUD completo utilizando SQLite3 para garantir soberania local absoluta
    e independência de serviços externos de rede.
    """
    def __init__(self, db_path="./persistence/sovereign_storage.db"):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        try:
            return sqlite3.connect(self.db_path)
        except Exception as err:
            print(f"🚨 Erro de Conexão SQLite: {err}")
            return None

    def _init_db(self):
        """Inicializa o banco e as tabelas se não existirem."""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        conn = self._get_connection()
        if conn:
            cursor = conn.cursor()
            # 1. Tabela de Modelos
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS neural_models (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                version_tag TEXT NOT NULL,
                weights_blob BLOB NOT NULL,
                architecture_json TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )""")
            
            # 2. Tabela de Reputação
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS swarm_reputation (
                agent_id TEXT PRIMARY KEY,
                score REAL DEFAULT 1.0,
                credits REAL DEFAULT 10.0,
                total_contributions INTEGER DEFAULT 0,
                last_seen TEXT
            )""")
            
            # 3. Tabela de Logs Éticos
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS ethics_ledger (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT,
                details TEXT,
                prev_hash TEXT,
                current_hash TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )""")
            
            # 4. Tabela de Histórico de Chat
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_input TEXT,
                response TEXT,
                modality TEXT,
                explanation_json TEXT,
                prediction_val REAL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )""")
            
            conn.commit()
            conn.close()

    # --- CRUD: Modelos e Pesos ---
    def save_model(self, version_tag, weights_dict, architecture=None):
        conn = self._get_connection()
        if not conn: return
        cursor = conn.cursor()
        weights_blob = pickle.dumps(weights_dict)
        arch_json = json.dumps(architecture) if architecture else None
        
        cursor.execute("INSERT INTO neural_models (version_tag, weights_blob, architecture_json) VALUES (?, ?, ?)", 
                       (version_tag, weights_blob, arch_json))
        conn.commit()
        conn.close()
        print(f"💾 Modelo {version_tag} salvo no Banco Soberano.")

    def load_latest_model(self):
        conn = self._get_connection()
        if not conn: return None
        cursor = conn.cursor()
        cursor.execute("SELECT weights_blob FROM neural_models ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()
        conn.close()
        return pickle.loads(row[0]) if row else None

    # --- CRUD: Reputação ---
    def upsert_reputation(self, agent_id, score, credits, contributions):
        conn = self._get_connection()
        if not conn: return
        cursor = conn.cursor()
        from datetime import datetime
        now = datetime.now().isoformat()
        
        cursor.execute("""
        INSERT INTO swarm_reputation (agent_id, score, credits, total_contributions, last_seen)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(agent_id) DO UPDATE SET 
            score=excluded.score, 
            credits=excluded.credits, 
            total_contributions=excluded.total_contributions, 
            last_seen=excluded.last_seen
        """, (agent_id, score, credits, contributions, now))
        conn.commit()
        conn.close()

    # --- CRUD: Chat ---
    def add_chat_entry(self, user_input, response, modality, explanation, prediction):
        conn = self._get_connection()
        if not conn: return
        cursor = conn.cursor()
        expl_json = json.dumps(explanation)
        cursor.execute("""
        INSERT INTO chat_history (user_input, response, modality, explanation_json, prediction_val)
        VALUES (?, ?, ?, ?, ?)
        """, (user_input, response, modality, expl_json, float(prediction)))
        conn.commit()
        conn.close()

    def get_chat_history(self, limit=50):
        conn = self._get_connection()
        if not conn: return []
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM chat_history ORDER BY timestamp DESC LIMIT ?", (limit,))
        rows = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return rows
