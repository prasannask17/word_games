from fastapi import FastAPI, Form
from fastapi.responses import Response, HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import tempfile, os, uuid
from word_games_book import build, THEMES, SECTIONS_META
from themes import auto_theme

app = FastAPI(title="Word Games Book Generator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


@app.get("/", response_class=HTMLResponse)
async def index():
    with open(os.path.join(BASE_DIR, "frontend.html")) as f:
        return f.read()


@app.get("/api/themes")
async def get_themes():
    return {
        "themes": [
            {"key": k, "name": v["name"], "tagline": v["tagline"], "palette": v["palette"]}
            for k, v in THEMES.items()
        ]
    }


@app.get("/api/games")
async def get_games():
    """Return all available game/puzzle types with metadata."""
    return {"games": SECTIONS_META}


@app.post("/api/generate")
async def generate(
    theme: str = Form(...),
    scale: float = Form(1.0),
    games: Optional[str] = Form(None),   # comma-separated keys, e.g. "anagram,wordsearch,riddle"
):
    theme = theme.strip()
    if not theme:
        return JSONResponse({"error": "Theme is required."}, status_code=400)

    # Parse selected game keys
    selected_keys = None
    if games and games.strip():
        selected_keys = [g.strip() for g in games.split(",") if g.strip()]

    # Use preset if matches, else auto-generate
    theme_key = theme if theme in THEMES else None
    if theme_key is None:
        theme_key = f"_auto_{uuid.uuid4().hex[:8]}"
        THEMES[theme_key] = auto_theme(theme)

    safe_name = THEMES[theme_key]["name"]
    tmpdir   = tempfile.mkdtemp()
    out_path = os.path.join(tmpdir, f"Word_Games_{safe_name}.pdf")

    try:
        build(theme_key, scale, out_path, selected_keys=selected_keys)
        with open(out_path, "rb") as f:
            pdf_bytes = f.read()
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'attachment; filename="Word_Games_{safe_name}.pdf"',
                "Content-Length": str(len(pdf_bytes)),
            },
        )
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
    finally:
        import shutil
        shutil.rmtree(tmpdir, ignore_errors=True)
        if theme_key.startswith("_auto_"):
            THEMES.pop(theme_key, None)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
