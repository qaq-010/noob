todo_list=[]

def todo_add():
    add_more = 0

    def print_test(add_more):
        if add_more==0:
            text = input("Enter your what you want to do:").strip()
            if text=="back":
                option=1
            else:
                option=0
            return text,option
        else:
            text = input("What else do you want to do(answer \"back\" to go back to operation):").strip()
            if text=="back":
                option=1
            else:
                option=0
            return text,option

    text_maxlength = 0
    while True:

        text,option=print_test(add_more)
        if len(text)>=50:
            print("Out of boundry.Please enter again")
            continue
        else:
            text_maxlength=max(text_maxlength,len(text))

        if text_maxlength<=20:
            grade=0
        else:
            grade=1
        if option==1:
            return grade
        if not text:
            print("Please input a text")
        else:
            if any(item["text"] == text for item in todo_list):
                print("Already have.Please enter again")
            else:
                todo_list.append({"text":text,"done":False})
                print("Successfully added")
                add_more=1


def todo_print(grade,index=-1):
    if not todo_list:
        print("There is no item to print")
        count=0
        return count

    else:
        count=0
        if grade==0:#grade1
            print("\t\t\t TODO    LIST")
            print("\tTask\t\t\t\t\t   Status\n")
            for item in todo_list:
                count+=1
                if count==index:
                    print(f"{count}.  {item['text']:<20}\t\t{item['done']}\t<-----(selected)")
                else:
                    print(f"{count}.  {item['text']:<20}\t\t{item['done']}")
            return count
        else:
            print(f"{' ':<27}TODO            LIST")
            print(f"{" ":<16}Task{' ':<39}Status\n")
            for item in todo_list:
                count += 1
                if count == index:
                    print(f"{count}.  {item['text']:<50}\t\t{item['done']}\t<-----(selected)")
                else:
                    print(f"{count}.  {item['text']:<50}\t\t{item['done']}")
            return count

def todo_mark():
    count=todo_print(grade)
    if count==0:
        print("There is no item to change.Please add some tasks")
    else:
        num=int(input(f"enter the text index you want to change,from 1 to {count}:"))
        todo_print(grade,num)
        while True:
            str=input("Do you want to change this item? \"yes or no\":").strip().lower()
            if str=="yes":
                todo_list[num-1]["done"]=not(todo_list[num-1]["done"])
                print("Successfully changed")
                todo_print(grade)
                break
            elif str=="no":
                break
            else:
                print("You should answer yes or no")  # 处理错误输入
                continue
def todo_delete():
    count = todo_print(grade)
    if count==0:
        print("There is no item to delete.Please add some tasks")
    else:
        num=int(input(f"Enter the item you want to delete,from 1 to {count}:"))
        todo_print(grade,num)
        while True:
            str=input("Do you want to delete this item? \"yes or no\":").strip().lower()
            if str=="yes":
                todo_list.remove(todo_list[num-1])
                print("Successfully deleted")
                todo_print(grade)
                break
            elif str=="no":
                break
            else:
                print("You should answer yes or no")#处理错误输入
                continue

def operation_menu():
    print("input \t\"print\" \tto show the todo list")
    print("input \t\"change\" \tto change the status of selected item")
    print("input \t\"delete\" \tto delete the selected item")
    print("input \t\"add\" \t\tto add a new item")

operation_menu()
grade=0
while True:
    choice=input("Enter your operation(input \"menu\" to show the operation menu):")
    match choice:
        case "print":
            todo_print(grade)
        case "change":
            todo_mark()
        case "add":
            grade=todo_add()
        case "delete":
            todo_delete()
        case "menu":
            operation_menu()
        case "exit":
            break
        case _:
            print("Please input a valid choice")
