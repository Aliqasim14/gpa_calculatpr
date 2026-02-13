import streamlit as st
import pandas as pd
from dataclasses import dataclass

@dataclass
class Course:
    name: str
    credit_hours: int
    grade_value: float
    grade_letter: str
    quality_points: float
    input_method: str
    percentage: float = 0.0
    marks_details: dict = None

class GPACalculator:
    def __init__(self):
        # Complete GCUF grading scale (from your image)
        self.grading_scale = [
            (85, 100, 4.00), (84, 84.99, 3.95), (83, 83.99, 3.90),
            (82, 82.99, 3.85), (81, 81.99, 3.80), (80, 80.99, 3.75),
            (79, 79.99, 3.70), (78, 78.99, 3.65), (77, 77.99, 3.60),
            (76, 76.99, 3.55), (75, 75.99, 3.50), (74, 74.99, 3.45),
            (73, 73.99, 3.40), (72, 72.99, 3.35), (71, 71.99, 3.30),
            (70, 70.99, 3.25), (69, 69.99, 3.20), (68, 68.99, 3.15),
            (67, 67.99, 3.10), (66, 66.99, 3.05), (65, 65.99, 3.00),
            (64, 64.99, 2.94), (63, 63.99, 2.88), (62, 62.99, 2.82),
            (61, 61.99, 2.76), (60, 60.99, 2.70), (59, 59.99, 2.63),
            (58, 58.99, 2.56), (57, 57.99, 2.49), (56, 56.99, 2.42),
            (55, 55.99, 2.35), (54, 54.99, 2.28), (53, 53.99, 2.21),
            (52, 52.99, 2.14), (51, 51.99, 2.07), (50, 50.99, 2.00),
            (49, 49.99, 1.90), (48, 48.99, 1.80), (47, 47.99, 1.70),
            (46, 46.99, 1.60), (45, 45.99, 1.50), (44, 44.99, 1.40),
            (43, 43.99, 1.30), (42, 42.99, 1.20), (41, 41.99, 1.10),
            (40, 40.99, 1.00), (0, 39.99, 0.00)
        ]
        
        # Letter grade mapping for display
        self.grade_to_letter = {
            4.00: 'A', 3.95: 'A', 3.90: 'A', 3.85: 'A', 3.80: 'A', 3.75: 'A',
            3.70: 'B+', 3.65: 'B+', 3.60: 'B+', 3.55: 'B+',
            3.50: 'B', 3.45: 'B', 3.40: 'B', 3.35: 'B', 3.30: 'B', 3.25: 'B',
            3.20: 'B', 3.15: 'B', 3.10: 'B', 3.05: 'B', 3.00: 'B',
            2.94: 'C', 2.88: 'C', 2.82: 'C', 2.76: 'C', 2.70: 'C',
            2.63: 'C', 2.56: 'C', 2.49: 'C', 2.42: 'C', 2.35: 'C',
            2.28: 'C', 2.21: 'C', 2.14: 'C', 2.07: 'C', 2.00: 'C',
            1.90: 'D', 1.80: 'D', 1.70: 'D', 1.60: 'D', 1.50: 'D',
            1.40: 'D', 1.30: 'D', 1.20: 'D', 1.10: 'D', 1.00: 'D',
            0.00: 'F'
        }

    def get_grade_from_percentage(self, percentage):
        """Get grade points from percentage using GCUF scale"""
        for low, high, points in self.grading_scale:
            if low <= percentage <= high:
                return points
        return 0.00

    def calculate_from_grade(self, name, credit_hours, grade_letter):
        """Calculate from direct grade selection"""
        # Map letter grades to approximate percentages (for display)
        grade_to_percentage = {
            'A': 85, 'B': 70, 'C': 55, 'D': 45, 'F': 30
        }
        
        # Get grade points based on letter
        if grade_letter == 'A':
            grade_value = 4.00
        elif grade_letter == 'B':
            grade_value = 3.00
        elif grade_letter == 'C':
            grade_value = 2.00
        elif grade_letter == 'D':
            grade_value = 1.00
        else:
            grade_value = 0.00
            
        quality_points = grade_value * credit_hours
        
        return Course(
            name=name,
            credit_hours=credit_hours,
            grade_value=grade_value,
            grade_letter=grade_letter,
            quality_points=quality_points,
            input_method='grade',
            percentage=grade_to_percentage.get(grade_letter, 0)
        )

    def calculate_from_marks(self, name, credit_hours, mids, final, sectional):
        """Calculate from marks based on credit hours"""
        
        # Set max marks based on credit hours
        if credit_hours == 3:
            max_mids, max_final, max_sectional = 20, 30, 10
            total_marks = 60
        elif credit_hours == 2:
            max_mids, max_final, max_sectional = 15, 20, 5
            total_marks = 40
        else:
            # Default for other credit hours
            max_mids, max_final, max_sectional = 0, 0, 0
            total_marks = 100
        
        # Calculate percentage
        obtained_marks = mids + final + sectional
        percentage = (obtained_marks / total_marks) * 100 if total_marks > 0 else 0
        
        # Get grade points from percentage
        grade_value = self.get_grade_from_percentage(percentage)
        
        # Get letter grade
        grade_letter = 'F'
        for points, letter in sorted([(k, v) for k, v in self.grade_to_letter.items()], reverse=True):
            if grade_value >= points:
                grade_letter = letter
                break
        
        quality_points = grade_value * credit_hours
        
        # Store marks details
        marks_details = {
            'mids': mids,
            'final': final,
            'sectional': sectional,
            'total_marks': total_marks,
            'obtained': obtained_marks,
            'max_mids': max_mids,
            'max_final': max_final,
            'max_sectional': max_sectional
        }
        
        return Course(
            name=name,
            credit_hours=credit_hours,
            grade_value=grade_value,
            grade_letter=grade_letter,
            quality_points=quality_points,
            input_method='marks',
            percentage=percentage,
            marks_details=marks_details
        )

