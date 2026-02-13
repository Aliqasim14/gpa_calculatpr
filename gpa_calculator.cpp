#include <iostream>
#include <vector>
#include <iomanip>
#include <string>
#include <map>

using namespace std;

class Course {
public:
    string name;
    double creditHours;
    double marksObtained;
    double totalMarks;
    double gradePoints;
    double qualityPoints;
    
    Course(string n, double credit, double obtained, double total) 
        : name(n), creditHours(credit), marksObtained(obtained), totalMarks(total) {
        calculateGradePoints();
        qualityPoints = gradePoints * creditHours;
    }
    
private:
    void calculateGradePoints() {
        double percentage = (marksObtained / totalMarks) * 100;
        
        // GCUF Grading System based on percentage
        if (percentage >= 85) gradePoints = 4.00;
        else if (percentage >= 84) gradePoints = 3.95;
        else if (percentage >= 83) gradePoints = 3.90;
        else if (percentage >= 82) gradePoints = 3.85;
        else if (percentage >= 81) gradePoints = 3.80;
        else if (percentage >= 80) gradePoints = 3.75;
        else if (percentage >= 79) gradePoints = 3.70;
        else if (percentage >= 78) gradePoints = 3.65;
        else if (percentage >= 77) gradePoints = 3.60;
        else if (percentage >= 76) gradePoints = 3.55;
        else if (percentage >= 75) gradePoints = 3.50;
        else if (percentage >= 74) gradePoints = 3.45;
        else if (percentage >= 73) gradePoints = 3.40;
        else if (percentage >= 72) gradePoints = 3.35;
        else if (percentage >= 71) gradePoints = 3.30;
        else if (percentage >= 70) gradePoints = 3.25;
        else if (percentage >= 69) gradePoints = 3.20;
        else if (percentage >= 68) gradePoints = 3.15;
        else if (percentage >= 67) gradePoints = 3.10;
        else if (percentage >= 66) gradePoints = 3.05;
        else if (percentage >= 65) gradePoints = 3.00;
        else if (percentage >= 64) gradePoints = 2.94;
        else if (percentage >= 63) gradePoints = 2.88;
        else if (percentage >= 62) gradePoints = 2.82;
        else if (percentage >= 61) gradePoints = 2.76;
        else if (percentage >= 60) gradePoints = 2.70;
        else if (percentage >= 59) gradePoints = 2.63;
        else if (percentage >= 58) gradePoints = 2.56;
        else if (percentage >= 57) gradePoints = 2.49;
        else if (percentage >= 56) gradePoints = 2.42;
        else if (percentage >= 55) gradePoints = 2.35;
        else if (percentage >= 54) gradePoints = 2.28;
        else if (percentage >= 53) gradePoints = 2.21;
        else if (percentage >= 52) gradePoints = 2.14;
        else if (percentage >= 51) gradePoints = 2.07;
        else if (percentage >= 50) gradePoints = 2.00;
        else if (percentage >= 49) gradePoints = 1.90;
        else if (percentage >= 48) gradePoints = 1.80;
        else if (percentage >= 47) gradePoints = 1.70;
        else if (percentage >= 46) gradePoints = 1.60;
        else if (percentage >= 45) gradePoints = 1.50;
        else if (percentage >= 44) gradePoints = 1.40;
        else if (percentage >= 43) gradePoints = 1.30;
        else if (percentage >= 42) gradePoints = 1.20;
        else if (percentage >= 41) gradePoints = 1.10;
        else if (percentage >= 40) gradePoints = 1.00;
        else gradePoints = 0.00;
    }
};

class GPACalculator {
private:
    vector<Course> courses;
    string studentName;
    string email;
    string rollNumber;
    
public:
    void addCourse() {
        string name;
        double creditHours, mids, final_, sectional;
        
        cout << "Course Name: ";
        cin.ignore();
        getline(cin, name);
        
        cout << "Credit Hours: ";
        cin >> creditHours;
        
        // Calculate total marks based on credit hours
        double totalMarks;
        if (creditHours == 3) {
            totalMarks = 60; // 3 credit hour course total marks
            cout << "Enter Mids marks (out of 20): ";
            cin >> mids;
            cout << "Enter Final marks (out of 30): ";
            cin >> final_;
            cout << "Enter Sectional marks (out of 10): ";
            cin >> sectional;
        } else if (creditHours == 2) {
            totalMarks = 40; // 2 credit hour course total marks
            cout << "Enter Mids marks (out of 15): ";
            cin >> mids;
            cout << "Enter Final marks (out of 20): ";
            cin >> final_;
            cout << "Enter Sectional marks (out of 5): ";
            cin >> sectional;
        } else {
            cout << "Enter total marks obtained: ";
            cin >> mids;
            totalMarks = mids;
            final_ = 0;
            sectional = 0;
        }
        
        double marksObtained = mids + final_ + sectional;
        courses.push_back(Course(name, creditHours, marksObtained, totalMarks));
    }
    
    void calculateGPA() {
        double totalQualityPoints = 0;
        double totalCredits = 0;
        
        cout << "\n\n" << string(50, '=') << endl;
        cout << "                    GPA TRANSCRIPT" << endl;
        cout << string(50, '=') << endl;
        
        if (!studentName.empty())
            cout << "Name: " << studentName << endl;
        if (!email.empty())
            cout << "Email: " << email << endl;
        if (!rollNumber.empty())
            cout << "Roll Number: " << rollNumber << endl;
        
        cout << "\n" << left << setw(30) << "Course" 
             << setw(10) << "Grade" 
             << setw(10) << "Credits" 
             << setw(15) << "Quality Points" << endl;
        cout << string(65, '-') << endl;
        
        for (const auto& course : courses) {
            char letterGrade = getLetterGrade(course.gradePoints);
            cout << left << setw(30) << course.name 
                 << setw(10) << letterGrade
                 << setw(10) << fixed << setprecision(2) << course.creditHours
                 << setw(15) << course.qualityPoints << endl;
            
            totalQualityPoints += course.qualityPoints;
            totalCredits += course.creditHours;
        }
        
        cout << string(65, '-') << endl;
        cout << left << setw(40) << "Total Quality Points: " 
             << fixed << setprecision(2) << totalQualityPoints << endl;
        cout << left << setw(40) << "Total Credits: " 
             << totalCredits << endl;
        
        double gpa = (totalCredits > 0) ? totalQualityPoints / totalCredits : 0;
        cout << left << setw(40) << "GPA: " 
             << fixed << setprecision(2) << gpa << endl;
        cout << string(50, '=') << endl;
    }
    
    void setStudentInfo() {
        cout << "Enter Student Name: ";
        cin.ignore();
        getline(cin, studentName);
        cout << "Enter Email: ";
        getline(cin, email);
        cout << "Enter Roll Number: ";
        getline(cin, rollNumber);
    }
    
private:
    char getLetterGrade(double gradePoints) {
        if (gradePoints >= 3.75) return 'A';
        else if (gradePoints >= 3.00) return 'B';
        else if (gradePoints >= 2.00) return 'C';
        else if (gradePoints >= 1.00) return 'D';
        else return 'F';
    }
};

int main() {
    GPACalculator calculator;
    int numCourses;
    
    cout << "=== GCUF GPA CALCULATOR ===\n" << endl;
    
    calculator.setStudentInfo();
    
    cout << "\nEnter number of courses: ";
    cin >> numCourses;
    
    for (int i = 0; i < numCourses; i++) {
        cout << "\n--- Course " << (i + 1) << " ---" << endl;
        calculator.addCourse();
    }
    
    calculator.calculateGPA();
    
    return 0;
}