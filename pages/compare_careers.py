import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Compare | Career Compass", page_icon="⚖️", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("data/careers.csv")

df = load_data()

st.markdown("# ⚖️ Compare Careers")
st.caption("Pick any two careers and compare them side by side.")
st.markdown("---")

col1, mid, col2 = st.columns([5, 1, 5])

with col1:
    st.markdown("### Career A")
    domain1 = st.selectbox("Domain A", sorted(df["domain"].unique()), key="d1")
    role1   = st.selectbox("Role A", sorted(df[df["domain"]==domain1]["role"].unique()), key="r1")

with mid:
    st.markdown("<br><br><br><br>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center; font-size:1.8rem'>⚡</div>", unsafe_allow_html=True)

with col2:
    st.markdown("### Career B")
    domain2 = st.selectbox("Domain B", sorted(df["domain"].unique()), index=1, key="d2")
    role2   = st.selectbox("Role B", sorted(df[df["domain"]==domain2]["role"].unique()), key="r2")

r1 = df[df["role"]==role1].iloc[0]
r2 = df[df["role"]==role2].iloc[0]

st.markdown("---")
st.markdown("### Head-to-Head Comparison")

demand_map = {"Very High": 5, "High": 4, "Medium": 3, "Low": 2, "Very Low": 1}

def stat_card(label, val1, val2, higher_is_better=True):
    try:
        v1 = float(str(val1).replace("₹","").replace(" LPA","").replace(" months",""))
        v2 = float(str(val2).replace("₹","").replace(" LPA","").replace(" months",""))
        if higher_is_better:
            c1 = "#1a3a2a" if v1 >= v2 else "#2a2a2a"
            c2 = "#1a3a2a" if v2 >= v1 else "#2a2a2a"
        else:
            c1 = "#1a3a2a" if v1 <= v2 else "#2a2a2a"
            c2 = "#1a3a2a" if v2 <= v1 else "#2a2a2a"
    except Exception:
        c1 = c2 = "#2a2a2a"

    cols = st.columns([2, 3, 3])
    cols[0].markdown(f"<div style='padding:10px 0; font-size:0.85rem; color:#aaa; font-weight:500'>{label}</div>", unsafe_allow_html=True)
    cols[1].markdown(f"<div style='background:{c1}; border-radius:8px; padding:10px 14px; font-weight:600; font-size:0.95rem; color:#ffffff; border:0.5px solid #3a3a3a'>{val1}</div>", unsafe_allow_html=True)
    cols[2].markdown(f"<div style='background:{c2}; border-radius:8px; padding:10px 14px; font-weight:600; font-size:0.95rem; color:#ffffff; border:0.5px solid #3a3a3a'>{val2}</div>", unsafe_allow_html=True)

header = st.columns([2, 3, 3])
header[0].markdown("")
header[1].markdown(f"**{role1}**")
header[2].markdown(f"**{role2}**")

st.markdown("<hr style='margin:4px 0 12px; border-color:#2a2a2a'>", unsafe_allow_html=True)
stat_card("💰 Avg Salary",      f"₹{r1['avg_salary_lpa']} LPA",   f"₹{r2['avg_salary_lpa']} LPA",   higher_is_better=True)
stat_card("📈 Job Demand",       r1["job_demand"],                  r2["job_demand"])
stat_card("⏱️ Time to Ready",   f"{r1['months_to_ready']} months", f"{r2['months_to_ready']} months", higher_is_better=False)
stat_card("📚 Skills Required",  len(r1["required_skills"].split(",")), len(r2["required_skills"].split(",")), higher_is_better=False)
stat_card("🌐 Domain",           r1["domain"],                      r2["domain"])

st.markdown("---")
st.markdown("### Visual Comparison")

chart1, chart2 = st.columns(2)

with chart1:
    metrics_df = pd.DataFrame({
        "Metric": ["Salary (LPA)", "Months to Ready"],
        role1: [r1["avg_salary_lpa"], r1["months_to_ready"]],
        role2: [r2["avg_salary_lpa"], r2["months_to_ready"]]
    })
    fig = px.bar(
        metrics_df, x="Metric", y=[role1, role2],
        barmode="group",
        color_discrete_sequence=["#1D9E75", "#7F77DD"],
        title="Salary & Time to Ready",
        text_auto=True
    )
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(title=""),
        margin=dict(l=0, r=0, t=40, b=10),
        height=300,
        font=dict(color="#ffffff"),
        xaxis=dict(tickfont=dict(color="#aaa"), gridcolor="#2a2a2a"),
        yaxis=dict(tickfont=dict(color="#aaa"), gridcolor="#2a2a2a"),
    )
    st.plotly_chart(fig, use_container_width=True)

