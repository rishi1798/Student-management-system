
student_id_to_obj = {}


class Student:

    def __init__(self):
        self.type = None  # BIT or DIT
        self.id = None
        self.name = None
        self.assessment_marks = []
        self.final_marks = None
        self.interim_grade = None
        self.final_grade = None
        self.AF_count = 0


    def add_student_id(self, value):
        if self.validate_student_id(value):
            self.id = value
            return True

        return False

    def validate_student_id(self, value):
        if value.startswith('A') and len(value[1:]) == 8:
            try:
                int(value[1:])
            except ValueError:
                return False

            return True

        return False

    def add_student_name(self, value):
        for i in value:
            if i.isalpha() or i == " ":
                continue
            else:
                print("Entered Student Name in Correct Format")
                return False
        self.name = value
        return True

    def add_assessment_marks(self, value):
        if self.validate_assesment_marks(value):
            self.assessment_marks = list(map(float,value.split(",")))
            return True
        

        return False

    def validate_assesment_marks(self, value):
        try:
            marks = list(map(float,value.split(",")))
        except ValueError:
            print("Provide Only Numeric Value")
            return False
        if len(marks) == 3:
            for val in marks:
                try:
                    if val > 100 or val < 0:
                        print("Marks Should be between 0 to 100")
                        return False
                except ValueError:
                    return False
            return True

        return False

    def calculate_final_marks(self):
        v = 0
        for index, value in enumerate([20, 40, 40]):
            mark = self.assessment_marks[index]
            v = v + (mark*value)/100

        self.final_marks = v

    def calculate_interim_grade(self):
        if self.type == "BIT":
            self.cal_interim_grade_for_bit()
        else:
            self.cal_interim_grade_for_dit()

    def cal_interim_grade_for_bit(self):
        self.calculate_final_marks()
        if self.final_marks >= 85:
            self.interim_grade = "HD"
        elif self.final_marks >= 75:
            self.interim_grade = "D"
        elif self.final_marks >= 65:
            self.interim_grade = "C"
        elif self.final_marks >= 50:
            self.interim_grade = "P"

        elif self.final_marks >= 45:
            one_assessment_zero = False
            failed_assessments_index = []

            for index, marks in enumerate(self.assessment_marks):
                if marks == 0:
                    one_assessment_zero = True
                if marks < 50:
                    failed_assessments_index.append(index)

            if one_assessment_zero and len(failed_assessments_index)>=1:
                self.interim_grade = "F"
            elif 2 in failed_assessments_index:
                self.interim_grade = "SE"
            else:
                self.interim_grade = "SA"

        else:
            zero_marks_assessments = 0
            for marks in self.assessment_marks:
                if marks == 0:
                    zero_marks_assessments += 1

            if zero_marks_assessments >=2:
                self.interim_grade = "AF"
            else:
                self.interim_grade = "F"

        if self.interim_grade == "SE" or self.interim_grade == "SA":
            supplementry_percent = None
            while True:
                try:
                    supplementry_percent = list(map(float,input("What is this student’s supplementary exam mark:").split(",")))
                except ValueError:
                    print("Provide Marks in Correct Format")

                if len(supplementry_percent) == 1:
                    break
                else:
                    print("Give only one final marks")

            if supplementry_percent[0] > 50:
                self.interim_grade = "SP"
            else:
                self.interim_grade = "F"

        if self.interim_grade == "AF":
            self.AF_count = 1
            self.interim_grade = "F"
        self.final_grade_letter()

    def cal_interim_grade_for_dit(self):
        self.calculate_final_marks()
        if self.final_marks <= 49:
            self.interim_grade = "NYC"
        else:
            self.interim_grade = "CP"

        if self.interim_grade == "NYC":
            while True:
                supplement_marks = input("What is this student’s resubmission marks (separated by comma): ")
                if self.add_assessment_marks(supplement_marks):
                    break
            self.calculate_final_marks()
            if self.final_marks > 50:
                self.interim_grade = "CP"
            else:
                self.interim_grade = "NC"
        self.final_grade_letter()

    def final_grade_letter(self):
        if self.interim_grade == "HD":
            self.final_grade = 4.0

        elif self.interim_grade == "D":
            self.final_grade = 3.0

        elif self.interim_grade == "C":
            self.final_grade = 2.0

        elif self.interim_grade == "P":
            self.final_grade = 1.0

        elif self.interim_grade == "SP":
            self.final_grade = 0.5

        elif self.interim_grade == "F":
            self.final_grade = 0

        elif self.interim_grade == "CP":
            self.final_grade = 4.0

        elif self.interim_grade == "NC":
            self.final_grade = 0


