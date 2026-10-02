import streamlit as st
import base64
from pathlib import Path

st.set_page_config(page_title="Alexandre ❤ Yasmin", page_icon="❤", layout="wide")

st.markdown("""
<style>
#MainMenu{visibility:hidden;}
footer{visibility:hidden;}
header{visibility:hidden;}
.block-container{padding:0 !important; max-width:100% !important;}
[data-testid="stVerticalBlock"]{gap:0;}
iframe{border:none;}
</style>
""", unsafe_allow_html=True)

def get_images():
    base_dir = Path(__file__).parent
    possible = [base_dir / "imagens", base_dir / "nosso-amor" / "imagens", Path("imagens")]
    folder = None
    for p in possible:
        if p.exists():
            folder = p
            break
    if folder is None:
        for p in Path(".").rglob("imagens"):
            if p.is_dir():
                folder = p
                break
    b64_list = []
    if folder and folder.exists():
        files = sorted(folder.rglob("*"))
        for ff in files:
            if ff.is_file() and ff.suffix.lower() in [".jpg",".jpeg",".png",".webp"]:
                try:
                    data = base64.b64encode(ff.read_bytes()).decode()
                    mime = "jpeg" if ff.suffix.lower() in [".jpg",".jpeg"] else ff.suffix.lower().replace(".","")
                    b64_list.append(f"data:image/{mime};base64,{data}")
                except:
                    pass
    return b64_list

imgs = get_images()
if len(imgs)==0:
    imgs = ["https://via.placeholder.com/800x600?text=Adicione+fotos+em+imagens/"]

carousel_items = ""
for i, img in enumerate(imgs):
    active = "active" if i==0 else ""
    carousel_items += f'<div class="carousel-item {active}"><img src="{img}"><div class="badge">💛 {i+1}/{len(imgs)}</div></div>\n'

dots = ""
for i in range(len(imgs)):
    active = "active" if i==0 else ""
    dots += f'<span class="dot {active}" onclick="goTo({i})"></span>'

