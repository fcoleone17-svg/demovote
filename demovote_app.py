import streamlit as st
import time
import random
from datetime import datetime

# ─── Page config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DemoVote²",
    page_icon="⬆",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─── Global CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Inter:wght@300;400;500&display=swap');

  /* ── Root palette ── */
  :root {
    --bg:        #0b0e1a;
    --surface:   #111629;
    --border:    #1e2540;
    --cyan:      #00e5ff;
    --purple:    #7c3aed;
    --grad:      linear-gradient(135deg, #00e5ff 0%, #7c3aed 100%);
    --text:      #e8eaf6;
    --muted:     #7986a6;
    --yes:       #00e5ff;
    --no:        #ff3d71;
    --abstain:   #7c3aed;
  }

  /* ── App shell ── */
  html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    font-family: 'Inter', sans-serif;
    color: var(--text);
  }
  [data-testid="stHeader"] { background: transparent !important; }
  section[data-testid="stSidebar"] { display: none; }
  .main .block-container { padding: 2rem 1.5rem 4rem; max-width: 780px; }

  /* ── Header ── */
  .dv-header {
    display: flex; align-items: center; gap: 14px;
    padding: 1.6rem 0 0.4rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1.8rem;
  }
  .dv-logo-mark {
    width: 44px; height: 44px;
    background: var(--grad);
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 22px; font-weight: 900;
    box-shadow: 0 0 18px #00e5ff44;
  }
  .dv-brand { font-family: 'Syne', sans-serif; }
  .dv-brand span { font-size: 1.5rem; font-weight: 800; letter-spacing: -0.5px; }
  .dv-brand small { display: block; font-size: 0.72rem; color: var(--muted); font-weight: 400; letter-spacing: 0.05em; }
  .dv-live-pill {
    margin-left: auto;
    background: #ff3d7118;
    border: 1px solid #ff3d7155;
    color: #ff3d71;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    animation: pulse-red 2s ease-in-out infinite;
  }
  @keyframes pulse-red {
    0%,100% { box-shadow: 0 0 0 0 #ff3d7133; }
    50%      { box-shadow: 0 0 0 6px #ff3d7100; }
  }

  /* ── Issue card ── */
  .issue-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 1.8rem;
    margin-bottom: 1.2rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s;
  }
  .issue-card::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 3px;
    background: var(--grad);
  }
  .issue-tag {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 6px;
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 0.8rem;
  }
  .tag-economy   { background: #00e5ff15; color: var(--cyan); border: 1px solid #00e5ff33; }
  .tag-health    { background: #00ff9015; color: #00ff90; border: 1px solid #00ff9033; }
  .tag-education { background: #ffb30015; color: #ffb300; border: 1px solid #ffb30033; }
  .tag-security  { background: #ff3d7115; color: #ff3d71; border: 1px solid #ff3d7133; }
  .tag-housing   { background: #7c3aed15; color: #a78bfa; border: 1px solid #7c3aed33; }

  .issue-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.25rem;
    font-weight: 700;
    line-height: 1.3;
    margin: 0.3rem 0 0.7rem;
    color: #fff;
  }
  .issue-desc {
    font-size: 0.88rem;
    color: var(--muted);
    line-height: 1.6;
    margin-bottom: 1.2rem;
  }
  .issue-meta {
    display: flex; gap: 1.2rem; margin-bottom: 1.4rem;
    font-size: 0.75rem; color: var(--muted);
  }
  .issue-meta span { display: flex; align-items: center; gap: 5px; }

  /* ── Progress bar ── */
  .prog-row { margin-bottom: 1.2rem; }
  .prog-labels { display: flex; justify-content: space-between; font-size: 0.72rem; color: var(--muted); margin-bottom: 6px; }
  .prog-bar { height: 8px; background: #1a1f35; border-radius: 99px; overflow: hidden; display: flex; gap: 2px; }
  .prog-yes     { background: var(--cyan);    border-radius: 99px 0 0 99px; }
  .prog-no      { background: var(--no);      }
  .prog-abstain { background: var(--abstain); border-radius: 0 99px 99px 0; }
  .prog-counts { display: flex; justify-content: space-between; font-size: 0.75rem; margin-top: 5px; }
  .c-yes { color: var(--cyan); } .c-no { color: var(--no); } .c-abs { color: #a78bfa; }

  /* ── Vote buttons ── */
  .vote-buttons { display: flex; gap: 10px; }
  .stButton > button {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 12px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    padding: 0.5rem 1.2rem !important;
    transition: all 0.2s !important;
    cursor: pointer;
  }
  .stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 16px #00e5ff22 !important;
  }

  /* ── Voted state ── */
  .voted-banner {
    display: flex; align-items: center; gap: 10px;
    background: #00e5ff0d;
    border: 1px solid #00e5ff33;
    border-radius: 12px;
    padding: 0.8rem 1.1rem;
    font-size: 0.85rem;
    color: var(--cyan);
    font-weight: 500;
    margin-top: 0.5rem;
  }
  .voted-icon { font-size: 1.2rem; }

  /* ── Mandate sent animation ── */
  .mandate-flash {
    text-align: center;
    padding: 1rem;
    background: linear-gradient(135deg, #00e5ff10, #7c3aed10);
    border: 1px solid #00e5ff33;
    border-radius: 14px;
    color: var(--cyan);
    font-family: 'Syne', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    animation: flash-in 0.4s ease;
    margin-top: 0.5rem;
  }
  @keyframes flash-in {
    from { opacity: 0; transform: scale(0.95); }
    to   { opacity: 1; transform: scale(1); }
  }

  /* ── Stats bar ── */
  .stats-row {
    display: flex; gap: 1rem;
    margin-bottom: 1.8rem;
  }
  .stat-chip {
    flex: 1;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1rem;
    text-align: center;
  }
  .stat-num {
    font-family: 'Syne', sans-serif;
    font-size: 1.6rem;
    font-weight: 800;
    background: var(--grad);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }
  .stat-lbl { font-size: 0.7rem; color: var(--muted); margin-top: 2px; }

  /* ── Section title ── */
  .section-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 1rem;
  }

  /* ── Tabs ── */
  .stTabs [data-baseweb="tab-list"] {
    background: var(--surface) !important;
    border-radius: 12px;
    padding: 4px;
    gap: 4px;
    border: 1px solid var(--border);
    margin-bottom: 1.4rem;
  }
  .stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--muted) !important;
    border-radius: 9px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    border: none !important;
    padding: 0.45rem 1.1rem !important;
  }
  .stTabs [aria-selected="true"] {
    background: var(--grad) !important;
    color: #fff !important;
  }
  .stTabs [data-baseweb="tab-border"] { display: none !important; }

  /* ── Citizen profile ── */
  .profile-pill {
    display: inline-flex; align-items: center; gap: 8px;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 99px;
    padding: 6px 14px 6px 8px;
    font-size: 0.8rem;
    color: var(--muted);
    margin-bottom: 1.6rem;
  }
  .profile-avatar {
    width: 28px; height: 28px;
    background: var(--grad);
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.8rem;
  }
  .profile-name { color: var(--text); font-weight: 500; }

  /* ── History item ── */
  .history-item {
    display: flex; align-items: center; gap: 12px;
    padding: 0.8rem 0;
    border-bottom: 1px solid var(--border);
    font-size: 0.83rem;
  }
  .h-icon { font-size: 1.1rem; width: 28px; text-align: center; }
  .h-title { flex: 1; color: var(--text); }
  .h-vote  { font-weight: 600; font-size: 0.75rem; padding: 2px 8px; border-radius: 6px; }
  .h-yes  { background: #00e5ff15; color: var(--cyan); }
  .h-no   { background: #ff3d7115; color: var(--no); }
  .h-abs  { background: #7c3aed15; color: #a78bfa; }
  .h-time { font-size: 0.7rem; color: var(--muted); }

  /* Hide streamlit chrome */
  #MainMenu, footer, [data-testid="stToolbar"] { display: none !important; }
  .stAlert { border-radius: 12px !important; }
</style>
""", unsafe_allow_html=True)

# ─── Session state init ──────────────────────────────────────────────────────
if "votes" not in st.session_state:
    st.session_state.votes = {}         # issue_id -> "yes" | "no" | "abstain"
if "counts" not in st.session_state:
    # seed with realistic-looking numbers
    st.session_state.counts = {
        "i1": {"yes": 48230, "no": 21450, "abstain": 4310},
        "i2": {"yes": 31900, "no": 39200, "abstain": 7600},
        "i3": {"yes": 62100, "no": 8400,  "abstain": 3200},
        "i4": {"yes": 27300, "no": 44800, "abstain": 9100},
    }
if "mandate_flash" not in st.session_state:
    st.session_state.mandate_flash = None
if "history" not in st.session_state:
    st.session_state.history = []

# ─── Data ───────────────────────────────────────────────────────────────────
ISSUES = [
    {
        "id": "i1",
        "tag": "Economía", "tag_class": "tag-economy",
        "emoji": "💰",
        "title": "Reducción del IVA en alimentos básicos del 19% al 10%",
        "desc": "El proyecto busca reducir el IVA aplicado a alimentos de la canasta básica familiar para aliviar el costo de vida. Congreso vota mañana a las 10:00 hrs.",
        "deadline": "Mañana 10:00 hrs",
        "district": "Nacional",
    },
    {
        "id": "i2",
        "tag": "Seguridad", "tag_class": "tag-security",
        "emoji": "🛡️",
        "title": "Ampliación de atribuciones de las FFAA en zonas de alta conflictividad",
        "desc": "Propuesta que otorgaría mayores poderes operativos a las fuerzas armadas en regiones con índices de violencia por sobre el promedio nacional.",
        "deadline": "Hoy 18:00 hrs",
        "district": "Nacional",
    },
    {
        "id": "i3",
        "tag": "Educación", "tag_class": "tag-education",
        "emoji": "📚",
        "title": "Extensión de la gratuidad universitaria al 70% de la población",
        "desc": "El proyecto expande el acceso gratuito a la educación superior pública, subiendo el umbral de ingresos elegibles del 60% al 70% de los hogares.",
        "deadline": "Esta semana",
        "district": "Nacional",
    },
    {
        "id": "i4",
        "tag": "Vivienda", "tag_class": "tag-housing",
        "emoji": "🏠",
        "title": "Subsidio habitacional de emergencia para arrendatarios en mora",
        "desc": "Fondo de emergencia para familias arrendatarias que acumularon deuda de arriendo durante crisis económica. Cubre hasta 4 meses de deuda.",
        "deadline": "Esta semana",
        "district": "Nacional",
    },
]

VOTE_LABELS = {
    "yes":     ("✅", "A FAVOR"),
    "no":      ("❌", "EN CONTRA"),
    "abstain": ("⬜", "ABSTENCIÓN"),
}

# ─── Helper ─────────────────────────────────────────────────────────────────
def fmt_num(n):
    if n >= 1_000_000:
        return f"{n/1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n/1_000:.1f}K"
    return str(n)

def pct(part, total):
    return round(part / total * 100) if total else 0

def cast_vote(issue_id, choice, issue_title):
    prev = st.session_state.votes.get(issue_id)
    if prev:                                          # undo previous
        st.session_state.counts[issue_id][prev] -= 1
    st.session_state.votes[issue_id] = choice
    st.session_state.counts[issue_id][choice] += 1
    st.session_state.mandate_flash = issue_id
    # Add to history (deduplicate by issue_id)
    st.session_state.history = [h for h in st.session_state.history if h["id"] != issue_id]
    st.session_state.history.insert(0, {
        "id": issue_id,
        "title": issue_title,
        "vote": choice,
        "time": datetime.now().strftime("%H:%M"),
        "emoji": next(i["emoji"] for i in ISSUES if i["id"] == issue_id),
    })

# ─── HEADER ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="dv-header">
  <div class="dv-logo-mark">⬆</div>
  <div class="dv-brand">
    <span>DemoVote²</span>
    <small>Decisions powered by people.</small>
  </div>
  <div class="dv-live-pill">● EN VIVO</div>
</div>
""", unsafe_allow_html=True)

# ─── CITIZEN PROFILE ────────────────────────────────────────────────────────
total_votes = len(st.session_state.votes)
st.markdown(f"""
<div class="profile-pill">
  <div class="profile-avatar">👤</div>
  <span class="profile-name">Ciudadano Verificado</span>
  &nbsp;·&nbsp; {total_votes} mandato{'s' if total_votes != 1 else ''} enviado{'s' if total_votes != 1 else ''}
</div>
""", unsafe_allow_html=True)

# ─── STATS BAR ──────────────────────────────────────────────────────────────
all_c = st.session_state.counts
total_mandates = sum(v for c in all_c.values() for v in c.values())
active_issues  = len(ISSUES)
citizens       = total_mandates // 4 + random.randint(0, 50)   # decorative

st.markdown(f"""
<div class="stats-row">
  <div class="stat-chip">
    <div class="stat-num">{fmt_num(total_mandates)}</div>
    <div class="stat-lbl">Mandatos enviados</div>
  </div>
  <div class="stat-chip">
    <div class="stat-num">{active_issues}</div>
    <div class="stat-lbl">Issues activos</div>
  </div>
  <div class="stat-chip">
    <div class="stat-num">{fmt_num(citizens)}</div>
    <div class="stat-lbl">Ciudadanos hoy</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─── TABS ───────────────────────────────────────────────────────────────────
tab_issues, tab_history = st.tabs(["🗳️  Issues activos", "📋  Mi historial"])

# ══════════════════════════════════════════════════════════════════════════════
#  TAB 1 — ISSUES
# ══════════════════════════════════════════════════════════════════════════════
with tab_issues:
    st.markdown('<div class="section-title">Decisiones pendientes en el Congreso</div>', unsafe_allow_html=True)

    for issue in ISSUES:
        iid   = issue["id"]
        cnt   = st.session_state.counts[iid]
        total = cnt["yes"] + cnt["no"] + cnt["abstain"]
        y_p   = pct(cnt["yes"], total)
        n_p   = pct(cnt["no"],  total)
        a_p   = pct(cnt["abstain"], total)
        voted = st.session_state.votes.get(iid)

        # ── Card top ──────────────────────────────────────────────────────
        st.markdown(f"""
        <div class="issue-card">
          <div class="issue-tag {issue['tag_class']}">{issue['tag']}</div>
          <div class="issue-title">{issue['emoji']} {issue['title']}</div>
          <div class="issue-desc">{issue['desc']}</div>
          <div class="issue-meta">
            <span>⏱ {issue['deadline']}</span>
            <span>🗺 {issue['district']}</span>
            <span>👥 {fmt_num(total)} votos</span>
          </div>

          <div class="prog-row">
            <div class="prog-labels">
              <span class="c-yes">A favor {y_p}%</span>
              <span class="c-no">En contra {n_p}%</span>
              <span class="c-abs">Abstención {a_p}%</span>
            </div>
            <div class="prog-bar">
              <div class="prog-yes"     style="width:{y_p}%"></div>
              <div class="prog-no"      style="width:{n_p}%"></div>
              <div class="prog-abstain" style="width:{a_p}%"></div>
            </div>
            <div class="prog-counts">
              <span class="c-yes">{fmt_num(cnt['yes'])}</span>
              <span class="c-no">{fmt_num(cnt['no'])}</span>
              <span class="c-abs">{fmt_num(cnt['abstain'])}</span>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Voted banner OR vote buttons ──────────────────────────────────
        if voted:
            icon, label = VOTE_LABELS[voted]
            color_cls = {"yes": "c-yes", "no": "c-no", "abstain": "c-abs"}[voted]
            st.markdown(f"""
            <div class="voted-banner">
              <span class="voted-icon">{icon}</span>
              Tu mandato: <strong class="{color_cls}">{label}</strong> — enviado al Congreso ✓
            </div>
            """, unsafe_allow_html=True)

            if st.session_state.mandate_flash == iid:
                st.markdown('<div class="mandate-flash">⬆ Mandato ciudadano enviado al Congreso en tiempo real</div>', unsafe_allow_html=True)
                st.session_state.mandate_flash = None

            # Allow changing vote
            with st.expander("Cambiar mi voto"):
                c1, c2, c3 = st.columns(3)
                if c1.button("✅ A favor",    key=f"y2_{iid}"): cast_vote(iid, "yes",     issue["title"]); st.rerun()
                if c2.button("❌ En contra",  key=f"n2_{iid}"): cast_vote(iid, "no",      issue["title"]); st.rerun()
                if c3.button("⬜ Abstención", key=f"a2_{iid}"): cast_vote(iid, "abstain", issue["title"]); st.rerun()
        else:
            col1, col2, col3 = st.columns(3)
            if col1.button("✅  A FAVOR",    key=f"y_{iid}", use_container_width=True):
                cast_vote(iid, "yes",     issue["title"]); st.rerun()
            if col2.button("❌  EN CONTRA",  key=f"n_{iid}", use_container_width=True):
                cast_vote(iid, "no",      issue["title"]); st.rerun()
            if col3.button("⬜  ABSTENCIÓN", key=f"a_{iid}", use_container_width=True):
                cast_vote(iid, "abstain", issue["title"]); st.rerun()

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  TAB 2 — HISTORY
# ══════════════════════════════════════════════════════════════════════════════
with tab_history:
    st.markdown('<div class="section-title">Mis mandatos enviados</div>', unsafe_allow_html=True)

    if not st.session_state.history:
        st.markdown("""
        <div style="text-align:center; padding:3rem 1rem; color:#7986a6;">
          <div style="font-size:2.5rem; margin-bottom:1rem">🗳️</div>
          <div style="font-family:'Syne',sans-serif; font-size:1rem; font-weight:600; color:#e8eaf6;">
            Aún no has enviado mandatos
          </div>
          <div style="font-size:0.85rem; margin-top:0.4rem">
            Ve a "Issues activos" y participa en las decisiones del Congreso.
          </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        vote_labels_map = {"yes": ("A FAVOR", "h-yes"), "no": ("EN CONTRA", "h-no"), "abstain": ("ABSTENCIÓN", "h-abs")}
        items_html = ""
        for h in st.session_state.history:
            label, cls = vote_labels_map[h["vote"]]
            items_html += f"""
            <div class="history-item">
              <div class="h-icon">{h['emoji']}</div>
              <div class="h-title">{h['title']}</div>
              <div class="h-vote {cls}">{label}</div>
              <div class="h-time">{h['time']}</div>
            </div>
            """
        st.markdown(items_html, unsafe_allow_html=True)

        st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="text-align:center; font-size:0.8rem; color:#7986a6;">
          {len(st.session_state.history)} de {len(ISSUES)} issues respondidos
          &nbsp;·&nbsp; Tu participación impulsa la democracia directa.
        </div>
        """, unsafe_allow_html=True)

# ─── Footer ─────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; margin-top:3rem; padding-top:1.5rem;
     border-top:1px solid #1e2540; font-size:0.72rem; color:#4a5568;">
  DemoVote² · Prototype v0.1 · Decisions powered by people.
</div>
""", unsafe_allow_html=True)
