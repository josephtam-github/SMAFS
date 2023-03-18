from datetime import datetime
import re


def matric(num: int):
    """formats an integer into matriculation number"""
    now = datetime.now()
    year = now.strftime("%Y")
    return "U{}/{:03d}".format(year, num)


def dematric(mat_no: str):
    """turns matriculation number into integer"""
    student_id = re.search('/\d{3}$')
    return int(student_id)
