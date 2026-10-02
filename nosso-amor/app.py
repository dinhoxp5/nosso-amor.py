import streamlit as st
import base64
from pathlib import Path
# python -m streamlit run app.py / da go no site
st.set_page_config(page_title="Alexandre ❤ Yasmin", page_icon="❤", layout="centered")

st.markdown("""
<style>
#MainMenu{visibility:hidden;}footer{visibility:hidden;}header{visibility:hidden;}
</style>
""", unsafe_allow_html=True)

def get_images():
    folder = Path("imagens")
    b64_list = []
    # se não achar na raiz, procura em subpastas
    if not folder.exists():
        # tenta achar em qualquer lugar tipo nosso-amor/imagens
        for p in Path(".").rglob("imagens"):
            if p.is_dir():
                folder = p
                break
    
    if folder.exists():
        files = sorted(folder.rglob("*")) # rglob pega até de subpasta
        for f in files:
            if f.suffix.lower() in [".jpg",".jpeg",".png",".webp"]:
                try:
                    data = base64.b64encode(f.read_bytes()).decode()
                    b64_list.append(f"data:image/jpeg;base64,{data}")
                except:
                    pass
    return b64_list

imgs = get_images()

if len(imgs)==0:
    imgs = ["https://via.placeholder.com/400x500?text=Adicione+fotos+em+imagens/"]

