import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import MultiLabelBinarizer

st.set_page_config(page_title="Insights | Career Compass", page_icon="📈", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("data/careers.csv")
    df["skills_list"] = df["required_skills"].str.split(",").apply(
        lambda x: [s.strip() for s in x]
    )
    return df

df = load_data()

st.markdown("# 📈 Data Insights")
st.caption("Key findings from our analysis of 35+ careers across 7 domains.")
st.markdown("---")

m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Careers Analysed",  len(df))
m2.metric("Domains Covered",   df["domain"].nunique())
m3.metric("Highest Salary",    f"₹{df['avg_salary_lpa'].max()} LPA")
m4.metric("Fastest Entry",     f"{df['months_to_ready'].min()} months")
m5.metric("Very High Demand",  df[df["job_demand"]=="Very High"]["role"].count())

st.markdown("---")

# CHART 1 — Salary by domain
st.markdown("### 1. Average Salary by Domain")
st.caption("Which domain pays the most on average?")

salary_avg = df.groupby("domain")["avg_salary_lpa"].mean().reset_index()
salary_avg.columns = ["Domain", "Avg Salary"]
salary_avg = salary_avg.sort_values("Avg Salary", ascending=True)

fig1 = px.bar(
    salary_avg, x="Avg Salary", y="Domain", orientation="h",
    color="Avg Salary",
    color_continuous_scale=["#9FE1CB", "#1D9E75", "#04342C"],
    text=salary_avg["Avg Salary"].apply(lambda x: f"₹{x:.1f} LPA"),
    labels={"Avg Salary": "Average Salary (₹ LPA)"}
)
fig1.update_traces(textposition="outside")
fig1.update_layout(
    coloraxis_showscale=False,
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=0, r=80, t=10, b=10),
    height=340
)
st.plotly_chart(fig1, use_container_width=True)
st.info("**Finding:** Technology and Business domains offer the highest average salaries.")

st.markdown("---")

# CHART 2 — Scatter salary vs time
st.markdown("### 2. Salary vs Time to Become Job-Ready")
st.caption("Is a higher paying career always slower to enter?")

domain_colors = {
    "Technology": "#378ADD", "Design": "#D4537E",
    "Engineering": "#EF9F27", "Business": "#1D9E75",
    "Creative Arts": "#D85A30", "Govt & Law": "#7F77DD",
    "Science & Research": "#639922"
}

fig2 = px.scatter(
    df, x="months_to_ready", y="avg_salary_lpa",
    color="domain", color_discrete_map=domain_colors,
    hover_name="role",
    hover_data={"job_demand": True, "months_to_ready": True, "avg_salary_lpa": True},
    labels={"months_to_ready": "Months to Become Job-Ready", "avg_salary_lpa": "Avg Salary (₹ LPA)"},
    text="role"
)
fig2.update_traces(textposition="top center", textfont_size=8)
fig2.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=0, r=0, t=10, b=10),
    height=450
)
st.plotly_chart(fig2, use_container_width=True)
st.info("**Finding:** Content Creator and Digital Marketer are quick to enter with decent pay. AI/ML Engineering tops salary but requires significant preparation.")

st.markdown("---")

# CHART 3 — Job demand pie
st.markdown("### 3. Job Demand Distribution")

c1, c2 = st.columns([1, 1])

with c1:
    demand_count = df["job_demand"].value_counts().reset_index()
    demand_count.columns = ["Demand Level", "Count"]
    fig3 = px.pie(
        demand_count, names="Demand Level", values="Count",
        color_discrete_sequence=["#1D9E75","#378ADD","#EF9F27","#D85A30","#7F77DD"],
        hole=0.5
    )
    fig3.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=20, b=20),
        height=280
    )
    st.plotly_chart(fig3, use_container_width=True)

