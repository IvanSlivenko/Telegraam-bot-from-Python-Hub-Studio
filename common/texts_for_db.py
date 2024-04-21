from aiogram.utils.formatting import Bold, as_list, as_marked_section

categories =['їжа', 'напої']

description_for_info_pages = {
    "main": "Ласкаво просимо",
    "about": as_marked_section(
        "Піцерія",
        Bold("Варіант"),
         Bold("Режим роботи :"),
        "Понеділок 9-00 -- 17-00\n",
        "Вівторок 9-00 -- 17-00\n",
        "Середа 9-00 -- 17-00\n",
        "Четвер 9-00 -- 17-00\n",
        "П-ятниця 9-00 -- 17-00\n",
        "Субота 9-00 -- 15-00\n",
        "Неділя - вихідний",
    ).as_html(),
    "payment": as_marked_section(
        Bold("Варіанти оплати :"),
            "Готівка",
            "Картка",
        marker='✔'
    ).as_html(),
    "shipping": as_list(
        as_marked_section(
        Bold("Варіанти доставки / замовлення :"),
            "Кур'єр",
            "Самовивіз",
            "Споживання в закладі",
            marker="✔",
        ),
        as_marked_section(Bold("Не відбувається :"), "Viber", "Email", marker="❌"),
        sep="\n-----------------------------\n",
    ).as_html(),
    "catalog": "Категорії",
    "cart": "В корзині нічого немає!"
}