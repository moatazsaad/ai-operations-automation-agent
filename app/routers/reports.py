# Serves generated report files (PDF/Markdown) so the browser can display or
# download them. build_operations_report()/build_sales_report() only write
# files to disk - nothing served them over HTTP until this router.
import re
from pathlib import Path
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

router = APIRouter(prefix="/reports", tags=["reports"])

REPORTS_DIR = Path("reports").resolve()

# Only lets through plain filenames like "weekly_operations_report_2026-08-07_23-07-19.pdf" -
# no slashes or ".." allowed, so this can't be used to read arbitrary files on the server.
FILENAME_PATTERN = re.compile(r"^[\w\-]+\.(pdf|md)$")


@router.get("/{filename}")
def get_report_file(filename: str):
    if not FILENAME_PATTERN.match(filename):
        raise HTTPException(status_code=400, detail="Invalid report filename")

    file_path = (REPORTS_DIR / filename).resolve()

    # Belt-and-suspenders check alongside the regex: the resolved path must
    # still be inside the reports directory.
    if not file_path.is_relative_to(REPORTS_DIR) or not file_path.is_file():
        raise HTTPException(status_code=404, detail="Report not found")

    media_type = "application/pdf" if filename.endswith(".pdf") else "text/markdown"
    return FileResponse(file_path, media_type=media_type)
