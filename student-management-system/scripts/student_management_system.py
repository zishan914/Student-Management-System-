import csv
import os
from typing import List, Dict, Optional

# File to store student data
STUDENTS_FILE = "students.csv"

def initialize_csv_file():
    """
    Initialize the CSV file with headers if it doesn't exist.
    This ensures the file is ready for reading and writing student data.
    """
    if not os.path.exists(STUDENTS_FILE):
        with open(STUDENTS_FILE, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Write header row
            writer.writerow(['Roll_No', 'Name', 'Age', 'Gender', 'Department', 'Semester', 'Marks', 'GPA', 'Grade'])
        print(f"Created new student database file: {STUDENTS_FILE}")

def load_students() -> List[Dict]:
    """
    Load all student records from the CSV file.
    Returns a list of dictionaries, each representing a student.
    """
    students = []
    try:
        with open(STUDENTS_FILE, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Convert numeric fields to appropriate types
                row['Age'] = int(row['Age']) if row['Age'] else 0
                row['Semester'] = int(row['Semester']) if row['Semester'] else 0
                row['Marks'] = float(row['Marks']) if row['Marks'] else 0.0
                row['GPA'] = float(row['GPA']) if row['GPA'] else 0.0
                students.append(row)
    except FileNotFoundError:
        print("No student records found. Starting with empty database.")
    except Exception as e:
        print(f"Error loading student data: {e}")
    
    return students

def save_students(students: List[Dict]):
    """
    Save all student records to the CSV file.
    This ensures data persistence between program runs.
    """
    try:
        with open(STUDENTS_FILE, 'w', newline='', encoding='utf-8') as file:
            if students:
                fieldnames = ['Roll_No', 'Name', 'Age', 'Gender', 'Department', 'Semester', 'Marks', 'GPA', 'Grade']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(students)
        print("Student data saved successfully!")
    except Exception as e:
        print(f"Error saving student data: {e}")

def calculate_gpa_and_grade(marks: float) -> tuple:
    """
    Calculate GPA and letter grade based on marks.
    Returns a tuple of (GPA, Grade).
    
    Grading scale:
    90-100: A+ (4.0)
    80-89:  A  (3.7)
    70-79:  B+ (3.3)
    60-69:  B  (3.0)
    50-59:  C+ (2.7)
    40-49:  C  (2.0)
    Below 40: F (0.0)
    """
    if marks >= 90:
        return 4.0, "A+"
    elif marks >= 80:
        return 3.7, "A"
    elif marks >= 70:
        return 3.3, "B+"
    elif marks >= 60:
        return 3.0, "B"
    elif marks >= 50:
        return 2.7, "C+"
    elif marks >= 40:
        return 2.0, "C"
    else:
        return 0.0, "F"

def is_roll_no_unique(roll_no: str, students: List[Dict], exclude_index: int = -1) -> bool:
    """
    Check if a roll number is unique in the student database.
    exclude_index is used when updating a student to exclude their current record.
    """
    for i, student in enumerate(students):
        if i != exclude_index and student['Roll_No'].lower() == roll_no.lower():
            return False
    return True

def get_valid_input(prompt: str, input_type: type, min_val=None, max_val=None):
    """
    Get valid input from user with type checking and range validation.
    """
    while True:
        try:
            value = input_type(input(prompt))
            if min_val is not None and value < min_val:
                print(f"Value must be at least {min_val}")
                continue
            if max_val is not None and value > max_val:
                print(f"Value must be at most {max_val}")
                continue
            return value
        except ValueError:
            print(f"Please enter a valid {input_type.__name__}")

def add_student(students: List[Dict]):
    """
    Add a new student to the database.
    Validates input and ensures roll number uniqueness.
    """
    print("\n" + "="*50)
    print("           ADD NEW STUDENT")
    print("="*50)
    
    # Get and validate roll number
    while True:
        roll_no = input("Enter Roll Number: ").strip()
        if not roll_no:
            print("Roll number cannot be empty!")
            continue
        if is_roll_no_unique(roll_no, students):
            break
        else:
            print("Roll number already exists! Please enter a unique roll number.")
    
    # Get other student details
    name = input("Enter Student Name: ").strip()
    while not name:
        print("Name cannot be empty!")
        name = input("Enter Student Name: ").strip()
    
    age = get_valid_input("Enter Age: ", int, 15, 100)
    
    gender = input("Enter Gender (M/F/Other): ").strip().upper()
    while gender not in ['M', 'F', 'OTHER']:
        print("Please enter M, F, or Other")
        gender = input("Enter Gender (M/F/Other): ").strip().upper()
    
    department = input("Enter Department: ").strip()
    while not department:
        print("Department cannot be empty!")
        department = input("Enter Department: ").strip()
    
    semester = get_valid_input("Enter Semester (1-8): ", int, 1, 8)
    marks = get_valid_input("Enter Marks (0-100): ", float, 0, 100)
    
    # Calculate GPA and Grade
    gpa, grade = calculate_gpa_and_grade(marks)
    
    # Create student record
    student = {
        'Roll_No': roll_no,
        'Name': name,
        'Age': age,
        'Gender': gender,
        'Department': department,
        'Semester': semester,
        'Marks': marks,
        'GPA': gpa,
        'Grade': grade
    }
    
    students.append(student)
    save_students(students)
    print(f"\nStudent {name} (Roll No: {roll_no}) added successfully!")
    print(f"GPA: {gpa}, Grade: {grade}")

def view_all_students(students: List[Dict]):
    """
    Display all students in a formatted table.
    """
    print("\n" + "="*120)
    print("                                    ALL STUDENTS")
    print("="*120)
    
    if not students:
        print("No students found in the database.")
        return
    
    # Print table header
    print(f"{'Roll No':<10} {'Name':<20} {'Age':<5} {'Gender':<8} {'Department':<15} {'Sem':<5} {'Marks':<7} {'GPA':<5} {'Grade':<5}")
    print("-" * 120)
    
    # Print student data
    for student in students:
        print(f"{student['Roll_No']:<10} {student['Name']:<20} {student['Age']:<5} "
              f"{student['Gender']:<8} {student['Department']:<15} {student['Semester']:<5} "
              f"{student['Marks']:<7.1f} {student['GPA']:<5.1f} {student['Grade']:<5}")
    
    print(f"\nTotal Students: {len(students)}")

def search_student(students: List[Dict]):
    """
    Search for a student by roll number or name.
    """
    print("\n" + "="*50)
    print("           SEARCH STUDENT")
    print("="*50)
    
    if not students:
        print("No students found in the database.")
        return
    
    print("Search by:")
    print("1. Roll Number")
    print("2. Name")
    
    choice = input("Enter your choice (1-2): ").strip()
    
    found_students = []
    
    if choice == '1':
        roll_no = input("Enter Roll Number to search: ").strip()
        found_students = [s for s in students if s['Roll_No'].lower() == roll_no.lower()]
    elif choice == '2':
        name = input("Enter Name to search: ").strip()
        found_students = [s for s in students if name.lower() in s['Name'].lower()]
    else:
        print("Invalid choice!")
        return
    
    if found_students:
        print(f"\nFound {len(found_students)} student(s):")
        print("-" * 80)
        for student in found_students:
            print(f"Roll No: {student['Roll_No']}")
            print(f"Name: {student['Name']}")
            print(f"Age: {student['Age']}")
            print(f"Gender: {student['Gender']}")
            print(f"Department: {student['Department']}")
            print(f"Semester: {student['Semester']}")
            print(f"Marks: {student['Marks']}")
            print(f"GPA: {student['GPA']}")
            print(f"Grade: {student['Grade']}")
            print("-" * 80)
    else:
        print("No student found with the given criteria.")

def update_student(students: List[Dict]):
    """
    Update an existing student's details.
    """
    print("\n" + "="*50)
    print("           UPDATE STUDENT")
    print("="*50)
    
    if not students:
        print("No students found in the database.")
        return
    
    roll_no = input("Enter Roll Number of student to update: ").strip()
    
    # Find student
    student_index = -1
    for i, student in enumerate(students):
        if student['Roll_No'].lower() == roll_no.lower():
            student_index = i
            break
    
    if student_index == -1:
        print("Student not found!")
        return
    
    student = students[student_index]
    print(f"\nCurrent details for {student['Name']}:")
    print(f"1. Name: {student['Name']}")
    print(f"2. Age: {student['Age']}")
    print(f"3. Gender: {student['Gender']}")
    print(f"4. Department: {student['Department']}")
    print(f"5. Semester: {student['Semester']}")
    print(f"6. Marks: {student['Marks']}")
    
    print("\nWhat would you like to update?")
    print("1. Name")
    print("2. Age")
    print("3. Gender")
    print("4. Department")
    print("5. Semester")
    print("6. Marks")
    print("7. Update All")
    
    choice = input("Enter your choice (1-7): ").strip()
    
    if choice == '1':
        new_name = input(f"Enter new name (current: {student['Name']}): ").strip()
        if new_name:
            student['Name'] = new_name
    elif choice == '2':
        student['Age'] = get_valid_input(f"Enter new age (current: {student['Age']}): ", int, 15, 100)
    elif choice == '3':
        new_gender = input(f"Enter new gender (current: {student['Gender']}) [M/F/Other]: ").strip().upper()
        if new_gender in ['M', 'F', 'OTHER']:
            student['Gender'] = new_gender
    elif choice == '4':
        new_dept = input(f"Enter new department (current: {student['Department']}): ").strip()
        if new_dept:
            student['Department'] = new_dept
    elif choice == '5':
        student['Semester'] = get_valid_input(f"Enter new semester (current: {student['Semester']}): ", int, 1, 8)
    elif choice == '6':
        student['Marks'] = get_valid_input(f"Enter new marks (current: {student['Marks']}): ", float, 0, 100)
        # Recalculate GPA and Grade
        student['GPA'], student['Grade'] = calculate_gpa_and_grade(student['Marks'])
    elif choice == '7':
        # Update all fields
        student['Name'] = input(f"Enter name (current: {student['Name']}): ").strip() or student['Name']
        student['Age'] = get_valid_input(f"Enter age (current: {student['Age']}): ", int, 15, 100)
        
        new_gender = input(f"Enter gender (current: {student['Gender']}) [M/F/Other]: ").strip().upper()
        if new_gender in ['M', 'F', 'OTHER']:
            student['Gender'] = new_gender
        
        new_dept = input(f"Enter department (current: {student['Department']}): ").strip()
        if new_dept:
            student['Department'] = new_dept
        
        student['Semester'] = get_valid_input(f"Enter semester (current: {student['Semester']}): ", int, 1, 8)
        student['Marks'] = get_valid_input(f"Enter marks (current: {student['Marks']}): ", float, 0, 100)
        
        # Recalculate GPA and Grade
        student['GPA'], student['Grade'] = calculate_gpa_and_grade(student['Marks'])
    else:
        print("Invalid choice!")
        return
    
    save_students(students)
    print("Student details updated successfully!")

def delete_student(students: List[Dict]):
    """
    Delete a student record from the database.
    """
    print("\n" + "="*50)
    print("           DELETE STUDENT")
    print("="*50)
    
    if not students:
        print("No students found in the database.")
        return
    
    roll_no = input("Enter Roll Number of student to delete: ").strip()
    
    # Find student
    student_index = -1
    for i, student in enumerate(students):
        if student['Roll_No'].lower() == roll_no.lower():
            student_index = i
            break
    
    if student_index == -1:
        print("Student not found!")
        return
    
    student = students[student_index]
    print(f"\nStudent found:")
    print(f"Roll No: {student['Roll_No']}")
    print(f"Name: {student['Name']}")
    print(f"Department: {student['Department']}")
    
    confirm = input("\nAre you sure you want to delete this student? (y/n): ").strip().lower()
    
    if confirm == 'y' or confirm == 'yes':
        deleted_student = students.pop(student_index)
        save_students(students)
        print(f"Student {deleted_student['Name']} (Roll No: {deleted_student['Roll_No']}) deleted successfully!")
    else:
        print("Deletion cancelled.")

def display_menu():
    """
    Display the main menu options.
    """
    print("\n" + "="*60)
    print("              STUDENT MANAGEMENT SYSTEM")
    print("="*60)
    print("1. Add New Student")
    print("2. View All Students")
    print("3. Search Student")
    print("4. Update Student Details")
    print("5. Delete Student")
    print("6. Exit")
    print("="*60)

def main():
    """
    Main function that runs the student management system.
    """
    print("Welcome to Student Management System!")
    print("Initializing system...")
    
    # Initialize CSV file
    initialize_csv_file()
    
    # Load existing students
    students = load_students()
    print(f"Loaded {len(students)} student records.")
    
    while True:
        display_menu()
        
        try:
            choice = input("Enter your choice (1-6): ").strip()
            
            if choice == '1':
                add_student(students)
            elif choice == '2':
                view_all_students(students)
            elif choice == '3':
                search_student(students)
            elif choice == '4':
                update_student(students)
            elif choice == '5':
                delete_student(students)
            elif choice == '6':
                print("\nThank you for using Student Management System!")
                print("All data has been saved. Goodbye!")
                break
            else:
                print("Invalid choice! Please enter a number between 1-6.")
        
        except KeyboardInterrupt:
            print("\n\nProgram interrupted by user.")
            print("All data has been saved. Goodbye!")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Please try again.")
        
        # Pause before showing menu again
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
