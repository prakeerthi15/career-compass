import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI Roadmap | Career Compass", page_icon="🤖", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("data/careers.csv")

df = load_data()

st.markdown("# 🤖 AI Career Roadmap Generator")
st.markdown("""
<div style="background:#1a1535; border-left:4px solid #7F77DD; border-radius:8px;
            padding:12px 16px; margin-bottom:1rem">
    <b style="color:#7F77DD">Intelligent Rule-Based Career Guidance System</b>
    <span style="color:#aaa"> — Fill in your details and get a personalised
    month-by-month career roadmap generated just for you instantly.</span>
</div>
""", unsafe_allow_html=True)
st.markdown("---")

st.markdown("### Tell us about yourself")

left, right = st.columns(2)

with left:
    name = st.text_input("👤 Your name", placeholder="e.g. Arjun Sharma")
    stream = st.selectbox("📚 Your current stream", [
        "PCM (Physics, Chemistry, Math)",
        "PCB (Physics, Chemistry, Biology)",
        "Commerce",
        "Arts / Humanities",
        "Computer Science (11th-12th)",
        "Currently in College",
        "Graduated",
        "Other"
    ])
    domain = st.selectbox("🌐 Your target domain", sorted(df["domain"].unique()))
    dream_career = st.selectbox("🎯 Your dream career",
        sorted(df[df["domain"] == domain]["role"].unique()))
    current_skills = st.multiselect("💡 Skills you already know",
        options=[s.strip() for s in
                 df[df["role"] == dream_career].iloc[0]["required_skills"].split(",")]
        if dream_career else [])

with right:
    hours_per_day = st.slider("⏰ Study hours available per day", 1, 10, 3)
    months = st.slider("📅 Months you can dedicate", 1, 36, 6)
    budget = st.selectbox("💸 Learning budget", [
        "Free only (YouTube, free courses)",
        "Low (under ₹5,000 total)",
        "Medium (₹5,000 – ₹20,000)",
        "High (paid bootcamps, coaching)"
    ])
    college_or_work = st.selectbox("🏫 Current situation", [
        "Just finished 12th",
        "Currently in college (1st / 2nd year)",
        "Final year student",
        "Working and switching careers",
        "Gap year / preparing full time"
    ])
    goal = st.selectbox("🏆 Your main goal", [
        "Get an internship",
        "Get a full time job",
        "Crack competitive exam",
        "Start freelancing",
        "Build my own startup",
        "Higher studies abroad"
    ])

st.markdown("---")

