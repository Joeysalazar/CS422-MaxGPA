engine = GradeAnalysisEngine()
csv_data = [
    {'TERM_DESC': 'Fall 2015', 'SUBJ': 'ARCH', 'NUMB': '119', 'CRN': '10358', 'INSTRUCTOR': 'Utsey, Glenda Helen'}
]

def load_csv_data():
    #Load CSV data from file
    dict_data = {}
    with open('course csv', 'r') as file:
        pass

    #return data
    return dict_data

def get_grade_distribution(courses):
    #get course data
    data = load_csv_data()

    #compute grade distribution
    grade_distribution = {}
    for course in data:
        for grade in course['grades']:
            if grade not in grade_distribution:
                grade_distribution[grade] = 0

            #sort grade into distribution
            if grade in ['AP', 'A', 'AM']:
                grade_a += 1
            elif grade in ['BP', 'B', 'BM']:
                grade_b += 1
            elif grade in ['CP', 'C', 'CM']:
                grade_c += 1
            elif grade in ['DP', 'D', 'DM', 'F', 'N']:
                grade_dnf += 1
            else:
                grade_other += 1
                
            grade_distribution[grade] += 1


    #return distribution
    return grade_distribution

def compare_instructors():
    #get instructor data
    instructor_data = load_csv_data()

    #compare instructors on grade distributions
    instructor_distribution = {}
    for instructor in instructor_data:
        instructor_distribution[instructor['name']] = get_grade_distribution(instructor['courses'])
        if instructor['name'] not in instructor_distribution:
            instructor_distribution[instructor['name']] = {}
        for course in instructor['courses']:
            for grade in course['grades']:
                if grade not in instructor_distribution[instructor['name']]:
                    instructor_distribution[instructor['name']][grade] = 0
                instructor_distribution[instructor['name']][grade] += 1

    
    #return metrics

def generate_analytics():
    #Load data
    #get distribution
    #get instructor comparison
    #return analytics


def summarize_results():
    #get analytics
    #summarize them into structured form
    #return summary 


