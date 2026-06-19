from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from html import escape

from little_red_engine import new_game_state, step

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

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
  --arcade:#FFD93B;
  --arcadeShadow:#D62828;
}

*{ box-sizing:border-box; }

html{
  width:100%;
  overflow-x:hidden;
}

body{
  margin:0;
  width:100%;
  min-height:100vh;
  overflow-x:hidden;
  font-family:"Press Start 2P", system-ui, sans-serif;
  color:var(--text);
  background:
    radial-gradient(1200px 600px at 50% 20%, rgba(45,252,255,.14), transparent 60%),
    radial-gradient(900px 500px at 30% 80%, rgba(255,43,214,.12), transparent 60%),
    linear-gradient(180deg, var(--bg1), var(--bg2));
}

button{ font-family:inherit; }

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
  width:min(100% - 32px, 920px);
  margin: 26px auto;
  padding: 0 0 40px;
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
  max-width:680px;
  font-size: clamp(14px, 2vw, 18px);
  line-height:1.45;
  color: var(--arcade);
  overflow-wrap:anywhere;
  text-shadow:
    3px 3px 0 var(--arcadeShadow),
    0 0 10px rgba(255,217,59,.18);
}

.sub{
  flex:0 0 auto;
  max-width:260px;
  font-size:10px;
  color:var(--muted);
  text-align:right;
  line-height:1.55;
}

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
  flex:1 1 170px;
  min-width:0;
  padding: 8px 10px;
  border-radius: 999px;
  border: 1px solid rgba(255,255,255,.14);
  background: rgba(255,255,255,.04);
  overflow-wrap:anywhere;
  line-height:1.45;
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

