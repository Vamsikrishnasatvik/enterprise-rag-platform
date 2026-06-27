from pathlib import Path
import uuid

UPLOAD_DIR = Path("app/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def save_uploaded_file(file) -> str:
    file_extension = Path(file.filename).suffix
    filename = f"{uuid.uuid4()}{file_extension}"

    file_path = UPLOAD_DIR / filename

    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    return str(file_path)