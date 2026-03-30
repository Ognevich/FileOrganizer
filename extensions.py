IMAGES = (
    ".png", ".jpg", ".jpeg", ".jpe", ".jfif",
    ".webp", ".gif", ".svg",
    ".bmp", ".dib",
    ".tiff", ".tif",
    ".ico",
    ".heic", ".heif",
    ".avif",
    ".raw", ".arw", ".cr2", ".nef", ".orf", ".sr2"
)
TEXT = (
    ".txt", ".md", ".rst",
    ".log", ".ini", ".cfg", ".conf",
    ".csv", ".tsv"
)
CODE = (
    ".py", ".js", ".ts", ".cpp", ".c", ".h", ".hpp",
    ".java", ".cs", ".go", ".rs",
    ".html", ".css", ".scss",
    ".json", ".xml", ".yaml", ".yml",
    ".sql", ".sh", ".bat", ".ps1"
)
EXECUTABLES = (
    ".exe", ".msi", ".bat", ".cmd",
    ".sh", ".bin", ".run",
    ".apk", ".appimage"
)
ARCHIVES = (
    ".zip", ".rar", ".7z", ".tar",
    ".gz", ".bz2", ".xz",
    ".tar.gz", ".tar.bz2"
)
AUDIO = (
    ".mp3", ".wav", ".flac",
    ".aac", ".ogg", ".wma", ".m4a"
)
VIDEO = (
    ".mp4", ".mkv", ".avi",
    ".mov", ".wmv", ".flv",
    ".webm", ".m4v"
)
DOCUMENTS = (
    ".pdf", ".doc", ".docx",
    ".xls", ".xlsx",
    ".ppt", ".pptx",
    ".odt", ".ods", ".odp"
)
CATEGORIES = {
    "images": IMAGES,
    "text": TEXT,
    "code": CODE,
    "executables": EXECUTABLES,
    "archives": ARCHIVES,
    "audio": AUDIO,
    "video": VIDEO,
    "documents": DOCUMENTS,
}
