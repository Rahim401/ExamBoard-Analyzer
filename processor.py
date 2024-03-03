from re import findall

# pattern = r'(\w+)(?: Semester\n)(.*)(?:\nCourse Code:? )(\w+)(?: CIE Marks )(\d+)'
pattern = r'(\w+)(?: Semester ?\n)(.*)(?:\nCourse Code:? )(\w+)(?: .*\n.*\n.*\nCredits:? )(\d+)'
romanNum = ("", "I", "II", "III", "IV", "V", "VI", "VII", "VIII")

def getListOfSubjects(fromFile):
    with open(fromFile, "r") as file:
        rawData = file.read()

    subjectList = findall(pattern, rawData)
    return [(romanNum.index(subject[0]), subject[1], subject[2], subject[3]) for subject in subjectList]


    # print(rawData)


if __name__ == '__main__':
    for i in getListOfSubjects("C:\\Users\\RAHIM\\Desktop\\File.txt"):
        print(i)


# x= ["21MAT11","21CIV14","21MAT21","21PSP23", "21MAT31","21MAT41","21ALP75", "21ARC33","21ARC35","21ARC41","21ARC44","21ARC51","21ARC55","21ARC61","21ARC65","21ARC73","21ARC74","21ARC83","21ARC84", "21CH32", "21CHL35","21CH44", "21BE45", "21CH52", "21CH54", "21CH63", "21CH61", "21CH71", "21CH72", "21CS33", "21CS42", "21CS44", "21CS51", "21CS52", "21CS61", "21CS62", "21CS71", "21CS72", "21MT34", "21MT33", "21MT43", "21MT44", "21MT52", "21MTL55","21MT63", "21MTL66","21MT71", "21MT72", "21MT34"]