with c2:
    st.markdown("#### Demand Breakdown")
    color_map = {"Very High": "#1D9E75", "High": "#378ADD",
                 "Medium": "#EF9F27", "Low": "#D85A30", "Very Low": "#888"}
    for _, row in demand_count.iterrows():
        color = color_map.get(row["Demand Level"], "#888")
        pct = round(row["Count"] / len(df) * 100)
        st.markdown(f"""
        <div style="display:flex; align-items:center; gap:10px; margin-bottom:10px">
            <div style="width:14px; height:14px; border-radius:3px; background:{color}; flex-shrink:0"></div>
            <div style="flex:1; font-size:0.9rem">{row["Demand Level"]}</div>
            <div style="font-weight:600; font-size:0.9rem">{row["Count"]} roles</div>
            <div style="color:#888; font-size:0.85rem">{pct}%</div>
        </div>
        """, unsafe_allow_html=True)

st.info("**Finding:** Over 50% of careers are High or Very High demand.")

st.markdown("---")

# CHART 4 — Top 10 salary
st.markdown("### 4. Top 10 Highest Paying Roles")

top10 = df.nlargest(10, "avg_salary_lpa")[["role", "avg_salary_lpa", "domain"]].copy()

fig4 = px.bar(
    top10.sort_values("avg_salary_lpa"),
    x="avg_salary_lpa", y="role", orientation="h",
    color="domain", color_discrete_map=domain_colors,
    text=top10.sort_values("avg_salary_lpa")["avg_salary_lpa"].apply(lambda x: f"₹{x} LPA"),
    labels={"avg_salary_lpa": "Avg Salary (₹ LPA)", "role": ""}
)
fig4.update_traces(textposition="outside")
fig4.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=0, r=80, t=10, b=10),
    height=360
)
st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")

# CHART 5 — Skill Heatmap
st.markdown("### 5. Skill Overlap Heatmap")
st.caption("Blue = that career requires that skill. Shows which skills appear across multiple careers.")

mlb = MultiLabelBinarizer()
skill_matrix = pd.DataFrame(
    mlb.fit_transform(df["skills_list"]),
    columns=mlb.classes_,
    index=df["role"]
)
common_skills = skill_matrix.columns[skill_matrix.sum() >= 2]
skill_matrix_filtered = skill_matrix[common_skills]

fig5 = px.imshow(
    skill_matrix_filtered,
    color_continuous_scale=["#f8f9fa", "#378ADD"],
    aspect="auto",
    title=""
)
fig5.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=0, r=0, t=10, b=0),
    height=600,
    xaxis=dict(tickfont=dict(size=9)),
    yaxis=dict(tickfont=dict(size=9))
)
fig5.update_coloraxes(showscale=False)
st.plotly_chart(fig5, use_container_width=True)

skill_freq = skill_matrix.sum().sort_values(ascending=False).head(10)
st.markdown("#### Top 10 most common skills across all careers:")
freq_cols = st.columns(5)
for i, (skill, count) in enumerate(skill_freq.items()):
    freq_cols[i % 5].metric(skill.strip(), f"{int(count)} careers")

st.info("**Finding:** Python, Excel, Research and Communication appear across the most career fields.")

st.markdown("---")

# CHART 6 — Survey results
st.markdown("### 6. Student Survey Results")
st.caption("Primary data collected from students on their biggest career challenges.")

survey_data = {
    "Challenge": [
        "Don't know what skills to learn",
        "Too many options, confused",
        "No mentor or guidance",
        "Can't find free resources",
        "Don't know where to start"
    ],
    "Students (%)": [38, 27, 18, 10, 7]
}
survey_df = pd.DataFrame(survey_data)

fig6 = px.bar(
    survey_df.sort_values("Students (%)"),
    x="Students (%)", y="Challenge", orientation="h",
    color="Students (%)",
    color_continuous_scale=["#FAECE7","#D85A30","#4A1B0C"],
    text=survey_df.sort_values("Students (%)")["Students (%)"].apply(lambda x: f"{x}%")
)
fig6.update_traces(textposition="outside")
fig6.update_layout(
    coloraxis_showscale=False,
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=0, r=60, t=10, b=10),
    height=280
)
st.plotly_chart(fig6, use_container_width=True)

st.error("**Key Finding:** 38% of students don't know what skills to learn — this is exactly the problem Career Compass solves.")

st.markdown("---")
st.caption("Data sourced from curated career research and primary student survey. Career Compass · 2024")