class Interface:
    """Class will be used to take user input and store them"""

    def initiate(self):
        options = """
        Choose one of the following options: 
        1 - Enter student grade information
        2 - Print all student grade information
        3 - Print class performance statistics
        4 - Exit
        """
        user_input = 10

        while user_input != '4':
            user_input = input(options)

            if user_input not in {'1', '2', '3', '4'}:
                print("Only enter a whole number between 1 and 4")
                return self.initiate()

            if user_input == '1':
                self.input_student_info_1()
            elif user_input == '2':
                self.input_student_info_2()
            elif user_input == '3':
                self.input_student_info_3()
            else:
                return 
            

                


    def input_student_info_1(self):
        student_detail_options = """
        Choose one of the following options:
        1.1 - Enter a BIT student information
        1.2 - Enter a DIT student information
        1.3 - Go back to the main menu
        """

        user_input = 10
        while user_input != "1.3":
            user_input = input(student_detail_options)
            if user_input not in {"1.1","1.2","1.3"}:
                print("invalid input")
                self.input_student_info_1()
            if user_input == "1.3":
                return self.initiate()

            student = Student()
            if user_input == "1.1":
                student.type = "BIT"
            else:
                student.type = "DIT"

            id = input("Enter student ID:")
            while student.add_student_id(id) == False:
                print("Entered invalid Student ID. ID start with A capital letter ‘A’ followed by 8 digits.")
                id = input("Enter student ID:")

            while True:
                name = input("Enter Student Name:")
                if student.add_student_name(name):
                    break
                
                

            assessment_marks = input("Enter student assessment marks (separated by comma):")
            while student.add_assessment_marks(assessment_marks) == False:
                print("Invalid Input")
                assessment_marks = input("Enter student assessment marks (separated by comma):")

            student.calculate_interim_grade()
            student_id_to_obj[student.id] = [student.id, student.name, student.type, student.final_grade, round(student.final_marks,2),student.AF_count,student.assessment_marks,student.interim_grade]



    def input_student_info_2(self):
        user_input=input("""
            >>> Choose one of the following options:
            >>> 2.1 - Print all student grade information ascendingly by final marks
            >>> 2.2 - Print all student grade information decendingly by final marks
            >>> 2.3 - Go back to main menu

        """)
        if user_input not in {"2.1","2.2","2.3"}:
            print("invalid input")
            self.input_student_info_2()

        if user_input=="2.1":
            self.ascend_final_marks()
        elif user_input=="2.2":
            self.descend_final_marks()
        return 


    def ascend_final_marks(self):
        self.sorted_list=sorted(student_id_to_obj.items(),key=lambda x: x[1][4])
        if len(self.sorted_list) == 0:
            print("Till now you have not given any student Details")
            return self.initiate()
        for j in range(len(self.sorted_list)):
            for i in range(5):
                print(self.sorted_list[j][1][i],end = " ")
            print()
        return


    def descend_final_marks(self):
        self.sorted_list=sorted(student_id_to_obj.items(),key=lambda x: x[1][4],reverse = True)
        if len(self.sorted_list) == 0:
            print("Till now you have not given any student Details")
            return self.initiate()
        for j in range(len(self.sorted_list)):
            for i in range(5):
                print(self.sorted_list[j][1][i],end = " ")
            print()
        return


    def input_student_info_3(self):
        n = len(student_id_to_obj)
        pass_rate = self.student_pass_rate()
        no_AF = self.count_AF()
        avg_1 = self.avg_as_1()
        avg_2 = self.avg_as_2()
        avg_3 = self.avg_as_3()
        avg_final = round((avg_1 + avg_2 + avg_3)/3,2)
        avg_grade_point = self.avg_grade_point()
        print("Total number of Student: ", n)
        print("Total number of Student in BIT: ", self.count_BIT())
        print("Total number of Student in DIT: ", self.count_DIT())
        print("Student Pass rate: ", round(pass_rate/n,2))
        print("Student Pass rate adjust: ", round(pass_rate/(n-no_AF),2))
        print("Average Marks for Assessment-1: ", avg_1)
        print("Average Marks for Assessment-2: ", avg_2)
        print("Average Marks for Assessment-3: ", avg_3)
        print("Average Marks for all Assessment: ", avg_final)
        print("Average Grade point for all Student: ", avg_grade_point)
        print("Total number of students who received a final grade letter HD: ", self.count_HD())
        print("Total number of students who received a final grade letter D: ", self.count_D())
        print("Total number of students who received a final grade letter C: ", self.count_C())
        print("Total number of students who received a final grade letter P: ", self.count_P())
        print("Total number of students who received a final grade letter SP: ", self.count_SP())
        print("Total number of students who received a final grade letter CP: ", self.count_CP())
        print("Total number of students who received a final grade letter F: ", self.count_F())

        return


    def count_BIT(self):
        count = 0
        for i in student_id_to_obj:
            if student_id_to_obj[i][2] == "BIT":
                count += 1
        return count

    def count_DIT(self):
        count = 0
        for i in student_id_to_obj:
            if student_id_to_obj[i][2] == "DIT":
                count += 1
        return count

    def student_pass_rate(self):
        count = 0
        for i in student_id_to_obj:
            if student_id_to_obj[i][3] != 0:
                count += 1
        return count

    def count_AF(self):
        count = 0
        for i in student_id_to_obj:
            if student_id_to_obj[i][5] != 0:
                count += 1
        return count

    def avg_as_1(self):
        count = 0
        n = len(student_id_to_obj)
        if n == 0:
            print("Give at least one Student Details")
            return self.initiate()
        for i in student_id_to_obj:
            count += student_id_to_obj[i][6][0]
        return round(count/n,2)

    def avg_as_2(self):
        count = 0
        n = len(student_id_to_obj)
        if n == 0:
            print("Give at least one Student Details")
            return self.initiate()
        for i in student_id_to_obj:
            count += student_id_to_obj[i][6][1]
        return round(count/n,2)

    def avg_as_3(self):
        count = 0
        n = len(student_id_to_obj)
        if n == 0:
            print("Give at least one Student Details")
            return self.initiate()
        for i in student_id_to_obj:
            count += student_id_to_obj[i][6][2]
        return round(count/n,2)

    def avg_grade_point(self):
        count = 0
        n = len(student_id_to_obj)
        if n == 0:
            print("Give at least one Student Details")
            return self.initiate()
        for i in student_id_to_obj:
            count += student_id_to_obj[i][3]
        return round(count/n,2)

    def count_HD(self):
        count = 0
        for i in student_id_to_obj:
            if student_id_to_obj[i][7] == "HD":
                count += 1
        return count
    def count_D(self):
        count = 0
        for i in student_id_to_obj:
            if student_id_to_obj[i][7] == "D":
                count += 1
        return count
    def count_C(self):
        count = 0
        for i in student_id_to_obj:
            if student_id_to_obj[i][7] == "C":
                count += 1
        return count
    def count_P(self):
        count = 0
        for i in student_id_to_obj:
            if student_id_to_obj[i][7] == "P":
                count += 1
        return count
    def count_SP(self):
        count = 0
        for i in student_id_to_obj:
            if student_id_to_obj[i][7] == "SP":
                count += 1
        return count
    def count_CP(self):
        count = 0
        for i in student_id_to_obj:
            if student_id_to_obj[i][7] == "CP":
                count += 1
        return count
    def count_F(self):
        count = 0
        for i in student_id_to_obj:
            if student_id_to_obj[i][7] == "F":
                count += 1
        return count


if __name__ == "__main__":
    Interface().initiate()