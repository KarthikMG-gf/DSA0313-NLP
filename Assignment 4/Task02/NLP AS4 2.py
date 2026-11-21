# Finite domain model M
students = {"Asha", "Bala"}
courses = {"CS101", "CS102", "NLP"}
instructors = {"rao", "sharma"}

enrolled = {("Asha", "CS101"), ("Bala", "CS102"), ("Asha", "NLP"), ("Bala", "NLP")}
teaches = {("rao", "CS101"), ("sharma", "CS102")}
passed = {("Asha", "CS101"), ("Asha", "NLP"), ("Bala", "NLP")}

# Formula (i): ∀x (Student(x) -> ∃y (Course(y) ∧ Enrolled(x, y)))
f1_every_student_some_course = all(
    any((s, c) in enrolled for c in courses)
    for s in students
)

# Reversed quantifier order: ∃y (Course(y) ∧ ∀x (Student(x) -> Enrolled(x, y)))
# Restricted to {CS101, CS102} to demonstrate counterexample
sub_courses = {"CS101", "CS102"}
f1_reversed = any(
    all((s, c) in enrolled for s in students)
    for c in sub_courses
)

# Formula (ii): ∃x (Student(x) ∧ ∀y ((Course(y) ∧ Teaches(rao, y)) -> Passed(x, y)))
f2_some_passed_all_rao = any(
    all((s, c) in passed for c in courses if ("rao", c) in teaches)
    for s in students
)

# Formula (iii): ¬∃z (Instructor(z) ∧ ∀y (Course(y) -> Teaches(z, y)))
f3_no_inst_all_courses = not any(
    all((inst, c) in teaches for c in courses)
    for inst in instructors
)

# Consistency check (Task 2.4)
every_passed_nlp = all((s, "NLP") in passed for s in students)
some_failed_nlp = any((s, "NLP") not in passed for s in students)

print("Formula (i) ∀x∃y:", f1_every_student_some_course)
print("Reversed ∃y∀x on {CS101, CS102}:", f1_reversed)
print("Formula (ii):", f2_some_passed_all_rao)
print("Formula (iii):", f3_no_inst_all_courses)
print("Consistent pair?:", not (every_passed_nlp and some_failed_nlp))
