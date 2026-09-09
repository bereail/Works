from pathlib import Path

from fastapi.templating import Jinja2Templates

DIR_TEMPLATES = Path(__file__).resolve().parent / "templates"
templates = Jinja2Templates(directory=str(DIR_TEMPLATES))
