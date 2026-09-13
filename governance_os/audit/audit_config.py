from pathlib import Path


ROOT_DIR = Path(
    __file__
).resolve().parents[2]


AUDIT_DIR = ROOT_DIR / "audit_logs"


AUDIT_FILE = (
    AUDIT_DIR / "governance_audit.jsonl"
)


MAX_AUDIT_FILE_SIZE = (
    50 * 1024 * 1024
)


BACKUP_COUNT = 10