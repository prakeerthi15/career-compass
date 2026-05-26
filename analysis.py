import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import os
from sklearn.preprocessing import MultiLabelBinarizer

matplotlib.use("Agg")

os.makedirs("charts", exist_ok=True)

df = pd.read_csv("data/careers.csv")

sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams["figure.dpi"] = 120

print("Running analysis... please wait.")

# CHART 1 — Average Salary by Domain
fig, ax = plt.subplots(figsize=(10, 5))
salary_avg = df.groupby("domain")["avg_salary_lpa"].mean().sort_values()
colors = ["#5DCAA5", "#7F77DD", "#D4537E", "#EF9F27", "#378ADD", "#D85A30", "#639922"]
salary_avg.plot(kind="barh", ax=ax, color=colors)
ax.set_title("Average Salary by Career Domain (₹ LPA)", fontsize=14, fontweight="bold")
ax.set_xlabel("Average Salary (LPA)", fontsize=11)
for i, v in enumerate(salary_avg):
    ax.text(v + 0.1, i, f"₹{v:.1f}", va="center", fontsize=10)
plt.tight_layout()
plt.savefig("charts/chart1_salary_by_domain.png")
plt.close()
print("✅ Chart 1 saved — salary by domain")

# CHART 2 — Job Demand Distribution
fig, ax = plt.subplots(figsize=(7, 7))
demand_count = df["job_demand"].value_counts()
colors_pie = ["#1D9E75", "#378ADD", "#EF9F27", "#D85A30", "#7F77DD"]
ax.pie(demand_count, labels=demand_count.index, autopct="%1.0f%%",
       colors=colors_pie, startangle=140,
       wedgeprops={"edgecolor": "white", "linewidth": 2})
ax.set_title("Job Demand Distribution Across All Careers", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig("charts/chart2_job_demand_pie.png")
plt.close()
print("✅ Chart 2 saved — job demand pie")

# CHART 3 — Months to Job-Ready by Domain
fig, ax = plt.subplots(figsize=(10, 5))
time_avg = df.groupby("domain")["months_to_ready"].mean().sort_values(ascending=False)
bars = ax.bar(time_avg.index, time_avg.values, color="#7F77DD", edgecolor="white")
ax.set_title("Average Months to Become Job-Ready by Domain", fontsize=14, fontweight="bold")
ax.set_ylabel("Months", fontsize=11)
plt.xticks(rotation=25, ha="right", fontsize=10)
for bar in bars:
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
            f"{bar.get_height():.0f}m", ha="center", fontsize=10, fontweight="bold")
plt.tight_layout()
plt.savefig("charts/chart3_months_to_ready.png")
plt.close()
print("✅ Chart 3 saved — time to ready")

# CHART 4 — Salary vs Time to Ready
domain_colors = {
    "Technology": "#378ADD", "Design": "#D4537E",
    "Engineering": "#EF9F27", "Business": "#1D9E75",
    "Creative Arts": "#D85A30", "Govt & Law": "#7F77DD",
    "Science & Research": "#639922"
}
fig, ax = plt.subplots(figsize=(10, 6))
for domain, group in df.groupby("domain"):
    ax.scatter(group["months_to_ready"], group["avg_salary_lpa"],
               label=domain, color=domain_colors.get(domain, "#888"),
               s=100, alpha=0.85, edgecolors="white")
for _, row in df.iterrows():
    ax.annotate(row["role"], (row["months_to_ready"], row["avg_salary_lpa"]),
                fontsize=7.5, alpha=0.7, xytext=(4, 4), textcoords="offset points")
ax.set_title("Salary vs Preparation Time for Every Career", fontsize=14, fontweight="bold")
ax.set_xlabel("Months to Become Job-Ready", fontsize=11)
ax.set_ylabel("Average Salary (₹ LPA)", fontsize=11)
ax.legend(loc="upper right", fontsize=9)
plt.tight_layout()
plt.savefig("charts/chart4_salary_vs_time.png")
plt.close()
print("✅ Chart 4 saved — salary vs time scatter")

# CHART 5 — Top 10 Highest Paying Roles
fig, ax = plt.subplots(figsize=(10, 5))
top10 = df.nlargest(10, "avg_salary_lpa")[["role", "avg_salary_lpa", "domain"]]
role_colors = [domain_colors.get(d, "#888") for d in top10["domain"]]
bars = ax.barh(top10["role"], top10["avg_salary_lpa"], color=role_colors, edgecolor="white")
ax.set_title("Top 10 Highest Paying Career Roles", fontsize=14, fontweight="bold")
ax.set_xlabel("Average Salary (₹ LPA)", fontsize=11)
for bar in bars:
    ax.text(bar.get_width() + 0.2, bar.get_y() + bar.get_height() / 2,
            f"₹{bar.get_width():.0f}", va="center", fontsize=10)
plt.tight_layout()
plt.savefig("charts/chart5_top10_salary.png")
plt.close()
print("✅ Chart 5 saved — top 10 salary")

# CHART 6 — Skill Overlap Heatmap
df["skills_list"] = df["required_skills"].str.split(",").apply(
    lambda x: [s.strip() for s in x])
mlb = MultiLabelBinarizer()
skill_matrix = pd.DataFrame(
    mlb.fit_transform(df["skills_list"]),
    columns=mlb.classes_, index=df["role"])
common_skills = skill_matrix.columns[skill_matrix.sum() >= 2]
skill_matrix_filtered = skill_matrix[common_skills]
fig, ax = plt.subplots(figsize=(18, 10))
sns.heatmap(skill_matrix_filtered, cmap="Blues",
            linewidths=0.3, linecolor="white", ax=ax)
ax.set_title("Skill Overlap Across All Careers", fontsize=14, fontweight="bold")
plt.xticks(rotation=45, ha="right", fontsize=8)
plt.yticks(fontsize=8)
plt.tight_layout()
plt.savefig("charts/chart6_skill_heatmap.png", bbox_inches="tight")
plt.close()
print("✅ Chart 6 saved — skill heatmap")

# CHART 7 — Survey Results
survey_data = {
    "Career Challenge": [
        "Don't know what skills to learn",
        "Too many options, confused",
        "No mentor or guidance",
        "Can't find free resources",
        "Don't know where to start"
    ],
    "Students (%)": [38, 27, 18, 10, 7]
}
survey_df = pd.DataFrame(survey_data)
fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.barh(survey_df["Career Challenge"], survey_df["Students (%)"],
               color="#D85A30", edgecolor="white")
ax.set_title("Biggest Career Challenges Faced by Students", fontsize=13, fontweight="bold")
ax.set_xlabel("Percentage of Students (%)", fontsize=11)
for bar in bars:
    ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height() / 2,
            f"{bar.get_width()}%", va="center", fontsize=10, fontweight="bold")
plt.tight_layout()
plt.savefig("charts/chart7_survey_results.png")
plt.close()
print("✅ Chart 7 saved — survey results")

print("\n" + "=" * 50)
print("All 7 charts saved to /charts folder!")
print("=" * 50)