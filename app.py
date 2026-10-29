
import streamlit as st
import pandas as pd

from resume_parser import extract_resume_text
from job_matcher import analyze_match
from ats_checker import calculate_ats_score


st.set_page_config(
    page_title="Smart Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Smart Resume Analyzer & Job Matcher")
st.write(
    "Analyze your resume, compare it with a job description, "
    "and identify areas for improvement."
)

st.sidebar.title("About")
st.sidebar.write(
    "This application uses text similarity, skill matching, "
    "and keyword coverage to help improve your resume."
)

st.sidebar.info(
    "Upload a text-based PDF resume and paste the job description."
)

uploaded_file = st.file_uploader(
    "Upload Your Resume (PDF)",
    type=["pdf"]
)

job_description = st.text_area(
    "Paste the Job Description",
    height=220,
    placeholder="Paste the complete job description here..."
)

if st.button("Analyze Resume", type="primary"):

    if uploaded_file is None:
        st.error("Please upload your resume PDF.")

    elif not job_description.strip():
        st.error("Please enter a job description.")

    else:
        try:
            with st.spinner("Analyzing your resume..."):

                resume_text = extract_resume_text(uploaded_file)

                if not resume_text.strip():
                    st.error(
                        "No readable text found in the PDF. "
                        "Please upload a text-based PDF."
                    )
                    st.stop()

                results = analyze_match(
                    resume_text,
                    job_description
                )

                ats_score, matched_keywords, missing_keywords = (
                    calculate_ats_score(
                        resume_text,
                        job_description
                    )
                )

            st.success("Resume analysis completed!")

            # Scores
            st.header("📊 Analysis Results")

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Text Similarity",
                f"{results['similarity_score']}%"
            )

            col2.metric(
                "Job Skill Coverage",
                f"{results['skill_score']}%"
            )

            col3.metric(
                "ATS Keyword Coverage",
                f"{ats_score}%"
            )

            st.caption(
                "These are estimates from this application's matching "
                "methods, not official ATS scores or hiring predictions."
            )

            # Skill matching
            st.header("🎯 Skill Matching")

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("✅ Matched Skills")

                if results["matched_skills"]:
                    for skill in results["matched_skills"]:
                        st.write(f"• {skill.title()}")
                else:
                    st.write("No matching skills found.")

            with col2:
                st.subheader("❌ Missing Job Skills")

                if results["missing_skills"]:
                    for skill in results["missing_skills"]:
                        st.write(f"• {skill.title()}")
                else:
                    st.write("No missing skills from the tracked list.")

            st.subheader("🧠 Skills Detected in Your Resume")

            if results["resume_skills"]:
                st.write(
                    ", ".join(
                        skill.title()
                        for skill in results["resume_skills"]
                    )
                )
            else:
                st.write("No skills from the application's tracked list found.")

            # ATS keywords
            st.header("🔎 ATS Keyword Analysis")

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Keywords Found")

                if matched_keywords:
                    st.write(", ".join(matched_keywords))
                else:
                    st.write("No matching keywords found.")

            with col2:
                st.subheader("Keywords Missing")

                if missing_keywords:
                    st.write(", ".join(missing_keywords[:50]))

                    if len(missing_keywords) > 50:
                        st.caption(
                            f"{len(missing_keywords) - 50} more "
                            "keywords are not displayed."
                        )
                else:
                    st.write("No missing keywords detected.")

            # Resume improvement suggestions
            st.header("📝 Resume Improvement Suggestions")

            resume_lower = resume_text.lower()

            sections = {
                "Education": [
                    "education",
                    "qualification",
                    "academic background"
                ],
                "Projects": [
                    "projects",
                    "project experience"
                ],
                "Experience": [
                    "experience",
                    "internship",
                    "work history",
                    "professional experience"
                ],
                "Certifications": [
                    "certifications",
                    "certificates",
                    "courses"
                ],
                "Skills": [
                    "skills",
                    "technical skills",
                    "key skills"
                ]
            }

            missing_sections = []

            for section, keywords in sections.items():
                if not any(
                    keyword in resume_lower
                    for keyword in keywords
                ):
                    missing_sections.append(section)

            if missing_sections:
                st.warning(
                    "Consider adding these sections if relevant "
                    "to your background:"
                )

                for section in missing_sections:
                    st.write(f"• Review or add your {section} section.")
            else:
                st.success(
                    "All five major resume section headings appear "
                    "to be present."
                )

            suggestions = []

            if results["missing_skills"]:
                suggestions.append(
                    "Include relevant missing skills only if you "
                    "actually have those skills."
                )

            if missing_keywords:
                suggestions.append(
                    "Review the missing keywords and naturally include "
                    "relevant ones in your resume where truthful."
                )

            if results["similarity_score"] < 40:
                suggestions.append(
                    "Tailor your summary and project descriptions "
                    "to the responsibilities in the job description."
                )

            if missing_sections:
                suggestions.append(
                    "Check whether any missing resume sections "
                    "are relevant and should be included."
                )

            suggestions.append(
                "Use clear headings, consistent formatting, and "
                "specific project achievements where possible."
            )

            st.subheader("💡 Recommended Actions")

            for suggestion in suggestions:
                st.write(f"• {suggestion}")

            # Score chart
            st.header("📈 Score Comparison")

            chart_data = pd.DataFrame(
                {
                    "Score Type": [
                        "Text Similarity",
                        "Job Skill Coverage",
                        "ATS Keyword Coverage"
                    ],
                    "Score (%)": [
                        results["similarity_score"],
                        results["skill_score"],
                        ats_score
                    ]
                }
            ).set_index("Score Type")

            st.bar_chart(chart_data)

            # Download text report
            report = f"""
SMART RESUME ANALYZER REPORT
============================

Text Similarity: {results['similarity_score']}%
Job Skill Coverage: {results['skill_score']}%
ATS Keyword Coverage: {ats_score}%

RESUME SKILLS
-------------
{', '.join(results['resume_skills']) or 'None detected'}

MATCHED SKILLS
--------------
{', '.join(results['matched_skills']) or 'None detected'}

MISSING JOB SKILLS
------------------
{', '.join(results['missing_skills']) or 'None detected'}

MATCHED KEYWORDS
----------------
{', '.join(matched_keywords) or 'None detected'}

MISSING KEYWORDS
----------------
{', '.join(missing_keywords) or 'None detected'}

MISSING RESUME SECTIONS
-----------------------
{', '.join(missing_sections) or 'None detected'}

RECOMMENDATIONS
---------------
{chr(10).join('- ' + item for item in suggestions)}

Note: Scores are estimates produced by this application.
They are not official ATS scores or hiring predictions.
"""

            st.download_button(
                label="📥 Download Analysis Report (TXT)",
                data=report,
                file_name="resume_analysis_report.txt",
                mime="text/plain"
            )

            # Download CSV report
            csv_data = pd.DataFrame(
                [
                    {
                        "Metric": "Text Similarity",
                        "Score": results["similarity_score"]
                    },
                    {
                        "Metric": "Job Skill Coverage",
                        "Score": results["skill_score"]
                    },
                    {
                        "Metric": "ATS Keyword Coverage",
                        "Score": ats_score
                    }
                ]
            )

            st.download_button(
                label="📥 Download Scores (CSV)",
                data=csv_data.to_csv(index=False),
                file_name="resume_analysis_scores.csv",
                mime="text/csv"
            )

            # Extracted text
            with st.expander("📄 View Extracted Resume Text"):
                st.text(resume_text)

        except Exception as error:
            st.error(
                "Unable to analyze this resume. "
                "Please check that the PDF contains readable text."
            )
            st.exception(error)