.crt::before{
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

.crt::after{
  content:"";
  position:absolute; inset:-20%;
  background:
    radial-gradient(circle at 50% 35%, rgba(255,43,214,.08), transparent 55%),
    radial-gradient(circle at 50% 50%, rgba(0,0,0,.55), transparent 60%);
  pointer-events:none;
}

.story{
  position:relative;
  z-index:1;
  margin:0;
  white-space:pre-wrap;
  overflow-wrap:anywhere;
  line-height: 1.85;
  font-size: 15px;
  color: var(--text);
  text-shadow: none;
}

.choices{
  position:relative;
  z-index:1;
  margin-top: 14px;
  display:flex;
  flex-direction:column;
  gap:10px;
}

.choice-form{
  width:100%;
  margin:0;
}

.choice-btn{
  display:block;
  width:100%;
  min-height:44px;
  text-align:left;
  border: 1px solid rgba(255,255,255,.16);
  background: rgba(255,255,255,.05);
  color: var(--arcade);
  padding: 14px 14px;
  border-radius: 14px;
  cursor:pointer;
  font-size: 11px;
  line-height:1.55;
  white-space:normal;
  overflow-wrap:anywhere;
  transition: transform .06s ease, box-shadow .12s ease, background .12s ease, border-color .12s ease;
}

.choice-btn span{
  font-size:inherit !important;
  letter-spacing:inherit !important;
  line-height:inherit;
}

.choice-btn:hover{
  transform: scale(1.03);
  border-color: rgba(45,252,255,.9);
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
  position:relative;
  z-index:1;
  margin-top: 14px;
  display:flex;
  align-items:center;
  justify-content:space-between;
  flex-wrap:wrap;
  gap:12px;
}

.reset-btn{
  min-height:40px;
  border: 1px solid rgba(255,43,214,.45);
  background: rgba(255,43,214,.10);
  color: var(--text);
  padding: 10px 12px;
  border-radius: 12px;
  cursor:pointer;
  font-size: 10px;
}

.reset-btn:hover{
  box-shadow: 0 0 16px rgba(255,43,214,.14);
}

.credit{
  font-size:10px;
  color: var(--muted);
  overflow-wrap:anywhere;
}

.maker-stamp{
  position:fixed;
  right:18px;
  bottom:14px;
  z-index:20;
  font-size:12px;
  color: rgba(255,217,59,.95);
  padding:10px 12px;
  border:1px solid rgba(255,217,59,.55);
  border-radius:12px;
  background:rgba(10,10,20,.50);
  box-shadow: 0 0 16px rgba(255,217,59,.14);
  text-transform:lowercase;
  letter-spacing:1px;
  pointer-events:none;
}

a, a:visited { color: var(--cyan); text-decoration:none; }
a:hover { text-decoration:underline; }

.hint{
  position:relative;
  z-index:1;
  margin-top: 10px;
  color: rgba(185,179,214,.9);
  font-size: 9px;
  line-height: 1.5;
  overflow-wrap:anywhere;
}

.character{
  position: fixed;
  bottom: 20px;
  left: 20px;
  z-index: 10;
  pointer-events:none;
}

.character img{
  display:block;
  width: clamp(110px, 13vw, 160px);
  height:auto;
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

@media (max-width: 900px){
  .wrap{
    width:min(100% - 28px, 820px);
    margin:20px auto;
  }

  h1{
    font-size: clamp(13px, 2.25vw, 16px);
    text-shadow:
      2px 2px 0 var(--arcadeShadow),
      0 0 10px rgba(255,217,59,.16);
  }

  .sub{
    font-size:9px;
    max-width:230px;
  }

  .story{
    font-size:13px;
  }

  .choice-btn{
    padding:12px;
    font-size:10px;
  }

  .choice-btn:hover{
    transform: scale(1.015);
  }

  .character{
    bottom:14px;
    left:12px;
  }

  .character img{
    width:110px;
  }

  .maker-stamp{
    right:12px;
    bottom:10px;
    font-size:10px;
    padding:8px 10px;
  }
}

@media (max-width: 700px){
  .wrap{
    width:min(100% - 24px, 620px);
    margin:14px auto;
    padding-bottom:24px;
  }

  .header{
    flex-direction:column;
    align-items:center;
    text-align:center;
    gap:12px;
  }

  h1{
    max-width:100%;
    font-size: clamp(12px, 4.2vw, 16px);
    line-height:1.55;
    text-align:center;
  }

  .sub{
    width:100%;
    max-width:360px;
    text-align:center;
    font-size:9px;
  }

  .hud{
    flex-direction:column;
    align-items:stretch;
    gap:8px;
    font-size:9px;
  }

  .hud .pill{
    flex:none;
    width:100%;
    border-radius:12px;
    text-align:center;
  }

  .crt{
    padding:14px;
    border-radius:14px;
  }

  .story{
    font-size:12px;
    line-height:1.75;
  }

  .choices{
    gap:8px;
  }

  .choice-btn{
    padding:11px 10px;
    font-size:9px;
    border-radius:11px;
  }

  .choice-btn:hover{
    transform:none;
  }

  .footer-row{
    flex-direction:column;
    align-items:stretch;
  }

  .footer-row form,
  .reset-btn{
    width:100%;
  }

  .credit{
    text-align:center;
    font-size:8px;
  }

  .hint{
    text-align:center;
    font-size:8px;
  }

  .character{
    position:static;
    display:flex;
    justify-content:center;
    margin:12px auto 0;
  }

  .character img{
    width:88px;
  }

  .maker-stamp{
    position:static;
    display:block;
    width:max-content;
    max-width:calc(100% - 24px);
    margin:8px auto 18px;
    padding:7px 9px;
    font-size:8px;
    text-align:center;
  }
}

@media (max-width: 420px){
  .wrap{
    width:min(100% - 18px, 390px);
    margin:10px auto;
  }

  .bg-grid{
    background-size:38px 38px;
  }

  h1{
    font-size: clamp(11px, 5vw, 14px);
    line-height:1.6;
  }

  .sub{
    font-size:8px;
  }

  .instructions-link{
    padding:7px 8px;
  }

  .hud{
    font-size:8px;
  }

  .crt{
    padding:12px;
    border-radius:12px;
  }

  .story{
    font-size:10px;
  }

  .choice-btn{
    padding:10px 9px;
    font-size:8px;
  }

  .reset-btn{
    font-size:8px;
  }

  .credit,
  .hint{
    font-size:7px;
  }

  .character img{
    width:72px;
  }
}

@media (max-width: 330px){
  .character{
    display:none;
  }

  .maker-stamp{
    display:none;
  }
}
"""


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


@app.get("/instructions", response_class=HTMLResponse)
def instructions():
    with open("instructions.html", "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())