# gera divs do carrossel
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
  :root {{
    --bg1:#ffe6f2; --bg2:#ffc2d1; --bg3:#ffb3c6;
    --card: rgba(255,255,255,0.88);
    --text:#4a1942; --sub:#a65a7a; --accent:#d63384;
  }}
  body.dark {{
    --bg1:#1a0a14; --bg2:#2d1328; --bg3:#4a1942;
    --card: rgba(40,18,36,0.92);
    --text:#ffd6e8; --sub:#ffb3d1; --accent:#ff6b9d;
  }}
  *{{margin:0;padding:0;box-sizing:border-box;}}
  body{{font-family:'Poppins',sans-serif;text-align:center;background:transparent;color:var(--text);transition:all .4s;}}
  .page-bg{{position:fixed;inset:0;background:linear-gradient(135deg,var(--bg1),var(--bg2),var(--bg3));z-index:-1;transition:all .4s;}}
  .topbar{{display:flex;justify-content:space-between;align-items:center;max-width:520px;margin:0 auto 12px;padding:0 4px;}}
  .icon-btn{{background:var(--card);border:1.5px solid rgba(255,255,255,0.3);border-radius:50px;padding:8px 14px;font-size:12px;cursor:pointer;box-shadow:0 4px 12px rgba(0,0,0,0.1);transition:.2s;color:var(--text);}}
  .icon-btn:hover{{transform:scale(1.05);}}
  .card{{background:var(--card);backdrop-filter:blur(16px);border-radius:28px;padding:32px 24px;box-shadow:0 20px 60px rgba(0,0,0,0.2);border:1.5px solid rgba(255,255,255,0.25);max-width:520px;margin:0 auto;transition:all .4s;}}
  .names{{font-family:'Dancing Script',cursive;font-size:48px;color:var(--accent);line-height:1;}}
  .heart-beat{{font-size:56px;animation:beat 1.2s infinite;margin:10px 0;display:inline-block;}}
  @keyframes beat{{0%{{transform:scale(1);}}50%{{transform:scale(1.2);}}100%{{transform:scale(1);}}}}
  .subtitle{{font-size:12px;letter-spacing:3px;text-transform:uppercase;color:var(--sub);margin-bottom:10px;}}
  
  /* CARROSSEL */
  .carousel{{position:relative;width:100%;aspect-ratio:4/3.2;border-radius:20px;overflow:hidden;box-shadow:0 10px 30px rgba(0,0,0,0.2);margin:18px 0;}}
  .carousel-item{{position:absolute;inset:0;opacity:0;transition:opacity .6s ease, transform .6s ease;transform:scale(0.98);}}
  .carousel-item.active{{opacity:1;transform:scale(1);z-index:2;}}
  .carousel-item img{{width:100%;height:100%;object-fit:cover;}}
  .badge{{position:absolute;bottom:10px;left:10px;background:rgba(0,0,0,0.55);color:white;padding:5px 12px;border-radius:20px;font-size:11px;font-weight:600;backdrop-filter:blur(4px);}}
  .carousel-nav{{position:absolute;top:50%;width:100%;display:flex;justify-content:space-between;transform:translateY(-50%);z-index:3;padding:0 8px;}}
  .nav-btn{{background:rgba(255,255,255,0.85);border:none;width:36px;height:36px;border-radius:50%;cursor:pointer;font-size:18px;display:grid;place-items:center;box-shadow:0 2px 8px rgba(0,0,0,0.2);}}
  .dots{{display:flex;gap:6px;justify-content:center;margin-top:12px;}}
  .dot{{width:8px;height:8px;border-radius:50%;background:rgba(214,51,132,0.25);cursor:pointer;transition:.3s;}}
  .dot.active{{background:var(--accent);width:22px;}}
  body.dark .dot{{background:rgba(255,255,255,0.2);}}
  body.dark .dot.active{{background:#ff6b9d;}}

  .contador-box{{background:linear-gradient(135deg,#d63384,#ff6b9d);color:white;border-radius:18px;padding:18px;margin-top:18px;}}
  .contador-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:12px;}}
  .unit{{background:rgba(255,255,255,0.18);border-radius:12px;padding:10px 4px;}}
  .unit b{{display:block;font-size:22px;}}
  .unit span{{font-size:11px;text-transform:uppercase;letter-spacing:1px;}}
  .seconds{{margin-top:12px;font-size:13px;opacity:0.9;}}

  /* MUSICA */
  .music-card{{background:var(--card);border-radius:16px;padding:14px;margin-top:16px;display:flex;align-items:center;gap:12px;text-align:left;border:1px solid rgba(255,255,255,0.3);}}
  .music-cover{{width:56px;height:56px;border-radius:12px;background:linear-gradient(135deg,#d63384,#ff6b9d);display:grid;place-items:center;font-size:28px;flex-shrink:0;}}
  .music-info{{flex:1;}}
  .music-info b{{display:block;font-size:13px;color:var(--text);}}
  .music-info span{{font-size:11px;color:var(--sub);}}
  .play-btn{{width:42px;height:42px;border-radius:50%;background:var(--accent);color:white;border:none;font-size:18px;cursor:pointer;display:grid;place-items:center;box-shadow:0 4px 12px rgba(214,51,132,0.3);}}

  .message{{margin-top:18px;font-size:14.5px;line-height:1.6;color:var(--text);font-style:italic;opacity:0.9;}}
  .hearts{{position:fixed;inset:0;pointer-events:none;overflow:hidden;z-index:0;}}
  .hearts span{{position:absolute;animation:fall linear infinite;font-size:18px;}}
  @keyframes fall{{from{{transform:translateY(-10vh) rotate(0deg);opacity:1;}}to{{transform:translateY(110vh) rotate(360deg);opacity:0;}}}}
</style>
</head>
<body>
<div class="page-bg"></div>
<div class="hearts" id="hearts"></div>

<div class="topbar">
  <button class="icon-btn" onclick="toggleDark()">🌙 / ☀️ Modo</button>
  <button class="icon-btn" onclick="toggleMusic()">🎵 Música</button>
</div>

<div class="card">
  <div class="subtitle">Nosso Amor</div>
  <div class="names">Alexandre</div>
  <div class="heart-beat">❤</div>
  <div class="names">Yasmin</div>
  <p style="margin-top:8px;color:var(--sub);font-size:13px;">Desde 19 de Setembro de 2026 • 16:30</p>

  <!-- CARROSSEL -->
  <div class="carousel" id="carousel">
    {carousel_items}
    <div class="carousel-nav">
      <button class="nav-btn" onclick="prev()">‹</button>
      <button class="nav-btn" onclick="next()">›</button>
    </div>
  </div>
  <div class="dots">{dots}</div>

  <div class="contador-box">
    <div style="font-weight:600;letter-spacing:1px;font-size:14px;">ESTAMOS JUNTOS HÁ</div>
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

  <!-- MUSICA -->
  <div class="music-card" id="musicCard">
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

  <p class="message">"Cada segundo ao seu lado é o meu momento favorito. Que venham muitos anos, muitos sonhos e muitos 'nós'."</p>
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

// carrossel
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

// coracoes
const container = document.getElementById("hearts");
for(let i=0;i<18;i++){{
  const span=document.createElement("span");
  span.innerText=["❤","💖","💕","💗"][Math.floor(Math.random()*4)];
  span.style.left=Math.random()*100+"vw";
  span.style.animationDuration=(5+Math.random()*5)+"s";
  span.style.animationDelay=Math.random()*5+"s";
  container.appendChild(span);
}}

// dark mode
function toggleDark(){{
  document.body.classList.toggle('dark');
  localStorage.setItem('dark', document.body.classList.contains('dark'));
}}
if(localStorage.getItem('dark')==='true'){{document.body.classList.add('dark');}}

// musica
let playing=false;
function toggleMusic(){{
  const wrap=document.getElementById('ytWrap');
  const btn=document.getElementById('playBtn');
  if(!playing){{
    wrap.style.display='block';
    btn.innerText='⏸';
    playing=true;
    // tenta autoplay
    const iframe=document.getElementById('ytplayer');
    iframe.src = iframe.src + "&autoplay=1";
  }} else {{
    wrap.style.display='none';
    btn.innerText='▶';
    playing=false;
  }}
}}
</script>
</body>
</html>
"""

html_final = html_template

st.components.v1.html(html_final, height=1100, scrolling=True)
st.markdown("<p style='text-align:center;font-size:12px;color:#a65a7a;margin-top:14px;'>Feito com ❤ para Yasmin minha nega • com 🎵 Foi Assim - Sotam</p>", unsafe_allow_html=True)
