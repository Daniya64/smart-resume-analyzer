
import streamlit as st
import pandas as pd

from resume_parser import extract_resume_text
from job_matcher import analyze_match

st.set_page_config(
    page_title="Smart Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
}
h1 {
    color: #4F8BF9;
}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("📄 Resume Analyzer")
    st.write("AI-powered resume and job matching")
    st.divider()
    st.info("Upload a PDF resume and job description.")

st.title("Smart Resume Analyzer & Job Matcher")
st.write("Analyze your resume against a job description.")

uploaded_file = st.file_uploader(
    "Upload your resume (PDF)",
    type=["pdf"]
)

job_description = st.text_area(
    "Paste the job description",
    height=200
)

if st.button("Analyze Resume", type="primary"):

    if uploaded_file is None:
        st.error("Please upload your resume PDF.")

    elif not job_description.strip():
        st.error("Please enter a job description.")

    else:
        try:
            with st.spinner("Analyzing resume..."):
                resume_text = extract_resume_text(uploaded_file)
                results = analyze_match(
                    resume_text,
                    job_description
                )

            st.success("Analysis completed!")

            st.subheader("📊 Resume Analysis Results")

            col1, col2 = st.columns(2)

            col1.metric(
                "Text Similarity",
                f"{results['similarity_score']}%"
            )

            col2.metric(
                "Job Skill Coverage",
                f"{results['skill_score']}%"
            )

            st.progress(results["skill_score"] / 100)

            st.subheader("✅ Matching Skills")
            st.write(
                ", ".join(results["matched_skills"])
                or "No matching skills detected."
            )

            st.subheader("📌 Skills to Develop")
            st.write(
                ", ".join(results["missing_skills"])
                or "No missing skills detected."
            )

            st.subheader("🧠 Skills Found in Resume")
            st.write(
                ", ".join(results["resume_skills"])
                or "No skills detected."
            )

            st.subheader("💡 Resume Improvement Suggestions")

            suggestions = []

            if results["missing_skills"]:
                suggestions.append(
                    "Consider learning these skills: "
                    + ", ".join(results["missing_skills"])
                )

            if results["skill_score"] < 50:
                suggestions.append(
                    "Add relevant skills and projects that "
                    "demonstrate your suitability for this role."
                )

            if results["similarity_score"] < 40:
                suggestions.append(
                    "Tailor your resume summary and project "
                    "descriptions to the job requirements."
                )

            if not suggestions:
                suggestions.append(
                    "Review your achievements and quantify "
                    "your project results where possible."
                )

            for suggestion in suggestions:
                st.info(suggestion)

            report = pd.DataFrame({
                "Metric": [
                    "Text Similarity",
                    "Job Skill Coverage"
                ],
                "Score (%)": [
                    results["similarity_score"],
                    results["skill_score"]
                ]
            })

            st.subheader("📈 Score Summary")
            st.bar_chart(
                report.set_index("Metric")
            )

            report_text = f"""SMART RESUME ANALYSIS REPORT

Text Similarity: {results['similarity_score']}%
Job Skill Coverage: {results['skill_score']}%

Resume Skills:
{', '.join(results['resume_skills'])}

Matching Skills:
{', '.join(results['matched_skills'])}

Skills to Develop:
{', '.join(results['missing_skills'])}
"""

            st.download_button(
                "Download Analysis Report",
                data=report_text,
                file_name="resume_analysis_report.txt",
                mime="text/plain"
            )

            st.download_button(
                "Download CSV Report",
                data=report.to_csv(index=False),
                file_name="resume_analysis.csv",
                mime="text/csv"
            )

            with st.expander("View Extracted Resume Text"):
                st.text(resume_text)

        except Exception as error:
            st.error(f"Analysis failed: {error}")
