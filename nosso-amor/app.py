import streamlit as st
import base64
from pathlib import Path

st.set_page_config(page_title="Alexandre ❤ Yasmin", page_icon="❤", layout="wide")

st.markdown('''
<style>
#MainMenu{visibility:hidden;}
footer{visibility:hidden;}
header{visibility:hidden;}
.block-container{
    padding-top: 0rem !important;
    padding-bottom: 0rem !important;
    padding-left: 0rem !important;
    padding-right: 0rem !important;
    max-width: 100% !important;
}
[data-testid="stVerticalBlock"]{gap:0rem;}
iframe{border:none;}
</style>
''', unsafe_allow_html=True)

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
        for f in files:
            if f.is_file() and f.suffix.lower() in [".jpg",".jpeg",".png",".webp"]:
                try:
                    data = base64.b64encode(f.read_bytes()).decode()
                    mime = "jpeg" if f.suffix.lower() in [".jpg",".jpeg"] else f.suffix.lower().replace(".","")
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
  html, body {{height:100%; overflow:hidden;}}
  body{{font-family:'Poppins',sans-serif;text-align:center;background:transparent;color:var(--text); display:flex; align-items:center; justify-content:center; min-height:100vh; padding:8px;}}
  .page-bg{{position:fixed;inset:0;background:linear-gradient(135deg,var(--bg1),var(--bg2),var(--bg3));z-index:-1;}}
  .topbar{{display:flex;justify-content:space-between;align-items:center;max-width:520px;margin:0 auto 10px;width:100%;}}
  .icon-btn{{background:var(--card);border:1.5px solid rgba(255,255,255,0.3);border-radius:50px;padding:7px 12px;font-size:11px;cursor:pointer;color:var(--text);}}
  .card{{background:var(--card);backdrop-filter:blur(16px);border-radius:28px;padding:20px;box-shadow:0 20px 60px rgba(0,0,0,0.2);border:1.5px solid rgba(255,255,255,0.25);max-width:520px; width:100%; max-height:96vh; overflow-y:auto; scrollbar-width:none;}}
  .card::-webkit-scrollbar{{display:none;}}
  .names{{font-family:'Dancing Script',cursive;font-size:42px;color:var(--accent);line-height:1;}}
  .heart-beat{{font-size:44px;animation:beat 1.2s infinite;margin:6px 0;display:inline-block;}}
  @keyframes beat{{0%{{transform:scale(1);}}50%{{transform:scale(1.2);}}100%{{transform:scale(1);}}}}
  .subtitle{{font-size:11px;letter-spacing:3px;text-transform:uppercase;color:var(--sub);margin-bottom:6px;}}
  .carousel{{position:relative;width:100%;aspect-ratio:4/3.1;border-radius:18px;overflow:hidden;box-shadow:0 10px 30px rgba(0,0,0,0.2);margin:12px 0;}}
  .carousel-item{{position:absolute;inset:0;opacity:0;transition:opacity .6s ease;transform:scale(0.98);}}
  .carousel-item.active{{opacity:1;transform:scale(1);z-index:2;}}
  .carousel-item img{{width:100%;height:100%;object-fit:cover;}}
  .badge{{position:absolute;bottom:8px;left:8px;background:rgba(0,0,0,0.55);color:white;padding:4px 10px;border-radius:20px;font-size:10px;}}
  .carousel-nav{{position:absolute;top:50%;width:100%;display:flex;justify-content:space-between;transform:translateY(-50%);z-index:3;padding:0 6px;}}
  .nav-btn{{background:rgba(255,255,255,0.85);border:none;width:32px;height:32px;border-radius:50%;cursor:pointer;font-size:16px;display:grid;place-items:center;}}
  .dots{{display:flex;gap:5px;justify-content:center;margin-top:8px;}}
  .dot{{width:7px;height:7px;border-radius:50%;background:rgba(214,51,132,0.25);cursor:pointer;}}
  .dot.active{{background:var(--accent);width:20px;}}
  .contador-box{{background:linear-gradient(135deg,#d63384,#ff6b9d);color:white;border-radius:16px;padding:14px;margin-top:12px;}}
  .contador-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-top:8px;}}
  .unit{{background:rgba(255,255,255,0.18);border-radius:10px;padding:7px 2px;}}
  .unit b{{display:block;font-size:18px;}}
  .unit span{{font-size:10px;text-transform:uppercase;}}
  .seconds{{margin-top:8px;font-size:11px;}}
  .music-card{{background:var(--card);border-radius:14px;padding:10px;margin-top:12px;display:flex;align-items:center;gap:10px;text-align:left;border:1px solid rgba(255,255,255,0.3);}}
  .music-cover{{width:48px;height:48px;border-radius:10px;background:linear-gradient(135deg,#d63384,#ff6b9d);display:grid;place-items:center;font-size:24px;}}
  .music-info b{{display:block;font-size:12px;}}
  .music-info span{{font-size:10px;color:var(--sub);}}
  .play-btn{{width:38px;height:38px;border-radius:50%;background:var(--accent);color:white;border:none;font-size:16px;cursor:pointer;display:grid;place-items:center;}}
  .message{{margin-top:12px;font-size:13px;line-height:1.5;font-style:italic;}}
  .hearts{{position:fixed;inset:0;pointer-events:none;overflow:hidden;}}
  .hearts span{{position:absolute;animation:fall linear infinite;font-size:16px;}}
  @keyframes fall{{from{{transform:translateY(-10vh) rotate(0deg);opacity:1;}}to{{transform:translateY(110vh) rotate(360deg);opacity:0;}}}}
</style>
</head>
<body>
<div class="page-bg"></div>
<div class="hearts" id="hearts"></div>
<div style="width:100%; max-width:520px;">
<div class="topbar">
  <button class="icon-btn" onclick="toggleDark()">🌙 / ☀️</button>
  <button class="icon-btn" onclick="toggleMusic()">🎵 Música</button>
</div>
<div class="card">
  <div class="subtitle">Nosso Amor</div>
  <div class="names">Alexandre</div>
  <div class="heart-beat">❤</div>
  <div class="names">Yasmin</div>
  <p style="margin-top:4px;color:var(--sub);font-size:12px;">Desde 19 de Setembro de 2026 • 16:30</p>
  <div class="carousel" id="carousel">
    {carousel_items}
    <div class="carousel-nav">
      <button class="nav-btn" onclick="prev()">‹</button>
      <button class="nav-btn" onclick="next()">›</button>
    </div>
  </div>
  <div class="dots">{dots}</div>
  <div class="contador-box">
    <div style="font-weight:600;font-size:13px;">ESTAMOS JUNTOS HÁ</div>
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
  <div class="music-card">
    <div class="music-cover">🎶</div>
    <div class="music-info"><b>Foi Assim - Sotam, Rob</b><span>E foi assim quando te vi...</span></div>
    <button class="play-btn" id="playBtn" onclick="toggleMusic()">▶</button>
  </div>
  <div id="ytWrap" style="display:none; margin-top:10px; border-radius:12px; overflow:hidden;">
    <iframe id="ytplayer" width="100%" height="160" src="https://www.youtube.com/embed/4ukPJTILszE?enablejsapi=1&loop=1" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
  </div>
  <p class="message">"Cada segundo ao seu lado é o meu momento favorito."</p>
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
for(let i=0;i<16;i++){{
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

st.components.v1.html(html_template, height=950, scrolling=False)
