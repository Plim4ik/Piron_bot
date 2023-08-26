from aiogram import types
from ..help.minutes_calc import calculate_minutes
from config import ADMINS, SUBORDINATES, MAIN_PEOPLES

def calc_subordinate_salary(minutes):
    return (minutes // 150 + 1) * 1000

def calc_main_people_salary(subordinate_minutes, main_people_minutes):
    return subordinate_minutes * 5 + calc_subordinate_salary(main_people_minutes)

async def cmd_get_my_salary(message: types.Message):
    user_id = message.from_user.id
    minutes = calculate_minutes(user_id)  # предполагаем, что функция calculate_minutes принимает user_id и возвращает минуты для этого пользователя


    if user_id in SUBORDINATES:
        salary = calc_subordinate_salary(minutes)
        await message.answer(f"Ваша зарплата: {salary} руб.")
    elif user_id in MAIN_PEOPLES:
        total_subordinate_minutes = sum([calculate_minutes(sub_id) for sub_id in SUBORDINATES.values()])
        salary = calc_main_people_salary(total_subordinate_minutes, minutes)
        await message.answer(f"Ваша зарплата: {salary} руб.")
    else:
        await message.answer("Извините, у вас нет доступа к этому функционалу.")

async def cmd_get_full_salary_report(message: types.Message):
    if message.from_user.id not in ADMINS:
        await message.answer("Извините, у вас нет доступа к этому функционалу.")
        return

    report = "Отчет по зарплатам:\n"
    total_subordinate_minutes = sum([calculate_minutes(sub_id) for sub_id in SUBORDINATES.values()])

    for user_id, name in SUBORDINATES.items():
        minutes = calculate_minutes(user_id)
        salary = calc_subordinate_salary(minutes)
        report += f"{name}: {salary} руб.\n"

    for user_id, name in MAIN_PEOPLES.items():
        minutes = calculate_minutes(user_id)
        salary = calc_main_people_salary(total_subordinate_minutes, minutes)
        report += f"{name}: {salary} руб.\n"

    await message.answer(report)
