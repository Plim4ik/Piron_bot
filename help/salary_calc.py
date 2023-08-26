from config import SUBORDINATES, MAIN_PEOPLES

def calc_subordinate_salary(minutes):
    return (minutes // 150 + 1) * 1000

def calc_main_people_salary(subordinate_minutes, main_people_minutes):
    return subordinate_minutes * 5 + calc_subordinate_salary(main_people_minutes)

def calculate_salaries(minutes_summary):
    salaries = {}
    total_subordinate_minutes = sum([minutes for employee, minutes in minutes_summary.items() if employee in SUBORDINATES.values()])

    for user_id, name in SUBORDINATES.items():
        minutes = minutes_summary.get(name, 0)
        salaries[name] = calc_subordinate_salary(minutes)

    for user_id, name in MAIN_PEOPLES.items():
        minutes = minutes_summary.get(name, 0)
        salaries[name] = calc_main_people_salary(total_subordinate_minutes, minutes)

    return salaries
