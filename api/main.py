import sys
from pathlib import Path
from typing import Literal
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from api.compiler import compilar_codigo
from api.tokens import obtener_tokens
from backend.reportes.simbolos_html import REPORTES
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

app = FastAPI(title="OxigenNative API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets" / "ast"
ASSETS_DIR.mkdir(parents=True, exist_ok=True)

app.mount("/api/ast", StaticFiles(directory=str(ASSETS_DIR)), name="ast_images")
REPORTES.mkdir(parents=True, exist_ok=True)
app.mount("/api/reportes", StaticFiles(directory=str(REPORTES)), name="reportes")

class CompileRequest(BaseModel):
    code: str
    mode: Literal["arm64", "interprete"] = "arm64"

class TokenRequest(BaseModel):
    code: str

@app.post("/api/compile")
def compile_code(req: CompileRequest):
    return compilar_codigo(req.code, req.mode)

@app.post("/api/tokens")
def get_tokens(req: TokenRequest):
    return {"tokens": obtener_tokens(req.code)}

@app.get("/api/ast/{filename}")
def get_ast_image(filename: str):
    file_path = ASSETS_DIR / filename
    if file_path.exists():
        return FileResponse(str(file_path), media_type="image/png")
    return {"error": "Image not found"}
