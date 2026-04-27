import csv
from random import choice
import sys
from collections import defaultdict

def load_csv_data(filename):
    #Load CSV data from file
    #data/degree_plans/matched/..matched_report.csv
    #read data from file
    with open(filename, newline='') as f:
        reader = csv.DictReader(f)
        return list(reader)

    #parse data into structured format
    #dict_data = {}
    #for row in data:
    #    year = row ['YEAR']
    #    term = row ['TERM']
    #    number = row ['NUM']
    #    subject = row ['SUBJ']
    #   title = row ['TITLE']


    #return data
    #return dict_data

def catagorize_grade(grade):
    if not grade or grade == '*':
            return None
    
    grade = grade.strip().upper()

    #sort grade into distribution
    if grade.startswith('A'):
        return 'A'
    elif grade.startswith('B'):
        return 'B'
    elif grade.startswith('C'):
        return 'C'
    elif grade.startswith('D', 'F', 'N'):
        return 'DNF'
    else:
        return None


def compute_grade_distribution(rows):
    #compute distribution from 'Grades' collumn
    counts = {'A': 0, 'B': 0, 'C': 0, 'DNF': 0}
    total = 0

    for row in rows:
        grade = catagorize_grade(row.get('GRADE'))
        if grade:
            counts[grade] += 1
            total += 1

    if total == 0:
        return counts
    
    return {k: round((v/total) * 100, 2) for k, v in counts.items()}

def group_by_course(rows):
    courses = defaultdict(list)

    for row in rows:
        subj = row.get('SUBJ', '').strip()
        num = row.get('NUM', '').strip()
        course_id = f"{subj} {num}"
        courses[course_id].append(row)

    return courses

def instructor_distribution(rows):
    #get instructor data
    instructors = defaultdict(list)
    for row in rows:
        instructor = row.get('INSTRUCTOR', 'UNKNOWN')
        instructors[instructor].append(row)

    results = {}
    for inst, inst_rows in instructors.items():
        results[inst] = compute_grade_distribution(inst_rows)

    return results

def rank_instructionors(distributions):
    #rank instructors based on distribution
    return sorted(distributions.items(), key = lambda x: x[1]['A'], reverse =True)


def filter_year(rows, start_year, end_year):
    filtered = []
    for row in rows: 
        term = row.get('TERM', '')
        if len(term) >= 4:
            year = int(term[:4])
            if start_year <= year <= end_year:
                filtered.append(row)

    return filtered
        
def anaylze_file(filename, start_year=None, end_year=None):
    data = load_csv_data(filename)
    if start_year and end_year:
        data = filter_year(data, start_year, end_year)

    courses = group_by_course(data)
    results = {}

    for course_id, rows in courses.items():
        results[course_id] = {
            "overall": compute_grade_distribution(rows),
            "instructors": instructor_distribution(rows)
        }

    return results 

def main():
    files = {
        "Architecture": "data/degree_plans/matched/architecture_matched_report.csv",
        "Computer Science": "data/degree_plans/matched/computer_science_matched_report.csv",
        "Psychology": "data/degree_plans/matched/psychology_matched_report.csv"
    }

    print("Avalilable majors: ")
    for key in files:
        print("-", key)

    choice = input("Choose major: ")
    if choice in files:
       start = int(input("Start year(e.g., 2015): "))
       end = int(input("End year(e.g., 2025): "))

       results = anaylze_file(files[choice], start, end)
       for course, data in results.items():
            print(f"\n {course}")
            print("Overall: ", (data)["overall"])
            ranked = rank_instructionors(data["instructors"])
            print ("top Instructor: ", ranked[0])

    else: print("Invalid choice")

if __name__ == "__main__":
    main()