import csv


def get_grade(row: list[str], index_grade: int, index_comm: int):
    try:
        return int(row[index_grade][0]), row[index_comm]
    except ValueError:
        return None, row[index_grade] + ". " + row[index_comm]


def add_data(data: dict, dev_name: str, data_name: str, grade: int, comment: str):
    if grade is not None:
        if f"{data_name}_grades" not in data[dev_name].keys():
            data[dev_name][f"{data_name}_grades"] = [grade]
        else:
            data[dev_name][f"{data_name}_grades"].append(grade)

    if len(comment) > 0:
        if f"{data_name}_comments" not in data[dev_name].keys():
            data[dev_name][f"{data_name}_comments"] = [comment]
        else:
            data[dev_name][f"{data_name}_comments"].append(comment)


def write_data(file, data, name, local_name):
    file.write(f"\n## {local_name}\n")
    file.write(f"Оценки: " + ", ".join([str(grade) for grade in data[name + '_grades']]) + "\n")
    file.write(f"Средняя оценка: {avg(data[name + '_grades'])}\n")
    if f"{name}_comments" in data.keys() and len(data[f"{name}_comments"]) > 0:
        file.write("\n### Комментарии\n")
        for comment in data[f"{name}_comments"]:
            file.write(f"- {comment}\n")


def write_data_no_grade(file, data, name, local_name):
    file.write(f"\n## {local_name}\n")
    if f"{name}_comments" in data.keys() and len(data[f"{name}_comments"]) > 0:
        for comment in data[f"{name}_comments"]:
            file.write(f"- {comment}\n")


def avg(numbers):
    return round(sum(numbers)/len(numbers), 2)


data = {}

with open('os.csv', newline='', encoding='utf-8') as csvfile:
    rows = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in list(rows)[1:]:
        dev_name = row[1]

        prof_grade, prof_comment = get_grade(row, 2, 3)
        comm_grade, comm_comment = get_grade(row, 4, 5)
        lead_grade, lead_comment = get_grade(row, 6, 7)
        teamwork_grade, teamwork_comment = get_grade(row, 8, 9)
        result_grade, result_comment = get_grade(row, 10, 11)
        good, better = row[12], row[13]
        
        # print(dev_name)

        if dev_name not in data.keys(): data[dev_name] = {}

        add_data(data, dev_name, "prof", prof_grade, prof_comment)
        add_data(data, dev_name, "comm", comm_grade, comm_comment)
        add_data(data, dev_name, "lead", lead_grade, lead_comment)
        add_data(data, dev_name, "teamwork", teamwork_grade, teamwork_comment)
        add_data(data, dev_name, "result", result_grade, result_comment)
        add_data(data, dev_name, "good", None, good)
        add_data(data, dev_name, "better", None, better)


for dev_name, dev_data in data.items():
    with open(f"reports/{dev_name}.md", "w", encoding="utf-8") as f:
        f.write(f"# {dev_name}\n")
        f.write(f"Количество оценок: {len(dev_data['prof_grades'])}\n")

        write_data(f, dev_data, "prof", "Профессионализм")
        write_data(f, dev_data, "comm", "Коммуникации")
        write_data(f, dev_data, "lead", "Лидерство")
        write_data(f, dev_data, "teamwork", "Работа в команде")
        write_data(f, dev_data, "result", "Результативность")

        write_data_no_grade(f, dev_data, "good", "Что получается хорошо")
        write_data_no_grade(f, dev_data, "better", "Что стоит улучшить")
            
