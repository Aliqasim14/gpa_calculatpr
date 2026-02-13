import streamlit as st
import pandas as pd
from dataclasses import dataclass

@dataclass
class Course:
    name: str
    credit_hours: float
    grade_value: float
    grade_letter: str
    quality_points: float

class GPACalculator:
    def __init__(self):
        # Simple grade to point mapping
        self.grade_map = {
            'A': 4.0,
            'B': 3.0, 
            'C': 2.0,
            'D': 1.0,
            'F': 0.0
        }

    def calculate_course(self, name: str, credit_hours: float, grade_letter: str) -> Course:
        grade_value = self.grade_map.get(grade_letter.upper(), 0.0)
        quality_points = grade_value * credit_hours
        return Course(
            name=name if name else f"Course {len(st.session_state.course_inputs)}",
            credit_hours=credit_hours,
            grade_value=grade_value,
            grade_letter=grade_letter.upper(),
            quality_points=quality_points
        )

# Custom dark theme CSS
def apply_dark_theme():
    st.markdown("""
        <style>
        /* Main background */
        .stApp {
            background-color: #1E1E1E;
            color: #FFFFFF;
        }
        
        /* Headers */
        h1, h2, h3, h4, h5, h6 {
            color: #FFFFFF !important;
        }
        
        /* Text elements */
        p, li, span, div {
            color: #E0E0E0;
        }
        
        /* Input fields */
        .stTextInput > div > div > input {
            background-color: #2D2D2D;
            color: #FFFFFF;
            border-color: #404040;
            border-radius: 5px;
        }
        
        .stNumberInput > div > div > input {
            background-color: #2D2D2D;
            color: #FFFFFF;
            border-color: #404040;
            border-radius: 5px;
        }
        
        /* Fixed Selectbox/Dropdown Styling */
        .stSelectbox > div > div {
            background-color: #2D2D2D !important;
            color: #FFFFFF !important;
            border-color: #404040 !important;
            border-radius: 5px;
        }
        
        .stSelectbox > div > div > div {
            background-color: #2D2D2D !important;
            color: #FFFFFF !important;
        }
        
        /* Dropdown options styling */
        div[data-baseweb="select"] > div {
            background-color: #2D2D2D !important;
            color: #FFFFFF !important;
        }
        
        div[data-baseweb="popover"] {
            background-color: #2D2D2D !important;
            border: 1px solid #404040 !important;
        }
        
        div[data-baseweb="popover"] li {
            background-color: #2D2D2D !important;
            color: #FFFFFF !important;
        }
        
        div[data-baseweb="popover"] li:hover {
            background-color: #404040 !important;
        }
        
        /* Selectbox arrow */
        .stSelectbox svg {
            fill: #FFFFFF !important;
        }
        
        /* Buttons */
        .stButton > button {
            background-color: #404040;
            color: #FFFFFF;
            border: 1px solid #555555;
            border-radius: 5px;
            padding: 10px 20px;
            font-weight: bold;
        }
        
        .stButton > button:hover {
            background-color: #555555;
            color: #FFFFFF;
            border: 1px solid #666666;
        }
        
        /* Primary button */
        .stButton > button[kind="primary"] {
            background-color: #0066CC;
            color: #FFFFFF;
            border: 1px solid #0077FF;
        }
        
        .stButton > button[kind="primary"]:hover {
            background-color: #0077FF;
        }
        
        /* Course entry container */
        .course-container {
            background-color: #2D2D2D;
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #404040;
            margin-bottom: 15px;
        }
        
        /* DataFrames/Tables */
        .stDataFrame {
            background-color: #2D2D2D;
            color: #FFFFFF;
        }
        
        .dataframe {
            background-color: #2D2D2D;
            color: #FFFFFF;
            width: 100%;
        }
        
        .dataframe th {
            background-color: #404040;
            color: #FFFFFF;
            border-color: #555555;
            padding: 10px;
        }
        
        .dataframe td {
            background-color: #2D2D2D;
            color: #FFFFFF;
            border-color: #404040;
            padding: 8px;
        }
        
        /* Course badge */
        .course-badge {
            background-color: #404040;
            color: #FFFFFF;
            padding: 8px 15px;
            border-radius: 20px;
            font-size: 14px;
            display: inline-block;
            margin-bottom: 15px;
        }
        </style>
    """, unsafe_allow_html=True)

