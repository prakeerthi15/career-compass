import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Skill Gap | Career Compass", page_icon="📊", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("data/careers.csv")

df = load_data()

st.markdown("# 📊 Skill Gap Analyser")
st.caption("Select your dream career and the skills you already know. We'll show exactly what you are missing.")
st.markdown("---")

st.markdown("### Step 1 — Choose your target career")
col1, col2 = st.columns(2)

with col1:
    domain = st.selectbox("Career Domain", sorted(df["domain"].unique()))
with col2:
    domain_df = df[df["domain"] == domain]
    role = st.selectbox("Specific Role", sorted(domain_df["role"].unique()))

selected = domain_df[domain_df["role"] == role].iloc[0]
required_skills = [s.strip() for s in selected["required_skills"].split(",")]

st.markdown(f"""
<div style="background:#E1F5EE; border-left:4px solid #1D9E75; border-radius:8px;
            padding:12px 16px; margin:12px 0">
    <b style="color:#085041">Target role:</b>
    <span style="color:#085041"> {role} in {domain} · ₹{selected['avg_salary_lpa']} LPA avg · {selected['months_to_ready']} months to ready</span>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

st.markdown("### Step 2 — Select skills you already have")
st.caption(f"This role requires **{len(required_skills)} skills**. Tick the ones you know:")

your_skills = []
num_cols = 3
cols = st.columns(num_cols)
for i, skill in enumerate(required_skills):
    with cols[i % num_cols]:
        if st.checkbox(skill, key=f"skill_{i}"):
            your_skills.append(skill)

st.markdown("---")

if your_skills or st.button("Show full gap (I have 0 skills)"):
    missing_skills = [s for s in required_skills if s not in your_skills]
    pct_done = round(len(your_skills) / len(required_skills) * 100)

    st.markdown("### Step 3 — Your Skill Gap Results")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("✅ Skills You Have",   len(your_skills))
    m2.metric("❌ Skills Missing",    len(missing_skills))
    m3.metric("📈 Readiness",         f"{pct_done}%")
    m4.metric("⏱️ Est. Time Needed",
              f"{round(selected['months_to_ready'] * (1 - pct_done/100))} months")

    st.markdown("#### Your readiness for this career")
    st.progress(pct_done / 100, text=f"{pct_done}% ready ({len(your_skills)} of {len(required_skills)} skills)")

    st.markdown("---")

    left, right = st.columns(2)

    with left:
        st.markdown("#### ✅ Skills You Already Have")
        if your_skills:
            for skill in your_skills:
                st.markdown(f"""
                <div style="background:#E1F5EE; border-left:4px solid #1D9E75;
                            border-radius:6px; padding:8px 14px; margin-bottom:6px;
                            font-size:0.9rem; color:#085041; font-weight:500">
                    ✓ &nbsp;{skill}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("You haven't selected any skills yet!")

    with right:
        st.markdown("#### 🔴 Skills to Learn (Priority Order)")
        if missing_skills:
            for i, skill in enumerate(missing_skills, 1):
                if i <= max(1, len(missing_skills) // 3):
                    bg = "#FAECE7"; border = "#D85A30"; priority = "Learn first"
                elif i <= max(2, 2 * len(missing_skills) // 3):
                    bg = "#FAEEDA"; border = "#BA7517"; priority = "Then this"
                else:
                    bg = "#EEEDFE"; border = "#534AB7"; priority = "Later"

                st.markdown(f"""
                <div style="background:{bg}; border-left:4px solid {border};
                            border-radius:6px; padding:8px 14px; margin-bottom:6px;
                            display:flex; justify-content:space-between; align-items:center">
                    <span style="font-size:0.9rem; font-weight:500; color:#1a1a1a">{i}. {skill}</span>
                    <span style="font-size:0.72rem; color:{border}; font-weight:600">{priority}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("🎉 You already have ALL the required skills! You are job-ready.")

    st.markdown("---")

    st.markdown("#### 📊 Skill Gap Visualisation")
    chart_left, chart_right = st.columns(2)

    with chart_left:
        fig_donut = go.Figure(data=[go.Pie(
            labels=["Skills You Have", "Skills Missing"],
            values=[len(your_skills), len(missing_skills)],
            hole=0.65,
            marker_colors=["#1D9E75", "#D85A30"],
            textinfo="label+percent",
            showlegend=False
        )])
        fig_donut.update_layout(
            annotations=[dict(text=f"{pct_done}%<br>Ready", x=0.5, y=0.5,
                              font_size=18, showarrow=False, font_color="#1D9E75")],
            margin=dict(l=10, r=10, t=30, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            title="Career Readiness"
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    with chart_right:
        if missing_skills:
            priority_data = {
                "Priority": ["Learn First", "Then This", "Later"],
                "Count": [
                    len(missing_skills[:max(1, len(missing_skills)//3)]),
                    len(missing_skills[max(1, len(missing_skills)//3):max(2, 2*len(missing_skills)//3)]),
                    len(missing_skills[max(2, 2*len(missing_skills)//3):])
                ]
            }
            fig_priority = px.bar(
                pd.DataFrame(priority_data),
                x="Priority", y="Count",
                color="Priority",
                color_discrete_sequence=["#D85A30", "#EF9F27", "#7F77DD"],
                title="Missing Skills by Priority",
                text="Count"
            )
            fig_priority.update_traces(textposition="outside")
            fig_priority.update_layout(
                showlegend=False,
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=0, r=0, t=40, b=10),
                height=280
            )
            st.plotly_chart(fig_priority, use_container_width=True)

    st.markdown("---")

    if missing_skills:
        st.markdown("#### 🗓️ Suggested Learning Plan")
        months_left = round(selected["months_to_ready"] * (1 - pct_done / 100))
        weeks_per_skill = max(1, round((months_left * 4) / len(missing_skills)))

        plan_data = []
        for i, skill in enumerate(missing_skills):
            start_week = i * weeks_per_skill + 1
            end_week = start_week + weeks_per_skill - 1
            plan_data.append({
                "Skill": skill,
                "Start": f"Week {start_week}",
                "End": f"Week {end_week}",
                "Duration": f"{weeks_per_skill} week(s)"
            })

        plan_df = pd.DataFrame(plan_data)
        st.dataframe(plan_df, use_container_width=True, hide_index=True)

        st.info(f"💡 You need approximately **{months_left} months** to become job-ready for **{role}**. Go to the **AI Roadmap** page for a detailed personalised plan!")
else:
    st.info("👆 Select the skills you already have above — your gap analysis will appear instantly.")