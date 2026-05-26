import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Career Compass",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background-color: #0E0E0E;
}
[data-testid="stMain"] {
    background-color: #0E0E0E;
}
[data-testid="stSidebar"] {
    background-color: #1A1A1A;
    border-right: 0.5px solid #2a2a2a;
}
[data-testid="stSidebarContent"] * {
    color: #ffffff !important;
}
.hero-wrap {
    background: #1A1A1A;
    border: 0.5px solid #2a2a2a;
    border-radius: 16px;
    padding: 36px 32px;
    margin-bottom: 12px;
    position: relative;
    overflow: hidden;
}
.hero-circle1 {
    position: absolute;
    top: -50px; right: -50px;
    width: 220px; height: 220px;
    border-radius: 50%;
    background: #0f2a1f;
}
.hero-circle2 {
    position: absolute;
    bottom: -40px; right: 80px;
    width: 130px; height: 130px;
    border-radius: 50%;
    background: #1a1a2e;
}
.hero-tag {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #2a2a2a;
    border: 0.5px solid #3a3a3a;
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 11px;
    color: #aaa;
    margin-bottom: 16px;
}
.hero-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #1D9E75;
    display: inline-block;
}
.hero-title {
    font-size: 32px;
    font-weight: 600;
    color: #ffffff;
    line-height: 1.25;
    margin-bottom: 12px;
    position: relative;
}
.hero-title span { color: #1D9E75; }
.hero-sub {
    font-size: 14px;
    color: #aaa;
    line-height: 1.75;
    max-width: 460px;
    margin-bottom: 24px;
    position: relative;
}
.stat-card {
    background: #1A1A1A;
    border: 0.5px solid #2a2a2a;
    border-radius: 14px;
    padding: 16px 18px;
    display: flex;
    align-items: center;
    gap: 14px;
}
.stat-icon {
    width: 40px; height: 40px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    flex-shrink: 0;
}
.stat-num {
    font-size: 20px;
    font-weight: 600;
    color: #ffffff;
    line-height: 1;
}
.stat-lbl {
    font-size: 11px;
    color: #666;
    margin-top: 3px;
}
.section-title {
    font-size: 15px;
    font-weight: 600;
    color: #ffffff;
    margin-bottom: 10px;
}
.domain-card {
    background: #1A1A1A;
    border: 0.5px solid #2a2a2a;
    border-radius: 14px;
    padding: 18px;
    height: 100%;
}
.domain-icon {
    width: 42px; height: 42px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    margin-bottom: 12px;
}
.domain-name {
    font-size: 14px;
    font-weight: 600;
    color: #ffffff;
    margin-bottom: 4px;
}
.domain-roles {
    font-size: 11px;
    color: #777;
    margin-bottom: 10px;
}
.domain-pill {
    display: inline-block;
    font-size: 10px;
    padding: 3px 9px;
    border-radius: 20px;
    border: 0.5px solid #333;
    color: #777;
}
.feature-card {
    background: #1A1A1A;
    border: 0.5px solid #2a2a2a;
    border-radius: 14px;
    padding: 18px;
    height: 100%;
}
.feature-icon {
    width: 38px; height: 38px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    margin-bottom: 12px;
}
.feature-title {
    font-size: 13px;
    font-weight: 600;
    color: #ffffff;
    margin-bottom: 5px;
}
.feature-desc {
    font-size: 12px;
    color: #777;
    line-height: 1.65;
}
.feature-tag {
    display: inline-block;
    font-size: 10px;
    padding: 3px 9px;
    border-radius: 20px;
    margin-top: 10px;
    font-weight: 500;
}
.ai-card {
    background: #1A1A1A;
    border: 0.5px solid #2a2a2a;
    border-radius: 14px;
    padding: 20px;
    height: 100%;
}
.footer-txt {
    text-align: center;
    font-size: 12px;
    color: #444;
    padding: 16px 0 4px;
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    return pd.read_csv("data/careers.csv")

df = load_data()

# ── HERO ───────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
    <div class="hero-circle1"></div>
    <div class="hero-circle2"></div>
    <div class="hero-tag">
        <span class="hero-dot"></span>
        AI-Powered Career Guidance Platform
    </div>
    <div class="hero-title">
        Your career starts with<br>the <span>right roadmap</span>
    </div>
    <div class="hero-sub">
        Explore 35+ career roles across 7 domains. Know exactly what skills
        you need, what you are missing, and get a personalised plan built
        just for you by AI — all in one place.
    </div>
</div>
""", unsafe_allow_html=True)

# ── STATS ──────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-icon" style="background:#0f2a1f">💼</div>
        <div><div class="stat-num">{len(df)}+</div><div class="stat-lbl">Roles mapped</div></div>
    </div>""", unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-icon" style="background:#0c1e35">🌐</div>
        <div><div class="stat-num">{df['domain'].nunique()}</div><div class="stat-lbl">Career domains</div></div>
    </div>""", unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-icon" style="background:#2a1f0a">💰</div>
        <div><div class="stat-num">₹{round(df['avg_salary_lpa'].mean(),1)}L</div><div class="stat-lbl">Avg salary</div></div>
    </div>""", unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-icon" style="background:#2a1209">⚡</div>
        <div><div class="stat-num">{df['months_to_ready'].min()} mo</div><div class="stat-lbl">Fastest entry</div></div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── DOMAINS ────────────────────────────────────────────────
st.markdown('<div class="section-title">Explore career domains</div>', unsafe_allow_html=True)

domain_info = {
    "Technology":         ("#0c1e35", "#185FA5", "💻", "Dev · AI · Data · Cloud"),
    "Design":             ("#2a0f1a", "#99355A", "🎨", "UI/UX · Graphic · Motion"),
    "Engineering":        ("#2a1a05", "#854F0B", "⚙️",  "Civil · Mech · Robotics"),
    "Business":           ("#0f2a1f", "#0F6E56", "📈", "MBA · CA · Marketing"),
    "Creative Arts":      ("#2a1209", "#993C1D", "🎬", "Film · Music · Content"),
    "Govt & Law":         ("#1a1535", "#3C3489", "⚖️",  "IAS · UPSC · Lawyer"),
    "Science & Research": ("#1a2a0a", "#3B6D11", "🔬", "Research · Biotech"),
}

d_cols = st.columns(4)
for i, (domain, (bg, color, icon, roles)) in enumerate(domain_info.items()):
    count = len(df[df["domain"] == domain])
    with d_cols[i % 4]:
        st.markdown(f"""
        <div class="domain-card">
            <div class="domain-icon" style="background:{bg}">{icon}</div>
            <div class="domain-name">{domain}</div>
            <div class="domain-roles">{roles}</div>
            <div class="domain-pill">{count} roles</div>
        </div>
        <br>
        """, unsafe_allow_html=True)

# ── FEATURES ───────────────────────────────────────────────
st.markdown('<div class="section-title">What you can do</div>', unsafe_allow_html=True)

f1, f2, f3, f4 = st.columns(4)

with f1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon" style="background:#0f2a1f">🗺️</div>
        <div class="feature-title">Explore roles</div>
        <div class="feature-desc">Pick any domain and role to see the full skill roadmap — what to learn, in what order, with which tools.</div>
        <span class="feature-tag" style="background:#0f2a1f;color:#1D9E75">35 roadmaps ready</span>
    </div>""", unsafe_allow_html=True)

with f2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon" style="background:#1a1535">🎯</div>
        <div class="feature-title">Skill gap analyser</div>
        <div class="feature-desc">Tick skills you already have. See your readiness %, missing skills by priority, and a week-by-week plan.</div>
        <span class="feature-tag" style="background:#1a1535;color:#7F77DD">Real-time analysis</span>
    </div>""", unsafe_allow_html=True)

with f3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon" style="background:#2a1a05">⚖️</div>
        <div class="feature-title">Compare careers</div>
        <div class="feature-desc">Pick two careers and compare salary, demand, time to ready, and skill overlap side by side.</div>
        <span class="feature-tag" style="background:#2a1a05;color:#EF9F27">Radar + bar charts</span>
    </div>""", unsafe_allow_html=True)

with f4:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon" style="background:#2a1209">📈</div>
        <div class="feature-title">Data insights</div>
        <div class="feature-desc">6 interactive charts — salary trends, skill heatmap, job demand, and survey results.</div>
        <span class="feature-tag" style="background:#2a1209;color:#D85A30">6 charts</span>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── BOTTOM ROW ─────────────────────────────────────────────
left, right = st.columns([2, 1])

with left:
    st.markdown('<div class="section-title">Average salary by domain</div>', unsafe_allow_html=True)
    salary_df = df.groupby("domain")["avg_salary_lpa"].mean().reset_index()
    salary_df.columns = ["Domain", "Avg Salary"]
    salary_df = salary_df.sort_values("Avg Salary", ascending=True)

    fig = px.bar(
        salary_df,
        x="Avg Salary", y="Domain", orientation="h",
        color="Domain",
        color_discrete_map={
            "Technology": "#378ADD",
            "Business": "#1D9E75",
            "Govt & Law": "#7F77DD",
            "Science & Research": "#639922",
            "Engineering": "#EF9F27",
            "Design": "#D4537E",
            "Creative Arts": "#D85A30",
        },
        text=salary_df["Avg Salary"].apply(lambda x: f"₹{x:.1f}"),
    )
    fig.update_traces(textposition="outside", textfont_color="#ffffff")
    fig.update_layout(
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=60, t=10, b=10),
        height=300,
        xaxis=dict(showgrid=True, gridcolor="#2a2a2a",
                   tickfont=dict(color="#666"), title=""),
        yaxis=dict(showgrid=False, tickfont=dict(color="#aaa"), title=""),
        font=dict(color="#aaa", size=12)
    )
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.markdown("""
    <div class="ai-card">
        <div style="width:46px;height:46px;border-radius:12px;background:#1a1535;
                    display:flex;align-items:center;justify-content:center;
                    font-size:22px;margin-bottom:14px">🤖</div>
        <div style="font-size:15px;font-weight:600;color:#fff;margin-bottom:8px">AI roadmap generator</div>
        <div style="font-size:12px;color:#777;line-height:1.7;margin-bottom:16px">
            Fill a short form. Claude AI reads your background, skills, time and budget
            and writes a personalised month-by-month career plan just for you.
        </div>
        <div style="background:#1a1535;border-radius:10px;padding:12px;margin-bottom:14px">
            <div style="font-size:11px;color:#7F77DD;font-weight:500;margin-bottom:4px">✨ Powered by Claude AI</div>
            <div style="font-size:11px;color:#534AB7">Anthropic's latest model generates your plan</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚀 Generate My Roadmap", use_container_width=True, type="primary"):
        st.switch_page("pages/ai_roadmap.py")

# ── FOOTER ─────────────────────────────────────────────────
st.markdown("---")
st.markdown('<div class="footer-txt">Career Compass · Built with Python, Streamlit & Claude AI · Made for students 🎓</div>', unsafe_allow_html=True)