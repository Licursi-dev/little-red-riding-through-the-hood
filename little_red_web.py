# PART 1/2 — little_red_web.py
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from html import escape

from little_red_engine import new_game_state, step

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# one simple in-memory game state (fine for your local project)
STATE = new_game_state()


CSS = """
@import url("https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap");

:root{
  --bg1:#070a1a;
  --bg2:#2a0b3f;
  --panel:#0b0f22cc;
  --neon:#ff2bd6;
  --cyan:#2dfcff;
  --text:#f6f3ff;
  --muted:#b9b3d6;

  /* arcade accent */
  --arcade:#FFD93B;      /* retro yellow */
  --arcadeShadow:#D62828;/* retro red */
}

*{ box-sizing:border-box; }

body{
  margin:0;
  min-height:100vh;
  font-family:"Press Start 2P", system-ui, sans-serif;
  color:var(--text);
  background:
    radial-gradient(1200px 600px at 50% 20%, rgba(45,252,255,.14), transparent 60%),
    radial-gradient(900px 500px at 30% 80%, rgba(255,43,214,.12), transparent 60%),
    linear-gradient(180deg, var(--bg1), var(--bg2));
}

.bg-grid{
  position:fixed; inset:0;
  background-image:
    linear-gradient(rgba(45,252,255,.07) 1px, transparent 1px),
    linear-gradient(90deg, rgba(45,252,255,.07) 1px, transparent 1px);
  background-size: 56px 56px;
  mask-image: radial-gradient(circle at 50% 25%, rgba(0,0,0,.9), transparent 70%);
  pointer-events:none;
}

.wrap{
  max-width: 920px;
  margin: 26px auto;
  padding: 0 16px 40px;
}

.header{
  display:flex;
  align-items:flex-end;
  justify-content:space-between;
  gap:12px;
  margin-bottom:14px;
}

h1{
  margin:0;
  font-size: 18px;
  letter-spacing: 0px;
  color: var(--arcade);
  text-shadow:
    3px 3px 0 var(--arcadeShadow),
    0 0 10px rgba(255,217,59,.18);
}

.sub{
  font-size:10px;
  color:var(--muted);
  text-align:right;
  line-height:1.55;
}

/* NEW: make the Instructions link look like a little arcade pill */
.instructions-link{
  display:inline-block;
  margin-top:8px;
  padding:8px 10px;
  border-radius:999px;
  border:1px solid rgba(255,217,59,.55);
  background:rgba(255,217,59,.08);
  color: var(--arcade);
  text-decoration:none;
}
.instructions-link:hover{
  box-shadow: 0 0 16px rgba(255,217,59,.12);
  text-decoration:none;
}

.hud{
  display:flex;
  flex-wrap:wrap;
  gap:10px;
  align-items:center;
  justify-content:space-between;
  margin: 10px 0 12px;
  color: var(--muted);
  font-size: 10px;
}

.hud .pill{
  padding: 8px 10px;
  border-radius: 999px;
  border: 1px solid rgba(255,255,255,.14);
  background: rgba(255,255,255,.04);
}

.hud strong{ color: var(--text); font-weight: 400; }

.crt{
  position:relative;
  background: var(--panel);
  border: 2px solid rgba(45,252,255,.33);
  border-radius: 18px;
  box-shadow:
    0 0 0 2px rgba(255,43,214,.10),
    0 0 36px rgba(45,252,255,.14);
  overflow:hidden;
  padding: 18px;
}

.crt::before{ /* scanlines - reduced */
  content:"";
  position:absolute; inset:0;
  background: repeating-linear-gradient(
    to bottom,
    rgba(255,255,255,.03),
    rgba(255,255,255,.03) 1px,
    rgba(0,0,0,0) 5px,
    rgba(0,0,0,0) 10px
  );
  pointer-events:none;
  mix-blend-mode: overlay;
  opacity:.38;
}

.crt::after{ /* vignette */
  content:"";
  position:absolute; inset:-20%;
  background:
    radial-gradient(circle at 50% 35%, rgba(255,43,214,.08), transparent 55%),
    radial-gradient(circle at 50% 50%, rgba(0,0,0,.55), transparent 60%);
  pointer-events:none;
}

.story{
  position:relative;
  margin:0;
  white-space:pre-wrap;
  line-height: 1.85;
  font-size: 15px;
  color: var(--text);
  text-shadow: none; /* remove “shine/glint” */
}

.choices{
  margin-top: 14px;
  display:flex;
  flex-direction:column;
  gap:10px;
}

.choice-btn{
  width:100%;
  text-align:left;
  border: 1px solid rgba(255,255,255,.16);
  background: rgba(255,255,255,.05);
  color: var(--arcade);
  padding: 14px 14px;
  border-radius: 14px;
  cursor:pointer;
  font-family: inherit;
  font-size: 11px;
  transition: transform .06s ease, box-shadow .12s ease, background .12s ease, border-color .12s ease;
}

  .choice-btn:hover{
  transform: scale(1.03);
  border-color: rgba(45,252,255,.9);   /* CYAN border */
  box-shadow: 0 0 18px rgba(45,252,255,.35);
  background: rgba(255,217,59,.08);
}

.choice-btn:focus{
  outline:none;
  border-color: rgba(255,43,214,.55);
  box-shadow: 0 0 0 3px rgba(255,43,214,.18);
}

.choice-btn:active{
  transform: translateY(1px);
}

.footer-row{
  margin-top: 14px;
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:12px;
}

.reset-btn{
  border: 1px solid rgba(255,43,214,.45);
  background: rgba(255,43,214,.10);
  color: var(--text);
  padding: 10px 12px;
  border-radius: 12px;
  cursor:pointer;
  font-family: inherit;
  font-size: 10px;
}

.reset-btn:hover{
  box-shadow: 0 0 16px rgba(255,43,214,.14);
}

.credit{
  font-size:10px;
  color: var(--muted);
}

.maker-stamp{
  position:fixed;
  right:18px;
  bottom:14px;
  font-size:12px;
  color: rgba(255,217,59,.95);
  padding:10px 12px;
  border:1px solid rgba(255,217,59,.55);
  border-radius:12px;
  background:rgba(10,10,20,.50);
  box-shadow: 0 0 16px rgba(255,217,59,.14);
  text-transform:lowercase;
  letter-spacing:1px;
}

a, a:visited { color: var(--cyan); text-decoration:none; }
a:hover { text-decoration:underline; }

.hint{
  margin-top: 10px;
  color: rgba(185,179,214,.9);
  font-size: 9px;
  line-height: 1.5;
}

.character{
  position: fixed;
  bottom: 20px;
  left: 20px;
  z-index: 10;
}

.character img{
  width: 160px;
  image-rendering: pixelated;
}

@keyframes idleSwap {
  0%   { content: url("/static/stand.png"); }
  50%  { content: url("/static/walk.png"); }
  100% { content: url("/static/stand.png"); }
}

#little-red.animate{
  animation: idleSwap 1s infinite;
}

"""
# PART 2/2 — little_red_web.py (continued)
def _hearts(lives: int) -> str:
    return "❤️ " * max(0, int(lives))


