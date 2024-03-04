import json as js
from ExamBoardDb import ExamBoard
from sqlalchemy import create_engine, text


USER = "root"
PASSWORD = "fuckPass"
engine = create_engine(f"mysql+mysqlconnector://{USER}:{PASSWORD}@localhost")

fakeData = js.load(open("FakeData.json", "r"))
subjects = fakeData["subjects"]
courses = fakeData["courses"]
collage = fakeData["collage"]

db = ExamBoard(engine.connect())
# print(db.isExamBoardExists())
db.createExamBoard(True)
for subCode, name, credit in subjects: db.insertSubject(subCode, name, credit)
for courseCode, courseData in courses.items(): db.insertCourseEx(courseCode, courseData[0], courseData[1:])
for collageCode, collageData in collage.items(): db.insertCollageEx(collageCode, collageData[0], collageData[1])
db.generateClasses()
db.generateAndPlaceTeachers()
# db.generateAndAllocateStudents()
