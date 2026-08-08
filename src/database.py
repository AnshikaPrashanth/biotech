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
    notes TEXT
);
'''

class SQLiteSessionDB:
    """SQLite database storing patient rehabilitation sessions and computing recovery metrics."""

    def __init__(self, db_path: str = 'rehab_sessions.db'):
        self.db_path = Path(db_path)
        self.connection = sqlite3.connect(str(self.db_path), check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
        self._create_tables()

    def _create_tables(self) -> None:
        with self.connection:
            self.connection.executescript(DB_SCHEMA)

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
    ) -> int:
        attention_json = json.dumps(attention_map)
        rom_deviation_json = json.dumps(rom_deviation) if rom_deviation is not None else '{}'
        timestamp = datetime.now(timezone.utc).isoformat()
        with self.connection:
            cursor = self.connection.execute(
                '''INSERT INTO sessions 
                   (timestamp, subject_id, exercise_type, confidence, verdict, attention_json, rom_deviation_json, session_duration, notes) 
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (timestamp, subject_id, exercise_type, confidence, verdict, attention_json, rom_deviation_json, session_duration, notes),
            )
        return cursor.lastrowid

    def get_weekly_trends(self, subject_id: Optional[str] = None) -> List[Dict[str, object]]:
        """Averages confidence scores grouped by week."""
        query = '''
        SELECT 
            strftime('%Y-%W', timestamp) AS week,
            AVG(confidence) AS average_confidence,
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
        """Averages confidence scores grouped by month."""
        query = '''
        SELECT 
            strftime('%Y-%m', timestamp) AS month,
            AVG(confidence) AS average_confidence,
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
        """Calculates the progress score difference between initial and latest sessions."""
        query = '''
        SELECT confidence, timestamp FROM sessions
        WHERE subject_id = ?
        ORDER BY timestamp ASC
        '''
        cursor = self.connection.execute(query, [subject_id])
        rows = cursor.fetchall()
        if len(rows) < 2:
            return {'improvement': 0.0, 'sessions_tracked': len(rows)}
        
        initial_confidence = rows[0]['confidence']
        latest_confidence = rows[-1]['confidence']
        improvement = latest_confidence - initial_confidence
        return {
            'initial_confidence': initial_confidence,
            'latest_confidence': latest_confidence,
            'improvement': float(improvement),
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