# Custom dark theme CSS (keeping your existing CSS)
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
        
        /* Selectbox/Dropdown */
        .stSelectbox > div > div {
            background-color: #2D2D2D !important;
            color: #FFFFFF !important;
            border-color: #404040 !important;
            border-radius: 5px;
        }
        
        /* Radio buttons */
        .stRadio > div {
            background-color: #2D2D2D;
            padding: 10px;
            border-radius: 5px;
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
        }
        
        .stButton > button[kind="primary"] {
            background-color: #0066CC;
            border: 1px solid #0077FF;
        }
        
        /* Course container */
        .course-container {
            background-color: #2D2D2D;
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #404040;
            margin-bottom: 15px;
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
        
        /* Method indicator */
        .method-indicator {
            background-color: #0066CC;
            color: white;
            padding: 3px 10px;
            border-radius: 15px;
            font-size: 12px;
            margin-left: 10px;
        }
        
        /* Success message */
        .stSuccess {
            background-color: #1E4A2E;
            color: #FFFFFF;
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
    st.markdown("Calculate your GPA using **Grade-based** or **Marks-based** input")
    
    # Initialize session state
    if 'calculator' not in st.session_state:
        st.session_state.calculator = GPACalculator()
    
    if 'course_inputs' not in st.session_state:
        st.session_state.course_inputs = []
    
    if 'show_transcript' not in st.session_state:
        st.session_state.show_transcript = False
    
    # Global input method selector
    input_method = st.radio(
        "Select Input Method:",
        options=["🎯 Grade-Based (A, B, C, D, F)", "📊 Marks-Based (Mids, Final, Sectional)"],
        horizontal=True,
        key="global_input_method"
    )
    
    # Main content area
    col_main, col_actions = st.columns([3, 1])
    
    with col_main:
        st.subheader("📝 Course Details")
        
        # Display course count
        course_count = len(st.session_state.course_inputs)
        st.markdown(f"<span class='course-badge'>📚 Courses Added: {course_count}</span>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Display all course input boxes
        if course_count > 0:
            for i, course in enumerate(st.session_state.course_inputs, 1):
                with st.container():
                    st.markdown(f"<div class='course-container'>", unsafe_allow_html=True)
                    
                    # Show which method this course uses
                    method_text = "🎯 Grade" if course.get('method') == 'grade' else "📊 Marks"
                    st.markdown(f"**Course {i}** <span class='method-indicator'>{method_text}</span>", unsafe_allow_html=True)
                    
                    # Course Name
                    st.session_state.course_inputs[i-1]["name"] = st.text_input(
                        "Course Name", 
                        value=course["name"],
                        key=f"name_{i}",
                        placeholder="e.g., Mathematics"
                    )
                    
                    # Credit Hours
                    credit_options = [1, 2, 3, 4]
                    default_index = credit_options.index(course["credits"]) if course["credits"] in credit_options else 2
                    
                    st.session_state.course_inputs[i-1]["credits"] = st.selectbox(
                        "Credit Hours",
                        options=credit_options,
                        index=default_index,
                        key=f"credits_{i}"
                    )
                    
                    # Show different inputs based on course method
                    if course.get('method') == 'grade':
                        grade_options = ['A', 'B', 'C', 'D', 'F']
                        grade_index = grade_options.index(course["grade"]) if course["grade"] in grade_options else 0
                        
                        selected_grade = st.selectbox(
                            "Select Grade",
                            options=grade_options,
                            index=grade_index,
                            key=f"grade_{i}",
                            help="A=4.0, B=3.0, C=2.0, D=1.0, F=0.0"
                        )
                        st.session_state.course_inputs[i-1]["grade"] = selected_grade
                        
                    else:  # marks-based
                        credits = st.session_state.course_inputs[i-1]["credits"]
                        
                        # Show appropriate marks fields based on credit hours
                        if credits == 3:
                            col_m1, col_m2, col_m3 = st.columns(3)
                            with col_m1:
                                mids = st.number_input(
                                    "Mids (out of 20)",
                                    min_value=0.0,
                                    max_value=20.0,
                                    value=course.get("mids", 0.0),
                                    step=0.5,
                                    key=f"mids_{i}"
                                )
                                st.session_state.course_inputs[i-1]["mids"] = mids
                            
                            with col_m2:
                                final = st.number_input(
                                    "Final (out of 30)",
                                    min_value=0.0,
                                    max_value=30.0,
                                    value=course.get("final", 0.0),
                                    step=0.5,
                                    key=f"final_{i}"
                                )
                                st.session_state.course_inputs[i-1]["final"] = final
                            
                            with col_m3:
                                sectional = st.number_input(
                                    "Sectional (out of 10)",
                                    min_value=0.0,
                                    max_value=10.0,
                                    value=course.get("sectional", 0.0),
                                    step=0.5,
                                    key=f"sectional_{i}"
                                )
                                st.session_state.course_inputs[i-1]["sectional"] = sectional
                                
                        elif credits == 2:
                            col_m1, col_m2, col_m3 = st.columns(3)
                            with col_m1:
                                mids = st.number_input(
                                    "Mids (out of 15)",
                                    min_value=0.0,
                                    max_value=15.0,
                                    value=course.get("mids", 0.0),
                                    step=0.5,
                                    key=f"mids_{i}"
                                )
                                st.session_state.course_inputs[i-1]["mids"] = mids
                            
                            with col_m2:
                                final = st.number_input(
                                    "Final (out of 20)",
                                    min_value=0.0,
                                    max_value=20.0,
                                    value=course.get("final", 0.0),
                                    step=0.5,
                                    key=f"final_{i}"
                                )
                                st.session_state.course_inputs[i-1]["final"] = final
                            
                            with col_m3:
                                sectional = st.number_input(
                                    "Sectional (out of 5)",
                                    min_value=0.0,
                                    max_value=5.0,
                                    value=course.get("sectional", 0.0),
                                    step=0.5,
                                    key=f"sectional_{i}"
                                )
                                st.session_state.course_inputs[i-1]["sectional"] = sectional
                        else:
                            # Generic for other credit hours
                            total = st.number_input(
                                "Total Marks Obtained",
                                min_value=0.0,
                                max_value=100.0,
                                value=course.get("obtained", 0.0),
                                step=0.5,
                                key=f"obtained_{i}"
                            )
                            st.session_state.course_inputs[i-1]["obtained"] = total
                    
                    st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("👆 Click 'Add Course' to start adding courses")
    
    with col_actions:
        st.subheader("⚡ Actions")
        
        # Add Course button
        if st.button("➕ Add Course", use_container_width=True):
            if "🎯 Grade" in input_method:
                # Add grade-based course
                st.session_state.course_inputs.append({
                    "name": "", 
                    "credits": 3, 
                    "grade": "A",
                    "method": "grade"
                })
            else:
                # Add marks-based course
                st.session_state.course_inputs.append({
                    "name": "", 
                    "credits": 3, 
                    "mids": 0.0,
                    "final": 0.0,
                    "sectional": 0.0,
                    "method": "marks"
                })
            st.rerun()
        
        # Calculate button
        if st.button("🧮 Calculate GPA", use_container_width=True, type="primary"):
            if len(st.session_state.course_inputs) > 0:
                st.session_state.show_transcript = True
            else:
                st.warning("Please add at least one course first")
        
        # Reset button
        if st.button("🔄 Reset All", use_container_width=True):
            st.session_state.course_inputs = []
            st.session_state.show_transcript = False
            st.rerun()
        
        # Remove Last Course button
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
            if input_data["name"]:
                if input_data.get('method') == 'grade':
                    course = st.session_state.calculator.calculate_from_grade(
                        input_data["name"],
                        input_data["credits"],
                        input_data["grade"]
                    )
                else:  # marks-based
                    if input_data["credits"] in [2, 3]:
                        course = st.session_state.calculator.calculate_from_marks(
                            input_data["name"],
                            input_data["credits"],
                            input_data.get("mids", 0),
                            input_data.get("final", 0),
                            input_data.get("sectional", 0)
                        )
                    else:
                        # Generic calculation for other credit hours
                        course = st.session_state.calculator.calculate_from_marks(
                            input_data["name"],
                            input_data["credits"],
                            input_data.get("obtained", 0),
                            0,
                            0
                        )
                
                courses.append(course)
                total_quality_points += course.quality_points
                total_credits += course.credit_hours
        
        if courses:
            # Course table
            table_data = []
            for i, course in enumerate(courses, 1):
                if course.input_method == 'marks' and course.marks_details:
                    marks_info = f" ({course.marks_details['obtained']:.0f}/{course.marks_details['total_marks']})"
                else:
                    marks_info = ""
                
                table_data.append({
                    "Course": course.name,
                    "Grade": f"{course.grade_letter}",
                    "Grade Points": f"{course.grade_value:.2f}",
                    "Credits": f"{course.credit_hours:.0f}",
                    "Quality Points": f"{course.quality_points:.2f}",
                    "Percentage": f"{course.percentage:.1f}%"
                })
            
            df = pd.DataFrame(table_data)
            st.table(df)
            
            st.markdown("")
            
            # Summary
            gpa = total_quality_points / total_credits if total_credits > 0 else 0
            
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
