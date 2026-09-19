# Jeremy Thomasson
# CIS261
# WK10 VIBE Coding

"""Student Grade Calculator."""

from dataclasses import dataclass


FILE_NAME = "student_grades.txt"


@dataclass
class Student:
	"""Store one student's scores and calculate the final results."""

	name: str
	student_id: str
	test1: float
	test2: float
	test3: float

	@property
	def average(self):
		return (self.test1 + self.test2 + self.test3) / 3

	@property
	def grade(self):
		if self.average >= 90:
			return "A"
		if self.average >= 80:
			return "B"
		if self.average >= 70:
			return "C"
		if self.average >= 60:
			return "D"
		return "F"

	def to_file_line(self):
		return (
			f"{self.name}|{self.student_id}|{self.test1:.2f}|"
			f"{self.test2:.2f}|{self.test3:.2f}|{self.average:.2f}|{self.grade}\n"
		)


def is_escape(value):
	return value == "\x1b"


def get_text(prompt):
	while True:
		value = input(prompt)
		if is_escape(value):
			return None
		if value.strip():
			return value.strip()
		print("Please enter a value.")


def get_score(test_name):
	while True:
		value = input(f"Enter {test_name} score (0-100): ")
		if is_escape(value):
			return None
		try:
			score = float(value)
			if 0 <= score <= 100:
				return score
			print("Score must be between 0 and 100.")
		except ValueError:
			print("Please enter a valid number.")


def add_student(students):
	print("\nAdd Student (press ESC to cancel)")
	name = get_text("Enter student name: ")
	if name is None:
		print("Add student canceled.")
		return
	student_id = get_text("Enter student ID: ")
	if student_id is None:
		print("Add student canceled.")
		return

	scores = []
	for test_name in ("Test 1", "Test 2", "Test 3"):
		score = get_score(test_name)
		if score is None:
			print("Add student canceled.")
			return
		scores.append(score)

	student = Student(name, student_id, scores[0], scores[1], scores[2])
	students.append(student)
	print(f"Added {name}. Average: {student.average:.2f}, Grade: {student.grade}")


def display_students(students):
	if not students:
		print("\nNo student records found.")
		return

	print("\nStudent Records")
	print("-" * 92)
	print(f"{'Name':<22} {'ID':<14} {'Test 1':>8} {'Test 2':>8} "
		  f"{'Test 3':>8} {'Average':>9} {'Grade':>7}")
	print("-" * 92)
	for student in students:
		print(f"{student.name:<22.22} {student.student_id:<14.14} "
			  f"{student.test1:>8.2f} {student.test2:>8.2f} "
			  f"{student.test3:>8.2f} {student.average:>9.2f} "
			  f"{student.grade:>7}")
	print("-" * 92)


def display_statistics(students):
	if not students:
		print("\nNo student records found.")
		return
	highest = max(students, key=lambda student: student.average)
	lowest = min(students, key=lambda student: student.average)
	class_average = sum(student.average for student in students) / len(students)
	print("\nClass Statistics")
	print(f"Highest average: {highest.average:.2f} ({highest.name})")
	print(f"Lowest average:  {lowest.average:.2f} ({lowest.name})")
	print(f"Class average:   {class_average:.2f}")


def search_student(students):
	name = get_text("\nEnter student name to search: ")
	if name is None:
		print("Search canceled.")
		return
	matches = [student for student in students if name.lower() in student.name.lower()]
	if matches:
		display_students(matches)
	else:
		print(f"No student found matching '{name}'.")


def save_students(students):
	try:
		with open(FILE_NAME, "w", encoding="utf-8") as file:
			for student in students:
				file.write(student.to_file_line())
		print(f"Saved {len(students)} record(s) to {FILE_NAME}.")
		return True
	except OSError as error:
		print(f"Error saving student records: {error}")
		return False


def load_students():
	students = []
	try:
		with open(FILE_NAME, "r", encoding="utf-8") as file:
			for line_number, line in enumerate(file, start=1):
				parts = line.rstrip("\n").split("|")
				if len(parts) != 7:
					print(f"Skipping invalid record on line {line_number}.")
					continue
				try:
					students.append(Student(
						parts[0], parts[1], float(parts[2]),
						float(parts[3]), float(parts[4])
					))
				except ValueError:
					print(f"Skipping invalid record on line {line_number}.")
		if students:
			print(f"Loaded {len(students)} record(s) from {FILE_NAME}.")
	except FileNotFoundError:
		print(f"No existing {FILE_NAME} found. Starting with an empty list.")
	except OSError as error:
		print(f"Error loading student records: {error}")
	return students


def display_menu():
	print("\nStudent Grade Calculator")
	print("1. Add student")
	print("2. Display all students")
	print("3. Display class statistics")
	print("4. Search for a student")
	print("5. Save records")
	print("6. Exit")
	print("Press ESC at the menu to save and exit.")


def main():
	students = load_students()
	while True:
		display_menu()
		choice = input("Choose an option: ")
		if is_escape(choice) or choice == "6":
			save_students(students)
			print("Goodbye!")
			break
		if choice == "1":
			add_student(students)
		elif choice == "2":
			display_students(students)
		elif choice == "3":
			display_statistics(students)
		elif choice == "4":
			search_student(students)
		elif choice == "5":
			save_students(students)
		else:
			print("Invalid option. Please choose 1-6 or press ESC.")


if __name__ == "__main__":
	main()