if st.button("🚀 Generate My Personalised Roadmap", type="primary", use_container_width=True):
    if not dream_career:
        st.error("Please select your dream career first.")
    else:
        # ── Get career data ────────────────────────────────
        selected = df[df["role"] == dream_career].iloc[0]
        all_skills = [s.strip() for s in selected["required_skills"].split(",")]
        tools_list = [t.strip() for t in selected["tools"].split(",")]
        missing_skills = [s for s in all_skills if s not in current_skills]
        readiness = round(len(current_skills) / len(all_skills) * 100) if all_skills else 0

        # ── Adjust timeline based on hours per day ─────────
        base_months = selected["months_to_ready"]
        if hours_per_day >= 6:
            adjusted_months = round(base_months * 0.7)
            pace = "fast"
        elif hours_per_day >= 3:
            adjusted_months = base_months
            pace = "steady"
        else:
            adjusted_months = round(base_months * 1.4)
            pace = "slow"
        adjusted_months = max(1, min(adjusted_months, months))

        # ── Personalised opening message ───────────────────
        stream_msg = {
            "PCM (Physics, Chemistry, Math)": "Your strong math and analytical background gives you a great foundation",
            "PCB (Physics, Chemistry, Biology)": "Your science background gives you strong research and analytical skills",
            "Commerce": "Your commerce background gives you a strong understanding of business and finance",
            "Arts / Humanities": "Your arts background gives you strong creative and communication skills",
            "Computer Science (11th-12th)": "Your CS background gives you a huge head start in the technical aspects",
            "Currently in College": "Being in college gives you the perfect time to build skills alongside your degree",
            "Graduated": "As a graduate you can now focus completely on building your career skills",
            "Other": "Your unique background brings a fresh perspective to this career path"
        }
        opening = stream_msg.get(stream, "Your background gives you a great starting point")

        # ── Budget based resources ─────────────────────────
        resources = {
            "Technology": {
                "free": ["CS50 on edX (free)", "Krish Naik YouTube", "Corey Schafer YouTube", "freeCodeCamp", "Kaggle free courses"],
                "paid": ["Udemy courses (₹499 sale)", "iNeuron bootcamp", "PW Skills", "Scaler Academy", "Newton School"]
            },
            "Design": {
                "free": ["DesignCourse YouTube", "Figma tutorials YouTube", "Google UX Design (Coursera audit)", "Canva Design School", "Adobe free tutorials"],
                "paid": ["Interaction Design Foundation", "Designboat India", "Udemy UI/UX courses", "NID online courses", "Skillshare"]
            },
            "Engineering": {
                "free": ["NPTEL free courses", "MIT OpenCourseWare", "Engineering Funda YouTube", "GATE Wallah YouTube", "Unacademy free classes"],
                "paid": ["MADE Easy", "ACE Academy", "Testbook Pro", "Unacademy Pro", "GATE preparation books"]
            },
            "Business": {
                "free": ["CA Foundation ICAI material", "Commerce Wallah YouTube", "Unacademy Commerce", "MBA Wallah YouTube", "IIM free courses"],
                "paid": ["Unacademy Pro", "Testbook Pro", "CA coaching classes", "MBA coaching", "BYJU's Commerce"]
            },
            "Creative Arts": {
                "free": ["Film Riot YouTube", "Premiere Gal YouTube", "SoundOnSound tutorials", "Lesterbanks", "Motion Array free tutorials"],
                "paid": ["MasterClass", "Skillshare", "Film Connection", "Berklee Online", "LinkedIn Learning"]
            },
            "Govt & Law": {
                "free": ["Drishti IAS YouTube", "StudyIQ YouTube", "Unacademy UPSC free", "Vision IAS free content", "InsightsIAS"],
                "paid": ["Vision IAS", "Drishti IAS", "Vajiram & Ravi", "Forum IAS", "GS SCORE"]
            },
            "Science & Research": {
                "free": ["NPTEL", "MIT OpenCourseWare", "Khan Academy", "Coursera audit", "ResearchGate free papers"],
                "paid": ["Coursera certificates", "edX certificates", "BYJU's", "Unacademy", "Testbook"]
            }
        }

        domain_resources = resources.get(selected["domain"], resources["Technology"])
        if "Free" in budget:
            resource_list = domain_resources["free"]
        else:
            resource_list = domain_resources["free"][:3] + domain_resources["paid"][:2]

        # ── Career difficulty and tips ─────────────────────
        difficulty_tips = {
            "High": "This is a competitive field — consistency beats intensity. Even 2 hours daily compounds massively over months.",
            "Very High": "Demand is very high for this role — companies are actively hiring. Your timing is perfect.",
            "Medium": "This field rewards depth over breadth. Focus on mastering fewer skills rather than knowing many superficially.",
            "Low": "While entry numbers are lower, those who do enter find stable and rewarding careers. Quality over quantity."
        }
        demand_tip = difficulty_tips.get(selected["job_demand"], "Focus on building a strong portfolio to stand out.")

        # ── Goal based advice ──────────────────────────────
        goal_advice = {
            "Get an internship": "Focus on building 1-2 strong projects and apply on Internshala, LinkedIn, and AngelList. Most internships don't require expert skills — just enthusiasm and basics.",
            "Get a full time job": "Target campus placements if in college, or apply on Naukri, LinkedIn, and company career pages. Build a GitHub portfolio and practice interview questions.",
            "Crack competitive exam": "Make a strict daily schedule. Previous year papers are your best friend. Join a test series 2 months before the exam.",
            "Start freelancing": "Start on Fiverr and Upwork with small projects. Build a portfolio of 3-5 projects first. Your first client is the hardest — after that it gets easier.",
            "Build my own startup": "Talk to 10 potential customers before building anything. Validate the problem first. Use your technical skills to build an MVP quickly.",
            "Higher studies abroad": "Focus on GRE/GMAT scores, research papers if possible, and a strong Statement of Purpose. Start 18 months before your target intake."
        }
        goal_tip = goal_advice.get(goal, "Stay consistent and track your progress weekly.")

        # ── Generate month by month plan ───────────────────
        weeks_per_skill = max(1, round((adjusted_months * 4) / max(len(missing_skills), 1)))
        phases = []
        skills_per_phase = max(1, len(missing_skills) // max(adjusted_months, 1))

        for month in range(1, adjusted_months + 1):
            start_idx = (month - 1) * skills_per_phase
            end_idx = start_idx + skills_per_phase
            phase_skills = missing_skills[start_idx:end_idx]
            if not phase_skills and month == adjusted_months:
                phase_skills = missing_skills[start_idx:]
            if phase_skills:
                phases.append({"month": month, "skills": phase_skills})

        # ── Common mistakes ────────────────────────────────
        mistakes = {
            "Technology": [
                "Jumping between too many languages — pick one and go deep",
                "Only watching tutorials without building real projects",
                "Ignoring communication skills — technical + soft skills win jobs"
            ],
            "Design": [
                "Copying designs without understanding the reasoning behind decisions",
                "Not getting feedback from real users — design for others not yourself",
                "Skipping the research phase and jumping straight to visuals"
            ],
            "Engineering": [
                "Focusing only on theory without practical application",
                "Ignoring soft skills and communication for technical roles",
                "Not joining relevant student clubs or competitions"
            ],
            "Business": [
                "Memorising without understanding — concepts matter more than marks",
                "Not building a network early — LinkedIn from day one",
                "Ignoring current affairs and industry news"
            ],
            "Creative Arts": [
                "Waiting to be perfect before sharing work — put it out early",
                "Not building an online portfolio — your work needs to be visible",
                "Ignoring the business side of creative careers"
            ],
            "Govt & Law": [
                "Starting preparation too late — consistency over 12-24 months wins",
                "Ignoring answer writing practice for essay based exams",
                "Not doing mock tests regularly under timed conditions"
            ],
            "Science & Research": [
                "Not reading research papers early — get comfortable with academic writing",
                "Ignoring networking with professors and researchers",
                "Focusing only on marks rather than actual research skills"
            ]
        }
        career_mistakes = mistakes.get(selected["domain"], mistakes["Technology"])

        # ════════════════════════════════════════════════════
        # DISPLAY THE ROADMAP
        # ════════════════════════════════════════════════════

        st.success(f"✅ Your personalised roadmap for **{dream_career}** is ready!")
        st.markdown("---")

        # Personal message
        st.markdown(f"""
        <div style="background:#0f2a1f; border-left:4px solid #1D9E75; border-radius:8px;
                    padding:16px 20px; margin-bottom:20px">
            <div style="font-size:16px; font-weight:600; color:#1D9E75; margin-bottom:6px">
                Hey {name if name else "there"} 👋
            </div>
            <div style="font-size:13px; color:#aaa; line-height:1.75">
                {opening}. You have chosen <b style="color:#ffffff">{dream_career}</b> —
                a career with <b style="color:#ffffff">{selected['job_demand']}</b> job demand
                and an average salary of <b style="color:#1D9E75">₹{selected['avg_salary_lpa']} LPA</b>.
                Based on your {hours_per_day} hours/day and {months} months available,
                here is your personalised roadmap. {demand_tip}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Key metrics
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("🎯 Career Readiness", f"{readiness}%")
        m2.metric("📚 Skills to Learn", len(missing_skills))
        m3.metric("⏱️ Est. Time", f"{adjusted_months} months")
        m4.metric("💰 Target Salary", f"₹{selected['avg_salary_lpa']} LPA")

        st.progress(readiness / 100,
            text=f"{readiness}% ready — {len(current_skills)} of {len(all_skills)} skills")

        st.markdown("---")

        # Month by month plan
        st.markdown("## 🗓️ Your Month-by-Month Plan")
        for phase in phases:
            month_num = phase["month"]
            phase_skills = phase["skills"]

            if month_num <= adjusted_months * 0.33:
                color = "#0f2a1f"; border = "#1D9E75"; phase_label = "Foundation Phase"
            elif month_num <= adjusted_months * 0.66:
                color = "#2a1a05"; border = "#EF9F27"; phase_label = "Building Phase"
            else:
                color = "#1a1535"; border = "#7F77DD"; phase_label = "Advanced Phase"

            st.markdown(f"""
            <div style="background:{color}; border-left:4px solid {border};
                        border-radius:10px; padding:16px 20px; margin-bottom:12px">
                <div style="font-size:13px; color:{border}; font-weight:600; margin-bottom:4px">
                    Month {month_num} — {phase_label}
                </div>
                <div style="font-size:15px; font-weight:600; color:#ffffff; margin-bottom:8px">
                    Focus: {" · ".join(phase_skills)}
                </div>
                <div style="font-size:12px; color:#aaa; line-height:1.7">
                    📖 <b style="color:#ddd">Learn:</b> {", ".join(phase_skills)}<br>
                    🛠️ <b style="color:#ddd">Practice:</b> Build a small project using {phase_skills[0]}<br>
                    🎯 <b style="color:#ddd">Milestone:</b> Complete {phase_skills[0]} and be able to explain it confidently<br>
                    ⏰ <b style="color:#ddd">Daily target:</b> {hours_per_day} hours — {round(hours_per_day * 0.6)} hrs learning + {round(hours_per_day * 0.4)} hrs practice
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # Skills you already have vs missing
        st.markdown("## 📊 Your Skill Status")
        left_col, right_col = st.columns(2)

        with left_col:
            st.markdown("#### ✅ Skills You Already Have")
            if current_skills:
                for skill in current_skills:
                    st.markdown(f"""
                    <div style="background:#0f2a1f; border-radius:6px; padding:7px 12px;
                                margin-bottom:6px; font-size:0.9rem; color:#1D9E75;
                                border:0.5px solid #1a3a2a">✓ {skill}</div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No skills selected yet — that is okay! Everyone starts from zero.")

        with right_col:
            st.markdown("#### 🎯 Skills to Learn Next")
            for i, skill in enumerate(missing_skills[:6], 1):
                if i <= 2:
                    bg = "#2a1209"; color_s = "#D85A30"; priority = "Learn first"
                elif i <= 4:
                    bg = "#2a1a05"; color_s = "#EF9F27"; priority = "Then this"
                else:
                    bg = "#1a1535"; color_s = "#7F77DD"; priority = "Later"
                st.markdown(f"""
                <div style="background:{bg}; border-radius:6px; padding:7px 12px;
                            margin-bottom:6px; font-size:0.9rem;
                            display:flex; justify-content:space-between; align-items:center;
                            border:0.5px solid #3a3a3a">
                    <span style="color:#ffffff">{i}. {skill}</span>
                    <span style="font-size:0.75rem; color:{color_s}; font-weight:600">{priority}</span>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("---")

        # Tools
        st.markdown("## 🛠️ Tools to Master")
        tool_cols = st.columns(3)
        for i, tool in enumerate(tools_list):
            tool_cols[i % 3].markdown(f"""
            <div style="background:#1e1e1e; border:0.5px solid #3a3a3a; border-radius:8px;
                        padding:10px 14px; margin-bottom:8px; font-size:0.9rem;
                        font-weight:500; color:#ffffff;">
                🔧 {tool}
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # Free resources
        st.markdown("## 📚 Best Free Resources for You")
        for i, resource in enumerate(resource_list, 1):
            st.markdown(f"""
            <div style="background:#1e1e1e; border-left:3px solid #1D9E75;
                        border-radius:6px; padding:10px 14px; margin-bottom:8px;
                        font-size:0.9rem; color:#ffffff">
                {i}. {resource}
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # Salary expectations
        st.markdown("## 💰 Salary Expectations in India")
        s1, s2, s3 = st.columns(3)
        base = selected["avg_salary_lpa"]
        s1.metric("Entry Level (0-1 yr)", f"₹{round(base * 0.6, 1)} LPA")
        s2.metric("Mid Level (2-3 yrs)", f"₹{round(base * 1.0, 1)} LPA")
        s3.metric("Senior Level (5+ yrs)", f"₹{round(base * 1.8, 1)} LPA")

        st.markdown("---")

        # Common mistakes
        st.markdown("## ⚠️ Common Mistakes to Avoid")
        for i, mistake in enumerate(career_mistakes, 1):
            st.markdown(f"""
            <div style="background:#2a1209; border-left:3px solid #D85A30;
                        border-radius:6px; padding:10px 14px; margin-bottom:8px;
                        font-size:0.9rem; color:#ffffff">
                ❌ {mistake}
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # Goal specific advice
        st.markdown("## 🏆 Advice for Your Goal")
        st.markdown(f"""
        <div style="background:#1a1535; border-left:4px solid #7F77DD;
                    border-radius:8px; padding:16px 20px; margin-bottom:16px">
            <div style="font-size:13px; font-weight:600; color:#7F77DD; margin-bottom:6px">
                Your goal: {goal}
            </div>
            <div style="font-size:13px; color:#aaa; line-height:1.75">{goal_tip}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # Final motivational note
        pace_msg = {
            "fast": f"At {hours_per_day} hours per day you are moving fast — just make sure you are building real projects and not just consuming content.",
            "steady": f"At {hours_per_day} hours per day you have a solid pace — consistency is everything. Show up every single day.",
            "slow": f"Even at {hours_per_day} hours per day you will get there — it just takes a bit longer. Slow progress is still progress."
        }

        st.markdown(f"""
        <div style="background:#0f2a1f; border:0.5px solid #1D9E75;
                    border-radius:12px; padding:20px 24px; text-align:center">
            <div style="font-size:18px; margin-bottom:10px">🌟</div>
            <div style="font-size:15px; font-weight:600; color:#1D9E75; margin-bottom:8px">
                Final note for {name if name else "you"}
            </div>
            <div style="font-size:13px; color:#aaa; line-height:1.85; max-width:500px; margin:0 auto">
                {pace_msg.get(pace, "")} The fact that you are planning this carefully already puts you
                ahead of 90% of students. <b style="color:#ffffff">{dream_career}</b> is absolutely
                achievable for you. Trust the process, stay consistent, and remember —
                every expert was once a beginner. You've got this! 💪
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # Download button
        roadmap_text = f"""
CAREER COMPASS — PERSONALISED ROADMAP
======================================
Name: {name if name else "Student"}
Dream Career: {dream_career}
Domain: {selected['domain']}
Generated on: Career Compass

CAREER OVERVIEW
---------------
Average Salary: ₹{selected['avg_salary_lpa']} LPA
Job Demand: {selected['job_demand']}
Time to Ready: {adjusted_months} months
Current Readiness: {readiness}%

SKILLS TO LEARN
---------------
{chr(10).join([f"{i+1}. {s}" for i, s in enumerate(missing_skills)])}

TOOLS TO MASTER
---------------
{chr(10).join([f"- {t}" for t in tools_list])}

MONTH BY MONTH PLAN
-------------------
{chr(10).join([f"Month {p['month']}: {', '.join(p['skills'])}" for p in phases])}

FREE RESOURCES
--------------
{chr(10).join([f"{i+1}. {r}" for i, r in enumerate(resource_list)])}

SALARY EXPECTATIONS
-------------------
Entry Level: ₹{round(base * 0.6, 1)} LPA
Mid Level: ₹{round(base * 1.0, 1)} LPA
Senior Level: ₹{round(base * 1.8, 1)} LPA

COMMON MISTAKES TO AVOID
------------------------
{chr(10).join([f"{i+1}. {m}" for i, m in enumerate(career_mistakes)])}

GOAL ADVICE
-----------
Goal: {goal}
{goal_tip}
"""
        st.download_button(
            label="📥 Download My Roadmap as Text File",
            data=roadmap_text,
            file_name=f"roadmap_{dream_career.replace(' ','_').lower()}.txt",
            mime="text/plain",
            use_container_width=True
        )

st.markdown("---")
st.caption("Career Compass · Intelligent Rule-Based Career Guidance System · Made for students 🎓")