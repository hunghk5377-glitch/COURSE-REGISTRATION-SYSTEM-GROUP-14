# =========================
# Course Registration System
# Roles: Admin, Lecturer, Student
# =========================

# ---------- USER BASE ----------
class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role


# ---------- STUDENT ----------
class Student(User):
    def __init__(self, username, password, student_id, name):
        super().__init__(username, password, "student")
        self.student_id = student_id
        self.name = name
        self.registered_courses = []

    def register_course(self, course):
        if course.is_full():
            print("❌ Course is full.")
            return
        if self.student_id in course.enrolled_students:
            print("❌ Already registered.")
            return
        self.registered_courses.append(course.course_id)
        course.enrolled_students.append(self.student_id)
        print("✅ Registered successfully.")

    def drop_course(self, course):
        if self.student_id not in course.enrolled_students:
            print("❌ You have not registered.")
            return
        self.registered_courses.remove(course.course_id)
        course.enrolled_students.remove(self.student_id)
        print("✅ Dropped successfully.")


# ---------- LECTURER ----------
class Lecturer(User):
    def __init__(self, username, password, lecturer_id, name):
        super().__init__(username, password, "lecturer")
        self.lecturer_id = lecturer_id
        self.name = name
        self.courses = []


# ---------- ADMIN ----------
class Admin(User):
    def __init__(self, username, password):
        super().__init__(username, password, "admin")


# ---------- COURSE ----------
class Course:
    def __init__(self, course_id, course_name, max_students, lecturer):
        self.course_id = course_id
        self.course_name = course_name
        self.max_students = max_students
        self.lecturer = lecturer
        self.enrolled_students = []

    def is_full(self):
        return len(self.enrolled_students) >= self.max_students


# ---------- SYSTEM ----------
class CourseRegistrationSystem:
    def __init__(self):
        self.users = {}
        self.courses = {}

    def add_user(self, user):
        self.users[user.username] = user

    def add_course(self, course):
        self.courses[course.course_id] = course

    def login(self, username, password):
        user = self.users.get(username)
        if user and user.password == password:
            print(f"✅ Login successful ({user.role})")
            return user
        print("❌ Invalid login.")
        return None

    def show_courses(self):
        print("\n--- Course List ---")
        for c in self.courses.values():
            print(f"{c.course_id} - {c.course_name} | Lecturer: {c.lecturer.name} | {len(c.enrolled_students)}/{c.max_students}")


# =========================
# MAIN PROGRAM
# =========================
def main():
    system = CourseRegistrationSystem()

    # --- Sample Data ---
    admin = Admin("admin", "admin")
    lec1 = Lecturer("lec01", "123", "L01", "Dr. Smith")
    stu1 = Student("sv01", "123", "S01", "Nguyen Van A")
    stu2 = Student("sv02", "123", "S02", "Tran Thi B")

    system.add_user(admin)
    system.add_user(lec1)
    system.add_user(stu1)
    system.add_user(stu2)

    c1 = Course("C001", "Data Structures", 2, lec1)
    lec1.courses.append(c1)
    system.add_course(c1)

    current_user = None

    while True:
        if not current_user:
            print("\n===== LOGIN =====")
            u = input("Username: ")
            p = input("Password: ")
            current_user = system.login(u, p)

        else:
            # ---------- ADMIN MENU ----------
            if current_user.role == "admin":
                print("\n--- ADMIN MENU ---")
                print("1. View courses")
                print("2. Logout")

                ch = input("Choose: ")
                if ch == "1":
                    system.show_courses()
                elif ch == "2":
                    current_user = None

            # ---------- LECTURER MENU ----------
            elif current_user.role == "lecturer":
                print("\n--- LECTURER MENU ---")
                print("1. View my courses")
                print("2. Logout")

                ch = input("Choose: ")
                if ch == "1":
                    for c in current_user.courses:
                        print(f"{c.course_id} - {c.course_name} | Students: {len(c.enrolled_students)}")
                elif ch == "2":
                    current_user = None

            # ---------- STUDENT MENU ----------
            elif current_user.role == "student":
                print("\n--- STUDENT MENU ---")
                print("1. View courses")
                print("2. Register course")
                print("3. Drop course")
                print("4. Logout")

                ch = input("Choose: ")
                if ch == "1":
                    system.show_courses()
                elif ch == "2":
                    cid = input("Course ID: ")
                    course = system.courses.get(cid)
                    if course:
                        current_user.register_course(course)
                elif ch == "3":
                    cid = input("Course ID: ")
                    course = system.courses.get(cid)
                    if course:
                        current_user.drop_course(course)
                elif ch == "4":
                    current_user = None


if __name__ == "__main__":
    main()