def main():
    st.set_page_config(
        page_title="GPA Calculator", 
        page_icon="📚",
        layout="wide"
    )
    
    apply_dark_theme()
    
    st.title("📚 GPA Calculator")
    st.markdown("Calculate your GPA easily.")
    
    # Initialize session state with NO default data
    if 'calculator' not in st.session_state:
        st.session_state.calculator = GPACalculator()
    
    # Start with NO courses - user must add them
    if 'course_inputs' not in st.session_state:
        st.session_state.course_inputs = []  # Empty list - no default courses
    
    if 'show_transcript' not in st.session_state:
        st.session_state.show_transcript = False
    
    # Main content area - no student info section
    col_main, col_actions = st.columns([3, 1])
    
    with col_main:
        st.subheader("📝 Course Details")
        
        # Display course count
        course_count = len(st.session_state.course_inputs)
        st.markdown(f"<span class='course-badge'>📚 Courses Added: {course_count}</span>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Display all course input boxes with numbering starting from 1
        if course_count > 0:
            for i, course in enumerate(st.session_state.course_inputs, 1):  # Start numbering from 1
                with st.container():
                    st.markdown(f"<div class='course-container'>", unsafe_allow_html=True)
                    st.markdown(f"**Course {i}**")  # Shows Course 1, Course 2, etc.
                    
                    col_c1, col_c2, col_c3 = st.columns(3)
                    
                    with col_c1:
                        st.session_state.course_inputs[i-1]["name"] = st.text_input(
                            "Course Name", 
                            value=course["name"],
                            key=f"name_{i}",
                            placeholder="e.g., Mathematics"
                        )
                    
                    with col_c2:
                        st.session_state.course_inputs[i-1]["credits"] = st.number_input(
                            "Credit Hours", 
                            min_value=1.0, 
                            max_value=4.0, 
                            value=course["credits"],
                            step=0.5,
                            key=f"credits_{i}"
                        )
                    
                    with col_c3:
                        grade_options = ['A', 'B', 'C', 'D', 'F']
                        grade_index = grade_options.index(course["grade"]) if course["grade"] in grade_options else 0
                        
                        selected_grade = st.selectbox(
                            "Grade",
                            options=grade_options,
                            index=grade_index,
                            key=f"grade_{i}",
                            help="A=4.0, B=3.0, C=2.0, D=1.0, F=0.0"
                        )
                        st.session_state.course_inputs[i-1]["grade"] = selected_grade
                    
                    st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("👆 Click 'Add Course' to start adding courses")
    
    with col_actions:
        st.subheader("⚡ Actions")
        
        # Add Course button
        if st.button("➕ Add Course", use_container_width=True):
            st.session_state.course_inputs.append({"name": "", "credits": 3.0, "grade": "A"})
            st.rerun()
        
        # Calculate button
        if st.button("🧮 Calculate GPA", use_container_width=True, type="primary"):
            if len(st.session_state.course_inputs) > 0:
                st.session_state.show_transcript = True
            else:
                st.warning("Please add at least one course first")
        
        # Reset button - clears ALL data
        if st.button("🔄 Reset All", use_container_width=True):
            st.session_state.course_inputs = []  # Empty list - no courses
            st.session_state.show_transcript = False
            st.rerun()
        
        # Remove Course button (last course)
        if len(st.session_state.course_inputs) > 0:
            if st.button("❌ Remove Last Course", use_container_width=True):
                st.session_state.course_inputs.pop()
                if len(st.session_state.course_inputs) == 0:
                    st.session_state.show_transcript = False
                st.rerun()
    
    st.markdown("---")
    
    # GPA Transcript Section
    st.header("📊 GPA Transcript")
    
    if st.session_state.show_transcript and st.session_state.course_inputs:
        # Process all courses
        courses = []
        total_quality_points = 0
        total_credits = 0
        
        for input_data in st.session_state.course_inputs:
            if input_data["name"]:  # Only process if there's a course name
                course = st.session_state.calculator.calculate_course(
                    input_data["name"],
                    input_data["credits"],
                    input_data["grade"]
                )
                courses.append(course)
                total_quality_points += course.quality_points
                total_credits += course.credit_hours
        
        if courses:
            # Course table
            table_data = []
            for i, course in enumerate(courses, 1):
                table_data.append({
                    "Course": course.name,
                    "Grade": f"{course.grade_value:.0f}",
                    "Credits": f"{course.credit_hours:.2f}",
                    "Quality Points": f"{course.quality_points:.2f}"
                })
            
            df = pd.DataFrame(table_data)
            st.table(df)
            
            st.markdown("")
            
            # Summary
            gpa = total_quality_points / total_credits if total_credits > 0 else 0
            
            # Format summary
            st.markdown(f"**Total Quality Points**: {total_quality_points:.2f}")
            st.markdown("")
            st.markdown(f"**Total Credits**: {total_credits:.0f}")
            st.markdown("")
            st.markdown(f"**GPA**: {gpa:.2f}")
        else:
            st.info("Please enter course names for all courses")
    
    elif st.session_state.show_transcript:
        st.info("No courses to display")
    else:
        st.info("Add courses and click 'Calculate GPA' to see your transcript")

if __name__ == "__main__":
    main()