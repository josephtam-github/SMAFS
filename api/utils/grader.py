def letter_grade(percent_grade: int):
    """Convert grade from percentage value to a letter"""
    if percent_grade >= 90:
        return 'A'
    elif 90 > percent_grade >= 80:
        return 'B'
    elif 80 > percent_grade >= 70:
        return 'C'
    elif 70 > percent_grade >= 60:
        return 'D'
    elif 60 > percent_grade >= 50:
        return 'E'
    else:
        return 'F'
