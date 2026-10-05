#本程序使用了较多状态变量
"""grade用来表示task的长度等级，以便对齐图形界面
add_more为判断是否需要继续连续添加task
text_maxlength用来得到grade等级

"""
import json
from pathlib import Path

# 在当前路径下创造todojson
BASE_DIR = Path(__file__).resolve().parent
FILE = BASE_DIR / "todo.json"

#加载文件
def load_todos():
    #load_todos要在文件一开始就执行，先找这个json在不在
    if not FILE.exists():
        return []
    try:#判断json数据格式是否损坏，损坏就重新生成空列表
        with FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except json.JSONDecodeError:
        print("todo.json is damaged,it has been initialized as a new list")
        return []

#保存，在下面add,change,delete函数中，每做一次更改都save一次
def save_todos(todo_list):
    with FILE.open("w", encoding="utf-8") as f:
        json.dump(todo_list, f, ensure_ascii=False, indent=2)


#打印
def todo_print(todo_list, grade, index=-1):#传入的index为实现箭头selected图像来使用
    # 若todo list没有内容                                  在delete和change函数中，返回num当作index传入todo_print
    if not todo_list:
        print("There is no item to print")
        return 0

    count = 0
    if grade == 0:#grade=0为输入的task长度较少时
        print("\t\t\t TODO    LIST")
        print("\tTask\t\t\t\t\t   Status\n")
        for item in todo_list:
            count += 1
            mark = "\t<-----(selected)" if count == index else ""
            print(f"{count}.  {item['text']:<20}\t\t{item['done']}{mark}")
    else:#grade=1为输入的task长度较大时
        print(f"{' ':<27}TODO            LIST")
        print(f"{' ':<16}Task{' ':<39}Status\n")
        for item in todo_list:
            count += 1
            mark = "\t<-----(selected)" if count == index else ""
            print(f"{count}.  {item['text']:<50}\t\t{item['done']}{mark}")
    return count


# ---------- 添加 ----------
def todo_add(todo_list, grade):
    add_more = 0#用add_more状态变量去实现连续添加task的功能

    def ask(add_more):
        if add_more == 0:
            text = input("Enter what you want to do: ").strip()
        else:
            text = input('What else? (input "back" to go back): ').strip()
        option = 1 if text == "back" else 0#若用户输入back不想再继续添加，则用option状态变量传递出去
        return text, option

    text_maxlength = 0#用该参数去判断用户是否输入过长，处在合适范围内则给出不同grade值实现todolist图形界面的对齐
    while True:
        text, option = ask(add_more)

        if option == 1:
            return grade

        if len(text) >= 50:
            print("Out of boundary. Please enter again")
            continue

        text_maxlength = max(text_maxlength, len(text))
        grade = 0 if text_maxlength <= 20 else 1

        if not text:
            print("Please enter a text")
        elif any(item["text"] == text for item in todo_list):
            print("Already have. Please enter again")
        else:
            todo_list.append({"text": text, "done": False})
            save_todos(todo_list)
            print("Successfully added")
            add_more = 1


#修改status完成状况
def todo_mark(todo_list, grade):
    count = todo_print(todo_list, grade)
    if count == 0:
        print("There is no item to change. Please add some tasks")
        return

    while True:
        try:
            num = int(input(f"Enter index (1-{count}): "))
            if 1 <= num <= count:
                break
            else:
                print(f"Please make sure your number is from 1 to {count}")
        except ValueError:
            print("Please enter a number")

    todo_print(todo_list, grade, num)
    while True:
        ans = input('Do you want to change this item? "yes or no": ').strip().lower()#更改删除double check
        if ans == "yes":
            todo_list[num - 1]["done"] = not todo_list[num - 1]["done"]
            save_todos(todo_list)
            print("Successfully changed")
            todo_print(todo_list, grade)
            break
        elif ans == "no":
            break
        else:
            print("You should answer yes or no")


#删除某一行
def todo_delete(todo_list, grade):
    count = todo_print(todo_list, grade)
    if count == 0:
        print("There is no item to delete. Please add some tasks")
        return

    while True:
        try:
            num = int(input(f"Enter index (1-{count}): "))
            if 1 <= num <= count:
                break
            print(f"Please enter 1 to {count}")
        except ValueError:
            print("Please enter a number")

    todo_print(todo_list, grade, num)
    while True:
        ans = input('Do you want to delete this item? "yes or no": ').strip().lower()
        if ans == "yes":
            del todo_list[num - 1]
            save_todos(todo_list)
            print("Successfully deleted")
            todo_print(todo_list, grade)
            break
        elif ans == "no":
            break
        else:
            print("You should answer yes or no")



def operation_menu():
    print('input \t"print" \tto show the todo list')
    print('input \t"change" \tto change the status of selected item')
    print('input \t"delete" \tto delete the selected item')
    print('input \t"add" \t\tto add a new item')
    print('input \t"exit" \t\tto exit the program')


# ---------- 主程序 ----------
def main():
    todo_list = load_todos()
    grade = 0

    print(f"the path of json:{FILE}")#提示文件位置
    operation_menu()
    while True:
        choice = input('Enter your operation (input "menu" to show menu): ').strip().lower()
        match choice:
            case "print":
                todo_print(todo_list, grade)
            case "change":
                todo_mark(todo_list, grade)
            case "add":
                grade = todo_add(todo_list, grade)
            case "delete":
                todo_delete(todo_list, grade)
            case "menu":
                operation_menu()
            case "exit":
                print("Bye")
                break
            case _:
                print("Please input a valid choice")


if __name__ == "__main__":
    main()