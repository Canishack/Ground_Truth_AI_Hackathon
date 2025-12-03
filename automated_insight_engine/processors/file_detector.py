def detect_file_type(filename: str) -> str:
    """
    Return one of: 'csv', 'sql', 'db', or None.
    """
    if not filename or "." not in filename:
        return None
    ext = filename.rsplit(".", 1)[1].lower()
    if ext == "csv":
        return "csv"
    if ext == "sql":
        return "sql"
    if ext in ("db", "sqlite"):
        return "db"
    return None