def page(state, text: str, choices: list[str]) -> str:
    safe_text = escape(text)

    lives = int(state.get("lives", 0))
    inv = state.get("inventory", []) or []
    loc = state.get("location", "unknown")

    safe_loc = escape(str(loc))
    safe_inv_count = escape(str(len(inv)))

    buttons = []
    for i, c in enumerate(choices):
        safe_choice = escape(c)
        label = f"<span style='font-size:17px; letter-spacing:0.5px'>{i+1}. {safe_choice}</span>" if i < 9 else safe_choice

        buttons.append(
            f"""
            <form method="post" action="/choose" class="choice-form">
                <input type="hidden" name="choice" value="{i}">
                <button class="choice-btn" type="submit" data-choice="{i}">{label}</button>
            </form>
            """
        )

    return f"""
    <html>
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Little Red</title>
        <style>{CSS}</style>
      </head>
      <body>
        <div class="bg-grid"></div>

        <div class="wrap">
          <div class="header">
            <h1>Little Red Riding Through the Hood</h1>
            <div class="sub">
              Retro Prototype<br>
              Built by <a href="https://licursi.dev" target="_blank" rel="noreferrer">licursi.dev</a><br>
              <a class="instructions-link" href="/instructions">Instructions</a>
            </div>
          </div>

          <div class="hud">
            <div class="pill">Lives: <strong>{escape(_hearts(lives).strip() or "0")}</strong></div>
            <div class="pill">Inventory: <strong>{safe_inv_count}</strong></div>
            <div class="pill">Location: <strong>{safe_loc}</strong></div>
          </div>

          <div class="crt">
            <pre class="story">{safe_text}</pre>

            <div class="choices">
              {''.join(buttons)}
            </div>

            <div class="footer-row">
              <form method="post" action="/reset">
                <button class="reset-btn" type="submit">Reset game</button>
              </form>
              <div class="credit">© {escape("licursi.dev")} — Little Red Prototype</div>
            </div>

            <div class="hint">
              Keys: 1–9 choose • R reset<br>
              Test tip: try at least one wrong choice to confirm life loss works.
            </div>
      
          </div>
          <div class="character">
           <img src="/static/stand.png" id="little-red" class="animate">
           </div>
        </div>

        <div class="maker-stamp">licursi.dev</div>

        <script>
          // Keyboard controls:
          // 1-9 picks choice, R resets
          document.addEventListener("keydown", (e) => {{
            const tag = (e.target && e.target.tagName) ? e.target.tagName.toLowerCase() : "";
            if (tag === "input" || tag === "textarea") return;

            const k = e.key.toLowerCase();

            if (k === "r") {{
              e.preventDefault();
              const resetForm = document.querySelector('form[action="/reset"]');
              if (resetForm) resetForm.submit();
              return;
            }}

            if (k >= "1" && k <= "9") {{
              const idx = parseInt(k, 10) - 1;
              const btn = document.querySelector(`button[data-choice="${{idx}}"]`);
              if (btn) {{
                e.preventDefault();
                btn.click();
              }}
            }}
          }});
        </script>
      </body>
    </html>
    """


@app.get("/", response_class=HTMLResponse)
def home():
    text, choices = step(STATE)
    return page(STATE, text, choices)


@app.post("/choose")
def choose(choice: int = Form(...)):
    step(STATE, choice)
    return RedirectResponse("/", status_code=303)


@app.post("/reset")
def reset():
    global STATE
    STATE = new_game_state()
    return RedirectResponse("/", status_code=303)


# NEW: instructions page route (reads instructions.html from same folder)
@app.get("/instructions", response_class=HTMLResponse)
def instructions():
    with open("instructions.html", "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())