with chart2:
    d1 = demand_map.get(r1["job_demand"], 3)
    d2 = demand_map.get(r2["job_demand"], 3)
    max_salary = df["avg_salary_lpa"].max()
    max_time   = df["months_to_ready"].max()

    categories = ["Salary", "Job Demand", "Speed to Ready", "Skill Simplicity"]
    vals1 = [
        round(r1["avg_salary_lpa"] / max_salary * 10, 1),
        round(d1 / 5 * 10, 1),
        round((1 - r1["months_to_ready"] / max_time) * 10, 1),
        round((1 - len(r1["required_skills"].split(",")) / 12) * 10, 1)
    ]
    vals2 = [
        round(r2["avg_salary_lpa"] / max_salary * 10, 1),
        round(d2 / 5 * 10, 1),
        round((1 - r2["months_to_ready"] / max_time) * 10, 1),
        round((1 - len(r2["required_skills"].split(",")) / 12) * 10, 1)
    ]

    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=vals1 + [vals1[0]], theta=categories + [categories[0]],
        fill="toself", name=role1,
        line_color="#1D9E75", fillcolor="rgba(29,158,117,0.15)"
    ))
    fig_radar.add_trace(go.Scatterpolar(
        r=vals2 + [vals2[0]], theta=categories + [categories[0]],
        fill="toself", name=role2,
        line_color="#7F77DD", fillcolor="rgba(127,119,221,0.15)"
    ))
    fig_radar.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True, range=[0, 10],
                           gridcolor="#2a2a2a", tickfont=dict(color="#666")),
            angularaxis=dict(tickfont=dict(color="#aaa"), gridcolor="#2a2a2a")
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        title="Career Score Radar (out of 10)",
        title_font_color="#ffffff",
        legend=dict(orientation="h", y=-0.1, font=dict(color="#aaa")),
        margin=dict(l=40, r=40, t=50, b=40),
        height=300,
        font=dict(color="#ffffff")
    )
    st.plotly_chart(fig_radar, use_container_width=True)

st.markdown("---")
st.markdown("### 🔗 Skill Overlap Analysis")

skills1 = set(s.strip() for s in r1["required_skills"].split(","))
skills2 = set(s.strip() for s in r2["required_skills"].split(","))
common  = skills1 & skills2
only1   = skills1 - skills2
only2   = skills2 - skills1

ov1, ov2, ov3 = st.columns(3)

with ov1:
    st.markdown(f"**Only in {role1}** ({len(only1)})")
    for s in sorted(only1):
        st.markdown(f"<div style='background:#0f2a1f; border-radius:6px; padding:6px 12px; margin-bottom:5px; font-size:0.85rem; color:#1D9E75; border:0.5px solid #1a3a2a'>● {s}</div>", unsafe_allow_html=True)

with ov2:
    st.markdown(f"**Common to Both** ({len(common)})")
    if common:
        for s in sorted(common):
            st.markdown(f"<div style='background:#1a1535; border-radius:6px; padding:6px 12px; margin-bottom:5px; font-size:0.85rem; color:#7F77DD; border:0.5px solid #2a2050'>⭐ {s}</div>", unsafe_allow_html=True)
        st.success(f"Learning these {len(common)} skills gives you a head-start in both careers!")
    else:
        st.warning("No skill overlap. These are very different career paths.")

with ov3:
    st.markdown(f"**Only in {role2}** ({len(only2)})")
    for s in sorted(only2):
        st.markdown(f"<div style='background:#2a1a05; border-radius:6px; padding:6px 12px; margin-bottom:5px; font-size:0.85rem; color:#EF9F27; border:0.5px solid #3a2a10'>● {s}</div>", unsafe_allow_html=True)

st.markdown("---")
st.markdown("### 🏆 Quick Verdict")

salary_winner = role1 if r1["avg_salary_lpa"] > r2["avg_salary_lpa"] else role2
speed_winner  = role1 if r1["months_to_ready"] < r2["months_to_ready"] else role2
demand_winner = role1 if demand_map.get(r1["job_demand"],3) >= demand_map.get(r2["job_demand"],3) else role2

v1, v2, v3 = st.columns(3)
v1.success(f"💰 Higher salary: **{salary_winner}**")
v2.info(f"⚡ Faster to enter: **{speed_winner}**")
v3.warning(f"📈 More in demand: **{demand_winner}**")

st.info("💡 Not sure which one to choose? Go to the **AI Roadmap** page for a personalised recommendation!")