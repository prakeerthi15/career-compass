import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Explore Roles | Career Compass", page_icon="🗺️", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("data/careers.csv")

df = load_data()

st.markdown("# 🗺️ Explore Career Roles")
st.caption("Pick any domain and role to see the complete roadmap — skills, tools, salary and timeline.")
st.markdown("---")

st.sidebar.markdown("### 🎯 Choose a Career")
domain = st.sidebar.selectbox(
    "Step 1: Pick a domain",
    sorted(df["domain"].unique())
)

domain_df = df[df["domain"] == domain]
role = st.sidebar.selectbox(
    "Step 2: Pick a role",
    sorted(domain_df["role"].unique())
)

selected = domain_df[domain_df["role"] == role].iloc[0]
skills_list = [s.strip() for s in selected["required_skills"].split(",")]
tools_list  = [t.strip() for t in selected["tools"].split(",")]

st.markdown(f"## {role}")
st.markdown(f"*{selected['description']}*")
st.markdown("")

col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Avg Salary", f"₹{selected['avg_salary_lpa']} LPA")
col2.metric("📈 Job Demand",  selected["job_demand"])
col3.metric("⏱️ Time to Ready", f"{selected['months_to_ready']} months")
col4.metric("🌐 Domain", domain)

st.markdown("---")

left, right = st.columns([1, 1])

with left:
    st.markdown("### 📋 Skill Roadmap (Learn in This Order)")
    for i, skill in enumerate(skills_list):
        if i == 0:
            bg = "#0f2a1f"; border = "#1D9E75"; color = "#1D9E75"; label = "Start here"
        elif i == len(skills_list) - 1:
            bg = "#1a1535"; border = "#7F77DD"; color = "#7F77DD"; label = "Final skill"
        else:
            bg = "#1e1e1e"; border = "#3a3a3a"; color = "#aaaaaa"; label = f"Step {i+1}"

        st.markdown(f"""
        <div style="background:{bg}; border-left: 4px solid {border};
                    border-radius:8px; padding:10px 14px; margin-bottom:8px;
                    display:flex; align-items:center; gap:12px;">
            <span style="font-size:0.72rem; color:{border}; font-weight:600;
                         min-width:58px;">{label}</span>
            <span style="font-size:0.95rem; font-weight:500; color:#ffffff">{skill}</span>
        </div>
        """, unsafe_allow_html=True)

with right:
    st.markdown("### 🛠️ Tools You Will Use")
    tool_cols = st.columns(2)
    for i, tool in enumerate(tools_list):
        tool_cols[i % 2].markdown(f"""
        <div style="background:#1e1e1e; border:0.5px solid #3a3a3a; border-radius:8px;
                    padding:8px 12px; margin-bottom:8px; font-size:0.9rem;
                    font-weight:500; color:#ffffff;">
            🔧 {tool}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("### 📊 Skills Breakdown")
    skill_levels = []
    n = len(skills_list)
    for i, s in enumerate(skills_list):
        if i < n * 0.33:
            skill_levels.append({"Skill": s, "Level": "Foundation", "Order": i+1})
        elif i < n * 0.66:
            skill_levels.append({"Skill": s, "Level": "Intermediate", "Order": i+1})
        else:
            skill_levels.append({"Skill": s, "Level": "Advanced", "Order": i+1})

    skill_df = pd.DataFrame(skill_levels)
    fig = px.bar(
        skill_df, x="Order", y=[1]*len(skill_df), color="Level",
        text="Skill",
        color_discrete_map={
            "Foundation": "#1D9E75",
            "Intermediate": "#EF9F27",
            "Advanced": "#7F77DD"
        },
        labels={"y": "", "Order": "Learning Order"},
        title="Learning Progression"
    )
    fig.update_traces(textposition="inside", textangle=0)
    fig.update_yaxes(visible=False)
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        height=220,
        margin=dict(l=0, r=0, t=40, b=20),
        legend=dict(orientation="h", y=-0.15,
                    font=dict(color="#aaa")),
        font=dict(color="#ffffff"),
        xaxis=dict(tickfont=dict(color="#aaa"), gridcolor="#2a2a2a"),
        title_font_color="#ffffff"
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

st.markdown("### 💰 How This Role Compares Within " + domain)
domain_salary = domain_df[["role", "avg_salary_lpa"]].copy()
domain_salary["Highlight"] = domain_salary["role"].apply(
    lambda r: "Selected" if r == role else "Other"
)
fig2 = px.bar(
    domain_salary.sort_values("avg_salary_lpa", ascending=True),
    x="avg_salary_lpa", y="role", orientation="h",
    color="Highlight",
    color_discrete_map={"Selected": "#1D9E75", "Other": "#3a3a3a"},
    text=domain_salary.sort_values("avg_salary_lpa", ascending=True)["avg_salary_lpa"].apply(lambda x: f"₹{x}"),
    labels={"avg_salary_lpa": "Avg Salary (LPA)", "role": "Role"}
)
fig2.update_traces(textposition="outside", textfont_color="#ffffff")
fig2.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    showlegend=False,
    margin=dict(l=0, r=60, t=10, b=10),
    height=max(250, len(domain_df) * 45),
    font=dict(color="#ffffff"),
    xaxis=dict(tickfont=dict(color="#aaa"), gridcolor="#2a2a2a"),
    yaxis=dict(tickfont=dict(color="#aaa"), gridcolor="#2a2a2a"),
)
st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")
st.success(f"✅ Interested in **{role}**? Go to the **Skill Gap Analyser** page in the sidebar!")