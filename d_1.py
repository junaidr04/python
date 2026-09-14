student_marks=[90,40,75,82,55,95,33,68]
print("Shob student er results:")
for mark in student_marks:
    if mark>=80:
        result="A+"
    elif mark>=60:
        result="Pass"
    else:
        result="Fail"
    print(f"Mark: {mark}, Result: {result}")

# Average calculation
total=sum(student_marks)
avg=total/len(student_marks)
print(f"\nClass average mark: {avg}")