import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

DB_SCHEMA = '''
CREATE TABLE IF NOT EXISTS sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    subject_id TEXT NOT NULL,
    exercise_type TEXT NOT NULL,
    confidence REAL NOT NULL,
    verdict TEXT NOT NULL,
    attention_json TEXT NOT NULL,
    rom_deviation_json TEXT,
    session_duration REAL DEFAULT 0.0,
    notes TEXT,
    movement_quality REAL,
    uncertainty REAL,
    decision_status TEXT,
    rom_score REAL,
    symmetry_score REAL,
    top_error_joints TEXT,
    repetition_stats TEXT
);
'''

class SQLiteSessionDB:
    """SQLite database storing patient rehabilitation sessions and computing recovery metrics."""

    def __init__(self, db_path: str = 'rehab_sessions.db'):
        self.db_path = Path(db_path)
        self.connection = sqlite3.connect(str(self.db_path), check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
        self._create_tables()
        self._run_migrations()

    def _create_tables(self) -> None:
        with self.connection:
            self.connection.executescript(DB_SCHEMA)

    def _run_migrations(self) -> None:
        """Checks if database contains new schema columns, adding them dynamically if missing."""
        cursor = self.connection.cursor()
        cursor.execute("PRAGMA table_info(sessions)")
        columns = [row['name'] for row in cursor.fetchall()]
        
        # New columns to add if they do not exist
        new_cols = {
            'movement_quality': 'REAL',
            'uncertainty': 'REAL',
            'decision_status': 'TEXT',
            'rom_score': 'REAL',
            'symmetry_score': 'REAL',
            'top_error_joints': 'TEXT',
            'repetition_stats': 'TEXT'
        }
        
        for col_name, col_type in new_cols.items():
            if col_name not in columns:
                try:
                    with self.connection:
                        self.connection.execute(f"ALTER TABLE sessions ADD COLUMN {col_name} {col_type};")
                except sqlite3.OperationalError as e:
                    # Column might have been added in parallel thread/session
                    pass

    def log_session(
        self,
        subject_id: str,
        exercise_type: str,
        confidence: float,
        verdict: str,
        attention_map: Dict[str, float],
        rom_deviation: Optional[Dict[str, float]] = None,
        session_duration: float = 0.0,
        notes: Optional[str] = None,
        movement_quality: Optional[float] = None,
        uncertainty: Optional[float] = None,
        rom_score: Optional[float] = None,
        symmetry_score: Optional[float] = None,
        top_error_joints: Optional[List] = None,
        repetition_stats: Optional[Dict] = None
    ) -> int:
        attention_json = json.dumps(attention_map)
        rom_deviation_json = json.dumps(rom_deviation) if rom_deviation is not None else '{}'
        top_err_json = json.dumps(top_error_joints) if top_error_joints is not None else '[]'
        rep_stats_json = json.dumps(repetition_stats) if repetition_stats is not None else '{}'
        timestamp = datetime.now(timezone.utc).isoformat()
        
        # decision_status falls back to verdict
        decision_status = verdict if verdict in ["Healthy", "Compensated", "Uncertain / Human Review"] else verdict
        
        with self.connection:
            cursor = self.connection.execute(
                '''INSERT INTO sessions 
                   (timestamp, subject_id, exercise_type, confidence, verdict, attention_json, rom_deviation_json, 
                    session_duration, notes, movement_quality, uncertainty, decision_status, rom_score, symmetry_score, 
                    top_error_joints, repetition_stats) 
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (timestamp, subject_id, exercise_type, confidence, verdict, attention_json, rom_deviation_json,
                 session_duration, notes, movement_quality, uncertainty, decision_status, rom_score, symmetry_score,
                 top_err_json, rep_stats_json),
            )
        return cursor.lastrowid

    def get_weekly_trends(self, subject_id: Optional[str] = None) -> List[Dict[str, object]]:
        """Averages movement quality scores grouped by week."""
        query = '''
        SELECT 
            strftime('%Y-%W', timestamp) AS week,
            AVG(COALESCE(movement_quality, confidence * 100)) AS average_confidence,
            COUNT(*) AS sessions
        FROM sessions
        '''
        params = []
        if subject_id:
            query += ' WHERE subject_id = ?\n'
            params.append(subject_id)
        query += ' GROUP BY week ORDER BY week ASC LIMIT 12;'
        
        cursor = self.connection.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]

    def get_monthly_trends(self, subject_id: Optional[str] = None) -> List[Dict[str, object]]:
        """Averages movement quality scores grouped by month."""
        query = '''
        SELECT 
            strftime('%Y-%m', timestamp) AS month,
            AVG(COALESCE(movement_quality, confidence * 100)) AS average_confidence,
            COUNT(*) AS sessions
        FROM sessions
        '''
        params = []
        if subject_id:
            query += ' WHERE subject_id = ?\n'
            params.append(subject_id)
        query += ' GROUP BY month ORDER BY month ASC LIMIT 12;'
        
        cursor = self.connection.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]

    def get_exercise_adherence(self, subject_id: Optional[str] = None) -> List[Dict[str, object]]:
        """Tracks the frequency of exercises performed by the subject."""
        query = '''
        SELECT 
            exercise_type,
            COUNT(*) as session_count,
            SUM(session_duration) as total_duration
        FROM sessions
        '''
        params = []
        if subject_id:
            query += ' WHERE subject_id = ?\n'
            params.append(subject_id)
        query += ' GROUP BY exercise_type ORDER BY session_count DESC;'
        
        cursor = self.connection.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]

    def get_best_improvement(self, subject_id: str) -> Dict[str, object]:
        """Calculates the movement quality difference between initial and latest sessions."""
        query = '''
        SELECT COALESCE(movement_quality, confidence * 100) AS quality, timestamp FROM sessions
        WHERE subject_id = ?
        ORDER BY timestamp ASC
        '''
        cursor = self.connection.execute(query, [subject_id])
        rows = cursor.fetchall()
        if len(rows) < 2:
            return {'improvement': 0.0, 'sessions_tracked': len(rows)}
        
        initial_val = rows[0]['quality']
        latest_val = rows[-1]['quality']
        improvement = latest_val - initial_val
        return {
            'initial_confidence': initial_val / 100.0,
            'latest_confidence': latest_val / 100.0,
            'improvement': float(improvement / 100.0),
            'sessions_tracked': len(rows)
        }

    def fetch_latest(self, limit: int = 10) -> List[Dict[str, object]]:
        cursor = self.connection.execute(
            'SELECT * FROM sessions ORDER BY timestamp DESC LIMIT ?',
            (limit,),
        )
        return [dict(row) for row in cursor.fetchall()]

    def close(self) -> None:
        self.connection.close()
