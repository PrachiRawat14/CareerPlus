
import streamlit as st
import pandas as pd
import re

st.set_page_config(
    page_title="Career Plus+",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- DESIGN ----------
st.markdown("""
<style>
.stApp { background: #F5F7FC; }
[data-testid="stSidebar"] {
    background: #142650;
}
[data-testid="stSidebar"] * { color: white; }
.block-container { padding-top: 2rem; }
h1, h2, h3 { color: #142650; }
.hero {
    padding: 28px;
    border-radius: 18px;
    background: linear-gradient(120deg, #142650, #3159A5);
    color: white;
    margin-bottom: 22px;
}
.hero h1, .hero p { color: white; }
.kpi {
    background: white;
    border: 1px solid #E2E8F2;
    border-radius: 14px;
    padding: 18px;
}
.kpi-label { color: #64718A; font-size: 14px; }
.kpi-value {
    color: #142650;
    font-size: 28px;
    font-weight: 800;
}
div[data-testid="stMetric"] {
    background: white;
    padding: 16px;
    border-radius: 12px;
    border: 1px solid #E2E8F2;
}
.stButton button {
    border-radius: 9px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# ---------- DATA ----------
ROLE_SKILLS = {
    "Data Analyst": [
        "Python", "SQL", "Excel", "Power BI", "Statistics"
    ],
    "Machine Learning Engineer": [
        "Python", "NumPy", "Pandas", "Scikit-learn", "Statistics"
    ],
    "Web Developer": [
        "HTML", "CSS", "JavaScript", "React", "SQL"
    ]
}

LEARNING = {
    "Python": "Practice Python fundamentals, pandas and data cleaning.",
    "SQL": "Learn SELECT, JOIN, GROUP BY and subqueries.",
    "Excel": "Practice formulas, PivotTables and data cleaning.",
    "Power BI": "Learn dashboards, data modelling and DAX.",
    "Statistics": "Study averages, distributions and hypothesis testing.",
    "NumPy": "Practice arrays and numerical operations.",
    "Pandas": "Learn DataFrames, filtering and data cleaning.",
    "Scikit-learn": "Explore preprocessing and basic ML models.",
    "HTML": "Learn semantic HTML and page structure.",
    "CSS": "Practice Flexbox, layouts and responsive design.",
    "JavaScript": "Learn functions, events and DOM manipulation.",
    "React": "Learn components, props and state."
}

INTERVIEW_QUESTIONS = {
    "Data Analyst": [
        ("What is data analysis?",
         "Data analysis is the process of inspecting and interpreting data to find useful insights."),
        ("What is the difference between WHERE and HAVING?",
         "WHERE filters rows before grouping; HAVING filters grouped results."),
        ("What is a primary key?",
         "A primary key uniquely identifies each record in a table."),
        ("What is a PivotTable?",
         "A PivotTable summarizes and analyzes data in Excel."),
        ("What is the difference between mean and median?",
         "Mean is the arithmetic average; median is the middle value in sorted data.")
    ],
    "Machine Learning Engineer": [
        ("What is machine learning?",
         "Machine learning enables systems to learn patterns from data."),
        ("What is overfitting?",
         "Overfitting occurs when a model learns training data too closely and generalizes poorly."),
        ("What is a feature?",
         "A feature is an input variable used by a model."),
        ("What is train-test split?",
         "It separates data for model training and evaluation."),
        ("What is classification?",
         "Classification predicts a category or class.")
    ],
    "Web Developer": [
        ("What is HTML?",
         "HTML defines the structure of a web page."),
        ("What is CSS?",
         "CSS controls the appearance and layout of a web page."),
        ("What is JavaScript?",
         "JavaScript adds behavior and interactivity to web pages."),
        ("What is React?",
         "React is a JavaScript library for building user interfaces."),
        ("What is an API?",
         "An API defines how software components communicate.")
    ]
}

# ---------- SESSION STATE ----------
defaults = {
    "student_name": "",
    "email": "",
    "education": "MCA",
    "target_role": "Data Analyst",
    "selected_skills": ["Python", "SQL", "Excel"],
    "assessment": {},
    "completed_tasks": [],
    "resume_text": "",
    "question_index": 0,
    "revealed_answers": []
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ---------- SIDEBAR ----------
st.sidebar.markdown("# 🎯 Career Plus+")
st.sidebar.caption("Your career growth companion")
st.sidebar.divider()

pages = [
    "Home",
    "Student Profile",
    "Skill Assessment",
    "Dashboard",
    "AI Roadmap",
    "Resume Analyzer",
    "Interview Questions",
    "Progress Tracker"
]

page = st.sidebar.radio("NAVIGATION", pages)

st.sidebar.divider()
st.sidebar.markdown("### Your Career Goal")
st.sidebar.write(st.session_state.target_role)
st.sidebar.caption("Prototype version · 1.0")

# ---------- REUSABLE HELPERS ----------
def page_header(title, description):
    st.title(title)
    st.caption(description)
    st.divider()

def current_skills():
    return st.session_state.selected_skills

def skill_results():
    required = ROLE_SKILLS[st.session_state.target_role]
    selected = current_skills()
    matched = [s for s in required if s in selected]
    missing = [s for s in required if s not in selected]
    score = round(len(matched) / len(required) * 100)
    return required, matched, missing, score

def show_kpis(score, matched, required, missing):
    a, b, c = st.columns(3)
    a.metric("Skill Match", f"{score}%")
    b.metric("Skills Matched", f"{len(matched)}/{len(required)}")
    c.metric("Skills to Develop", len(missing))
    st.progress(score / 100)

# ---------- HOME ----------
if page == "Home":
    st.markdown("""
    <div class="hero">
      <h1>Welcome to Career Plus+</h1>
      <p>Your personal space to assess skills, improve your resume
      and prepare for your dream career.</p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Your career journey starts here")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### 🎯 Skill Assessment")
        st.write("Understand your strengths and identify skill gaps.")
    with col2:
        st.markdown("### 📄 Resume Analyzer")
        st.write("Review your resume text and check relevant keywords.")
    with col3:
        st.markdown("### 🚀 AI Roadmap")
        st.write("Get a suggested learning path for your target role.")

    st.divider()
    st.subheader("Your current career snapshot")

    required, matched, missing, score = skill_results()
    show_kpis(score, matched, required, missing)

    st.write("")
    if st.button("Open My Dashboard", type="primary"):
        st.session_state["open_dashboard_notice"] = True

    if st.session_state.get("open_dashboard_notice", False):
        st.info("Choose Dashboard from the sidebar to view detailed charts.")

# ---------- STUDENT PROFILE ----------
elif page == "Student Profile":
    page_header(
        "👤 Student Profile",
        "Manage your profile and career preferences."
    )

    with st.form("profile_form"):
        name = st.text_input(
            "Full name", value=st.session_state.student_name
        )
        email = st.text_input(
            "Email address", value=st.session_state.email
        )
        education = st.selectbox(
            "Current education",
            ["BCA", "MCA", "B.Tech", "B.Sc", "Other"],
            index=["BCA", "MCA", "B.Tech", "B.Sc", "Other"].index(
                st.session_state.education
            )
        )
        role = st.selectbox(
            "Target career role",
            list(ROLE_SKILLS.keys()),
            index=list(ROLE_SKILLS.keys()).index(
                st.session_state.target_role
            )
        )

        available_skills = sorted({
            skill
            for skills in ROLE_SKILLS.values()
            for skill in skills
        })

        skills = st.multiselect(
            "Skills you currently know",
            available_skills,
            default=[
                s for s in st.session_state.selected_skills
                if s in available_skills
            ]
        )

        submitted = st.form_submit_button(
            "Save Profile", type="primary"
        )

    if submitted:
        st.session_state.student_name = name
        st.session_state.email = email
        st.session_state.education = education
        st.session_state.target_role = role
        st.session_state.selected_skills = skills
        st.success("Profile updated for this session!")

    st.info(
        "This prototype keeps profile data in session state. "
        "Connect MongoDB later for persistent storage."
    )

# ---------- SKILL ASSESSMENT ----------
elif page == "Skill Assessment":
    page_header(
        "📝 Skill Assessment",
        "Rate your confidence in each skill for your target role."
    )

    required = ROLE_SKILLS[st.session_state.target_role]
    st.write(f"**Target role:** {st.session_state.target_role}")

    with st.form("assessment_form"):
        ratings = {}
        for skill in required:
            ratings[skill] = st.slider(
                f"{skill} proficiency",
                min_value=0,
                max_value=5,
                value=st.session_state.assessment.get(skill, 0),
                help="0 = beginner or no experience; 5 = highly confident"
            )

        submitted = st.form_submit_button(
            "Submit Assessment", type="primary"
        )

    if submitted:
        st.session_state.assessment = ratings
        st.session_state.selected_skills = [
            s for s, rating in ratings.items() if rating >= 3
        ]
        st.success("Assessment saved!")

    if st.session_state.assessment:
        st.subheader("Your proficiency overview")
        assessment_data = pd.DataFrame({
            "Skill": list(st.session_state.assessment.keys()),
            "Confidence (out of 5)": list(
                st.session_state.assessment.values()
            )
        })
        st.bar_chart(
            assessment_data.set_index("Skill")
        )
        st.caption(
            "These are self-reported confidence ratings, "
            "not verified skill test results."
        )

# ---------- DASHBOARD ----------
elif page == "Dashboard":
    page_header(
        "📊 Career Dashboard",
        "Explore your current skill coverage and development needs."
    )

    required, matched, missing, score = skill_results()
    show_kpis(score, matched, required, missing)

    left, right = st.columns(2)

    with left:
        st.subheader("Skill Coverage")
        coverage = pd.DataFrame({
            "Skill": required,
            "Selected": [
                1 if skill in matched else 0
                for skill in required
            ]
        }).set_index("Skill")
        st.bar_chart(coverage)
        st.caption("1 means selected; 0 means not selected.")

    with right:
        st.subheader("Your Skill Status")
        for skill in matched:
            st.success(f"✓ {skill}")
        for skill in missing:
            st.warning(f"Learn next: {skill}")

    st.divider()
    st.subheader("Recommended priorities")
    for index, skill in enumerate(missing, start=1):
        st.markdown(f"**{index}. {skill}**")
        st.write(LEARNING.get(skill, f"Start learning {skill}."))

# ---------- AI ROADMAP ----------
elif page == "AI Roadmap":
    page_header(
        "🚀 Your Learning Roadmap",
        "A suggested sequence based on your current skill gaps."
    )

    required, matched, missing, score = skill_results()

    st.metric("Current skill coverage", f"{score}%")
    st.write(f"**Career goal:** {st.session_state.target_role}")

    if missing:
        st.subheader("Your next learning steps")
        for index, skill in enumerate(missing, start=1):
            with st.expander(f"Step {index}: Learn {skill}", expanded=True):
                st.write(LEARNING.get(skill, f"Learn {skill} fundamentals."))
                st.checkbox(
                    f"I have studied {skill}",
                    key=f"roadmap_{skill}"
                )
    else:
        st.success(
            "All listed skills are selected. Consider advanced topics "
            "and practical portfolio projects."
        )

    st.caption(
        "This roadmap uses predefined rules. It is not generated "
        "by a trained AI model yet."
    )

# ---------- RESUME ANALYZER ----------
elif page == "Resume Analyzer":
    page_header(
        "📄 Resume Analyzer",
        "Upload a resume to check for target-role skill keywords."
    )

    uploaded_file = st.file_uploader(
        "Upload your resume",
        type=["txt", "pdf", "docx"]
    )

    if uploaded_file:
        filename = uploaded_file.name.lower()
        resume_text = ""

        try:
            if filename.endswith(".txt"):
                resume_text = uploaded_file.getvalue().decode(
                    "utf-8", errors="ignore"
                )

            elif filename.endswith(".pdf"):
                from pypdf import PdfReader
                reader = PdfReader(uploaded_file)
                resume_text = "\n".join(
                    page.extract_text() or ""
                    for page in reader.pages
                )

            elif filename.endswith(".docx"):
                from docx import Document
                document = Document(uploaded_file)
                resume_text = "\n".join(
                    paragraph.text for paragraph in document.paragraphs
                )

        except ImportError:
            st.error(
                "Install the document-reading packages in your terminal: "
                "pip install pypdf python-docx"
            )
        except Exception as error:
            st.error(f"Could not read this file: {error}")

        if resume_text.strip():
            st.session_state.resume_text = resume_text

    resume_text = st.session_state.resume_text

    if resume_text.strip():
        st.subheader("Extracted Resume Text")
        st.text_area(
            "Review extracted content",
            value=resume_text,
            height=220
        )

        required = ROLE_SKILLS[st.session_state.target_role]
        resume_lower = resume_text.lower()

        found = [
            s for s in required
            if re.search(
                r"(?<!\w)" + re.escape(s.lower()) + r"(?!\w)",
                resume_lower
            )
        ]
        missing = [s for s in required if s not in found]
        score = round(len(found) / len(required) * 100)

        st.subheader("Resume Keyword Overview")
        a, b, c = st.columns(3)
        a.metric("Keyword Coverage", f"{score}%")
        b.metric("Keywords Found", len(found))
        c.metric("Keywords Missing", len(missing))

        st.progress(score / 100)

        for skill in found:
            st.success(f"Found: {skill}")
        for skill in missing:
            st.warning(f"Not found: {skill}")

        st.caption(
            "This checks keyword presence only. It does not judge "
            "resume quality, prove proficiency or use a trained AI model."
        )
    else:
        st.info(
            "Upload a TXT, PDF or DOCX resume to start the keyword check."
        )

# ---------- INTERVIEW QUESTIONS ----------
elif page == "Interview Questions":
    page_header(
        "🎤 Interview Practice",
        "Practise common questions for your chosen career."
    )

    role = st.selectbox(
        "Choose a role for practice",
        list(INTERVIEW_QUESTIONS.keys()),
        index=list(INTERVIEW_QUESTIONS.keys()).index(
            st.session_state.target_role
        ),
        key="interview_role"
    )

    questions = INTERVIEW_QUESTIONS[role]

    if st.session_state.question_index >= len(questions):
        st.session_state.question_index = 0

    index = st.session_state.question_index
    question, answer = questions[index]

    st.progress((index + 1) / len(questions))
    st.caption(f"Question {index + 1} of {len(questions)}")
    st.subheader(question)

    response = st.text_area(
        "Write your answer before revealing the sample answer",
        key=f"response_{role}_{index}",
        height=130
    )

    if st.button("Show Sample Answer"):
        st.session_state.revealed_answers.append(f"{role}_{index}")

    if f"{role}_{index}" in st.session_state.revealed_answers:
        st.info(answer)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Previous Question", disabled=index == 0):
            st.session_state.question_index -= 1
            st.rerun()

    with col2:
        if st.button(
            "Next Question",
            disabled=index == len(questions) - 1,
            type="primary"
        ):
            st.session_state.question_index += 1
            st.rerun()

# ---------- PROGRESS TRACKER ----------
elif page == "Progress Tracker":
    page_header(
        "📈 Progress Tracker",
        "Mark completed learning tasks and monitor your progress."
    )

    tasks = [
        "Revise Python fundamentals",
        "Practise SQL joins and grouping",
        "Complete Excel formulas and PivotTables",
        "Build a Power BI dashboard",
        "Revise basic statistics",
        "Build a data analysis portfolio project"
    ]

    st.write("Tick a task when you complete it.")

    for task in tasks:
        checked = task in st.session_state.completed_tasks
        new_value = st.checkbox(task, value=checked, key=f"task_{task}")

        if new_value and task not in st.session_state.completed_tasks:
            st.session_state.completed_tasks.append(task)
        elif not new_value and task in st.session_state.completed_tasks:
            st.session_state.completed_tasks.remove(task)

    completed = len(st.session_state.completed_tasks)
    total = len(tasks)
    percentage = round(completed / total * 100)

    st.divider()
    a, b, c = st.columns(3)
    a.metric("Tasks Completed", f"{completed}/{total}")
    b.metric("Overall Progress", f"{percentage}%")
    c.metric("Tasks Remaining", total - completed)

    st.progress(percentage / 100)

    if percentage == 100:
        st.balloons()
        st.success("Excellent! You completed every task in this plan.")

    if st.button("Reset Progress"):
        st.session_state.completed_tasks = []
        st.rerun()

# ---------- FOOTER ----------
st.divider()
st.caption(
    "Career Plus+ | Career guidance prototype | "
    "Progress and profile data are currently session-based."
)