html_template = f"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link href="https://fonts.googleapis.com/css2?family=Dancing+Script:wght@700&family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
<style>
  :root {{ --bg1:#ffe6f2; --bg2:#ffc2d1; --bg3:#ffb3c6; --card: rgba(255,255,255,0.88); --text:#4a1942; --sub:#a65a7a; --accent:#d63384; }}
  body.dark {{ --bg1:#1a0a14; --bg2:#2d1328; --bg3:#4a1942; --card: rgba(40,18,36,0.92); --text:#ffd6e8; --sub:#ffb3d1; --accent:#ff6b9d; }}
  *{{margin:0;padding:0;box-sizing:border-box;}}
  html,body{{min-height:100%;}}
  body{{font-family:'Poppins',sans-serif;background:transparent;color:var(--text);display:flex;justify-content:center;padding:14px;}}
  .page-bg{{position:fixed;inset:0;background:linear-gradient(135deg,var(--bg1),var(--bg2),var(--bg3));z-index:-1;}}
  .topbar{{display:flex;justify-content:space-between;max-width:1100px;width:100%;margin:0 auto 12px;}}
  .icon-btn{{background:var(--card);border:1.5px solid rgba(255,255,255,0.3);border-radius:50px;padding:7px 14px;font-size:11px;cursor:pointer;color:var(--text);box-shadow:0 4px 12px rgba(0,0,0,0.1);}}

  .wrapper{{width:100%;max-width:1100px;}}
  .main-grid{{display:grid;grid-template-columns:1.15fr 0.85fr;gap:18px;align-items:start;}}
  
  .card{{background:var(--card);backdrop-filter:blur(16px);border-radius:26px;padding:22px;box-shadow:0 20px 60px rgba(0,0,0,0.18);border:1.5px solid rgba(255,255,255,0.25);}}
  .left-card .header-row{{display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;}}
  .names-wrap{{text-align:left;}}
  .names{{font-family:'Dancing Script',cursive;font-size:40px;color:var(--accent);line-height:1;}}
  .names.small{{font-size:36px;}}
  .heart-beat{{font-size:32px;animation:beat 1.2s infinite;margin:0 8px;display:inline-block;}}
  @keyframes beat{{0%{{transform:scale(1);}}50%{{transform:scale(1.25);}}100%{{transform:scale(1);}}}}
  .subtitle{{font-size:10px;letter-spacing:3px;text-transform:uppercase;color:var(--sub);}}
  .date-line{{font-size:12px;color:var(--sub);margin-top:4px;}}

  .carousel{{position:relative;width:100%;aspect-ratio:4/3;border-radius:18px;overflow:hidden;box-shadow:0 10px 30px rgba(0,0,0,0.18);margin-top:14px;}}
  .carousel-item{{position:absolute;inset:0;opacity:0;transition:opacity .6s ease;}}
  .carousel-item.active{{opacity:1;z-index:2;}}
  .carousel-item img{{width:100%;height:100%;object-fit:cover;}}
  .badge{{position:absolute;bottom:10px;left:10px;background:rgba(0,0,0,0.55);color:white;padding:5px 10px;border-radius:20px;font-size:10px;}}
  .carousel-nav{{position:absolute;top:50%;width:100%;display:flex;justify-content:space-between;transform:translateY(-50%);z-index:3;padding:0 8px;}}
  .nav-btn{{background:rgba(255,255,255,0.9);border:none;width:34px;height:34px;border-radius:50%;cursor:pointer;font-size:18px;display:grid;place-items:center;}}
  .dots{{display:flex;gap:6px;justify-content:center;margin-top:10px;}}
  .dot{{width:7px;height:7px;border-radius:50%;background:rgba(214,51,132,0.25);cursor:pointer;}}
  .dot.active{{background:var(--accent);width:22px;}}

  .right-stack{{display:flex;flex-direction:column;gap:18px;}}
  .contador-box{{background:linear-gradient(135deg,#d63384,#ff6b9d);color:white;border-radius:20px;padding:20px;text-align:center;}}
  .contador-box h3{{font-size:13px;letter-spacing:2px;font-weight:600;opacity:0.95;}}
  .contador-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:14px;}}
  .unit{{background:rgba(255,255,255,0.18);border-radius:12px;padding:12px 4px;}}
  .unit b{{display:block;font-size:22px;}}
  .unit span{{font-size:10px;text-transform:uppercase;letter-spacing:1px;}}
  .seconds{{margin-top:12px;font-size:12px;opacity:0.9;}}

  .music-card{{background:var(--card);border-radius:18px;padding:16px;display:flex;align-items:center;gap:12px;border:1px solid rgba(255,255,255,0.3);}}
  .music-cover{{width:58px;height:58px;border-radius:14px;background:linear-gradient(135deg,#d63384,#ff6b9d);display:grid;place-items:center;font-size:28px;flex-shrink:0;}}
  .music-info b{{font-size:13px;display:block;}}
  .music-info span{{font-size:11px;color:var(--sub);}}
  .play-btn{{width:42px;height:42px;border-radius:50%;background:var(--accent);color:white;border:none;font-size:18px;cursor:pointer;margin-left:auto;}}

  .bottom-message{{margin-top:18px;text-align:center;background:var(--card);border-radius:20px;padding:22px 24px;box-shadow:0 10px 30px rgba(0,0,0,0.12);border:1.5px solid rgba(255,255,255,0.25);}}
  .bottom-message p{{font-family:'Dancing Script',cursive;font-size:28px;color:var(--accent);line-height:1.3;}}
  .bottom-message span{{display:block;margin-top:6px;font-family:'Poppins',sans-serif;font-size:13px;color:var(--sub);letter-spacing:1px;}}

  .hearts{{position:fixed;inset:0;pointer-events:none;overflow:hidden;}}
  .hearts span{{position:absolute;animation:fall linear infinite;}}
  @keyframes fall{{from{{transform:translateY(-10vh) rotate(0deg);opacity:1;}}to{{transform:translateY(110vh) rotate(360deg);opacity:0;}}}}

  @media (max-width: 900px){{
    .main-grid{{grid-template-columns:1fr;}}
    .topbar{{max-width:520px;}}
    .card{{max-width:520px;margin:0 auto;}}
    .bottom-message{{max-width:520px;margin:18px auto 0;}}
    .bottom-message p{{font-size:24px;}}
  }}
</style>
</head>
<body>
<div class="page-bg"></div>
<div class="hearts" id="hearts"></div>

<div class="wrapper">
  <div class="topbar">
    <button class="icon-btn" onclick="toggleDark()">🌙 / ☀️ Modo</button>
    <button class="icon-btn" onclick="toggleMusic()">🎵 Tocar música</button>
  </div>

  <div class="main-grid">
    <!-- ESQUERDA -->
    <div class="card left-card">
      <div class="header-row">
        <div class="names-wrap">
          <div class="subtitle">Nosso Amor</div>
          <div style="display:flex;align-items:center;margin-top:4px;">
            <div class="names">Alexandre</div>
            <div class="heart-beat">❤</div>
            <div class="names small">Yasmin</div>
          </div>
          <div class="date-line">Desde 19 de Setembro de 2026 • 16:30</div>
        </div>
      </div>

      <div class="carousel" id="carousel">
        {carousel_items}
        <div class="carousel-nav">
          <button class="nav-btn" onclick="prev()">‹</button>
          <button class="nav-btn" onclick="next()">›</button>
        </div>
      </div>
      <div class="dots">{dots}</div>
    </div>

    <!-- DIREITA -->
    <div class="right-stack">
      <div class="contador-box">
        <h3>ESTAMOS JUNTOS HÁ</h3>
        <div class="contador-grid">
          <div class="unit"><b id="anos">0</b><span>Anos</span></div>
          <div class="unit"><b id="meses">0</b><span>Meses</span></div>
          <div class="unit"><b id="dias">0</b><span>Dias</span></div>
          <div class="unit"><b id="horas">0</b><span>Horas</span></div>
          <div class="unit"><b id="mins">0</b><span>Min</span></div>
          <div class="unit"><b id="totalDias">0</b><span>Total dias</span></div>
        </div>
        <div class="seconds" id="fullText"></div>
      </div>

      <div class="card" style="padding:16px;">
        <div class="music-card" style="margin:0;border:none;padding:0;background:transparent;box-shadow:none;">
          <div class="music-cover">🎶</div>
          <div class="music-info">
            <b>Foi Assim - Sotam, Rob</b>
            <span>E foi assim quando te vi a primeira vez...</span>
          </div>
          <button class="play-btn" id="playBtn" onclick="toggleMusic()">▶</button>
        </div>
        <div id="ytWrap" style="display:none; margin-top:12px; border-radius:12px; overflow:hidden;">
          <iframe id="ytplayer" width="100%" height="180" src="https://www.youtube.com/embed/4ukPJTILszE?enablejsapi=1&loop=1" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
        </div>
      </div>
    </div>
  </div>

  <div class="bottom-message">
    <p>"Cada segundo ao seu lado é o meu capítulo favorito. Obrigado por me fazer o homem mais feliz do mundo. Te amo hoje e sempre."</p>
    <span>para minha nega ❤</span>
  </div>
</div>

<script>
const inicio = new Date("2026-09-19T16:30:00-03:00");
function atualizar(){{
  const agora = new Date();
  let diff = agora - inicio;
  const totalDias = Math.floor(diff / (1000*60*60*24));
  let anos = agora.getFullYear() - inicio.getFullYear();
  let meses = agora.getMonth() - inicio.getMonth();
  let dias = agora.getDate() - inicio.getDate();
  if(dias < 0){{ meses--; const prevMonth = new Date(agora.getFullYear(), agora.getMonth(), 0).getDate(); dias += prevMonth; }}
  if(meses < 0){{ anos--; meses += 12; }}
  const h = Math.floor((diff % (1000*60*60*24)) / (1000*60*60));
  const m = Math.floor((diff % (1000*60*60)) / (1000*60));
  const s = Math.floor((diff % (1000*60)) / 1000);
  document.getElementById("anos").innerText = anos;
  document.getElementById("meses").innerText = meses;
  document.getElementById("dias").innerText = dias;
  document.getElementById("horas").innerText = h;
  document.getElementById("mins").innerText = m;
  document.getElementById("totalDias").innerText = totalDias;
  document.getElementById("fullText").innerText = anos+" anos, "+meses+" meses, "+dias+" dias, "+h+"h "+m+"m "+s+"s de nós dois ❤";
}}
setInterval(atualizar,1000); atualizar();

let cur=0;
const items=document.querySelectorAll('.carousel-item');
const dotsEls=document.querySelectorAll('.dot');
function show(i){{
  items[cur].classList.remove('active');
  dotsEls[cur].classList.remove('active');
  cur=(i+items.length)%items.length;
  items[cur].classList.add('active');
  dotsEls[cur].classList.add('active');
}}
function next(){{show(cur+1);}}function prev(){{show(cur-1);}}function goTo(i){{show(i);}}
setInterval(next,4000);

const container = document.getElementById("hearts");
for(let i=0;i<18;i++){{
  const span=document.createElement("span");
  span.innerText=["❤","💖","💕","💗"][Math.floor(Math.random()*4)];
  span.style.left=Math.random()*100+"vw";
  span.style.animationDuration=(5+Math.random()*5)+"s";
  span.style.animationDelay=Math.random()*5+"s";
  container.appendChild(span);
}}
function toggleDark(){{
  document.body.classList.toggle('dark');
  localStorage.setItem('dark', document.body.classList.contains('dark'));
}}
if(localStorage.getItem('dark')==='true'){{document.body.classList.add('dark');}}
let playing=false;
function toggleMusic(){{
  const wrap=document.getElementById('ytWrap');
  const btn=document.getElementById('playBtn');
  if(!playing){{wrap.style.display='block';btn.innerText='⏸';playing=true;document.getElementById('ytplayer').src+='&autoplay=1';}} else {{wrap.style.display='none';btn.innerText='▶';playing=false;}}
}}
</script>
</body>
</html>
"""

st.components.v1.html(html_template, height=850, scrolling=False)
