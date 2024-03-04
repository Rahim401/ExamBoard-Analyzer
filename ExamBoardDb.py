import random

from sqlalchemy import Connection, text
from sqlalchemy.exc import SQLAlchemyError


class ExamBoard:
    DbName = "ExamBoard"
    DbMakeFile = "ExamBoardMaker"

    def __init__(self, sqlConn:Connection):
        self.sqlConn = sqlConn
        # self.createExamBoard()
        self.executeStatement("use examboard;", printError=False)

    def isExamBoardExists(self):
        result = self.executeStatement("show databases;", printError=False).scalars().all()
        return ExamBoard.DbName.lower() in result
    def createExamBoard(self, forceCreate=False):
        if self.isExamBoardExists():
            if forceCreate: self.dropExamBoard()
            else: return
        with open(ExamBoard.DbMakeFile) as file:
            allQuery = file.read().replace("\n", "").replace("\t", "")\
                .replace("    ", "").split(";")
            try:
                for query in allQuery: self.sqlConn.execute(text(query))
            except Exception as e: print("Error on creating database: ", e)
    def executeStatement(self, statement, commit = False, printError = True):
        try:
            result = self.sqlConn.execute(text(statement))
            if commit: self.sqlConn.commit()
            return result
        except SQLAlchemyError as error:
            if printError: print(f"Error while executing: {statement}\n{error}")

    def insertSubject(self, subCode, name, credit):
        statement = f"INSERT INTO Subject (subCode, name, credit) VALUES ('{subCode}', '{name}', {credit});"
        self.executeStatement(statement, True)
        # print(self.sqlConn.execute(text("select * from subject")).all())
    def insertCourse(self, courseCode, name):
        statement = f"INSERT INTO Course (courseCode, name) VALUES ('{courseCode}', '{name}')"
        self.executeStatement(statement, True)
    def insertCollage(self, clgCode, name):
        statement = f"INSERT INTO Collage (clgCode, name) VALUES ('{clgCode}', '{name}')"
        self.executeStatement(statement, True)
    def insertClass(self, classId, clgCode, courseCode, sem, sec):
        statement = f"INSERT INTO Class (classId, clgCode, courseCode, sem, sec) VALUES ('{classId}', '{clgCode}', '{courseCode}', {sem}, '{sec}')"
        self.executeStatement(statement, True)
    def insertTeacher(self, name):
        statement = f"INSERT INTO Teacher (name) VALUES ( '{name}')"
        self.executeStatement(statement, True)
        return self.executeStatement("SELECT LAST_INSERT_ID();").first()[0]
    def insertStudent(self, name):
        statement = f"INSERT INTO Student (name) VALUES ('{name}')"
        self.executeStatement(statement, True)
        return self.executeStatement("SELECT LAST_INSERT_ID();").first()[0]
    def insertExamMarks(self, studentId, sem, subCode, marks):
        statement = f"INSERT INTO ExamMarks (studentId, sem, subCode, marks) VALUES ({studentId}, {sem}, '{subCode}', {marks})"
        self.executeStatement(statement, True)

    def insertSubjectInCourse(self, courseCode, sem, subCode):
        statement = f"INSERT INTO SubjectInCourse (courseCode, sem, subCode) VALUES ('{courseCode}', {sem}, '{subCode}')"
        self.executeStatement(statement, True)
    def insertCoursesInCollage(self, clgCode, courseCode):
        statement = f"INSERT INTO CoursesInCollage (clgCode, courseCode) VALUES ('{clgCode}', '{courseCode}')"
        self.executeStatement(statement, True)
    def insertTeacherInClasses(self, teacherId, classId, subCode):
        statement = f"INSERT INTO TeacherInClasses (teacherId, classId, subCode) VALUES ({teacherId}, '{classId}', '{subCode}')"
        self.executeStatement(statement, True)
    def insertStudentInClasses(self, studentId, sem, classId):
        statement = f"INSERT INTO StudentInClasses (studentId, sem, classId) VALUES ({studentId}, {sem}, '{classId}')"
        self.executeStatement(statement, True)

    def insertCourseEx(self, courseCode, name, subjects):
        self.insertCourse(courseCode, name)
        for sem, subjects in enumerate(subjects, 1):
            for subCode in subjects:
                self.insertSubjectInCourse(courseCode, sem, subCode)
    def insertCollageEx(self, clgCode, name, courses):
        self.insertCollage(clgCode, name)
        for courseCode in courses:
            self.insertCoursesInCollage(clgCode, courseCode)
    def generateClasses(self, noOfSem=4, noOfSec=2):
        listOfClgCourses = self.executeStatement("select * from CoursesInCollage;").all()
        for clgCode, courseCode in listOfClgCourses:
            for sem in range(1, noOfSem+1):
                for sec in "ABCDEFGH"[:noOfSec]:
                    self.insertClass(f"{clgCode}BE{courseCode}{sem}{sec}", clgCode, courseCode, sem, sec)
    def generateAndPlaceTeachers(self, canHandelRange=(12, 20)):
        query = """
            select c.classId, sc.subCode 
            from Class c,SubjectInCourse sc
            where c.courseCode = sc.courseCode and c.sem = sc.sem
        """
        listOfClassSub = list(self.executeStatement(query).all())
        rd = random.Random()

        while len(listOfClassSub) > 0:
            teacherId = self.insertTeacher("Paith Yam")
            canHandel = rd.randint(*canHandelRange)
            for i in range(min(canHandel, len(listOfClassSub))):
                idx = rd.randint(0, len(listOfClassSub)-1)
                classId, subCode = listOfClassSub.pop(idx)
                self.insertTeacherInClasses(teacherId, classId, subCode)

    def generateAndAllocateStudents(self, classStrengthRange=(5, 10)):
        listOfClass = list(self.executeStatement("select sem,classId from class;").all())
        rd = random.Random()

        for sem, classId in listOfClass:
            classStrength = rd.randint(*classStrengthRange)
            for _ in range(classStrength):
                studentId = self.insertStudent("Puda Karan")
                print("Inserting ", sem, classId, studentId)
                self.insertStudentInClasses(studentId, sem, classId)

    def generateStudentMarks(self, tillSem=8):
        query = """
            select c.classId, sc.subCode 
            from Class c,SubjectInCourse sc
            where c.courseCode = sc.courseCode and c.sem = sc.sem
        """
        listOfClassSub = list(self.executeStatement(query).all())
        rd = random.Random()

        # while len(listOfClassSub) > 0:
        #     teacherId = self.insertTeacher("Paith Yam")
        #     canHandel = rd.randint(*canHandelRange)
        #     for i in range(min(canHandel, len(listOfClassSub))):
        #         idx = rd.randint(0, len(listOfClassSub) - 1)
        #         classId, subCode = listOfClassSub.pop(idx)

        # teachersNeed = len(listOfClassSub)/teacherCanHandel


        # for clgCode, courseCode in listOfClgCourses:
        #     for sem in range(1, noOfSem+1):
        #         for sec in "ABCDEFGH"[:noOfSec]:
        #             self.insertClass(f"{clgCode}BE{courseCode}{sem}{sec}", clgCode, courseCode, sem, sec)
        # print(listOfClgCourses)


    def dropExamBoard(self):
        self.executeStatement(f"drop database {ExamBoard.DbName};", printError=False)
