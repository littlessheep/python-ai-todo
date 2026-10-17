from taskmanager import TaskMananger

def main():
 manage = TaskMananger()
 while True:
    print("请输入一个数字:1，建立一个新任务。2，查看一个任务。3，删除一个任务。4，编辑一个任务。5，查看现在保存的所有任务（优先度排序）。6，完成任务。7，退出")
    choice = input()
    match choice :
        case "1" : 
            print("建立一个新任务。请输入名字内容开始时间结束时间优先度，用中文逗号隔开")
            while True:
                data = input()
                while (len(data.split("，")) != 5):
                                print("输入错误，请输入名字内容开始时间结束时间优先度，用中文逗号隔开") 
                                data =input()
                name,content,start_time,end_time,priority = data.split("，")
                if(name.strip() == "" or content.strip() == "" or start_time.strip() == "" or end_time.strip() == ""  or priority ==""):
                    print("输入的字符中有空的字符串请重新输入")
                elif(not int(priority) in (1,2,3)):
                    print("优先度输入错误，请重新输入")
                else:
                    break
            manage.addtask(name,content,start_time,end_time,int(priority))
            print("成功建立该任务")

        case "2" : 
            print("查看一个任务,请输入id")
            while True:
                try:
                    data = input()
                    a = manage.checktask(int(data))
                    break
                except ValueError:
                    print("请输入一个数字")
            if a != None:
                print("name:" + a.name)
                print("content:" + a.content)
                print("start_time:" + a.start_time)
                print("end_time:" + a.end_time)
                print("status:" + str(a.status))
                print("priority" + str(a.priority))
            else:
                print("未找到该任务")


        case "3" : 
            print("删除一个任务，请输入id")
            while True:
                try:
                    data = input()
                    a = manage.deletetask(int(data))
                    break
                except ValueError:
                    print("请输入一个id")
            if a :
                print("已删除该任务")
            else:
                print("未找到该任务")
            
        case "4" : 
            print("编辑一个任务,请输入id名字内容开始时间结束时间优先度，用中文逗号隔开")
            while True:
                try:
                    data = input()
                    while(len(data.split("，")) != 6):
                        print("请输入五个字段")
                        data = input()
                    id,name,content,start_time,end_time,priority = data.split("，")
                    a = manage.edittask(int(id),name,content,start_time,end_time,priority)
                    break
                except ValueError:
                    print("请输入正确的数字")
                
            if a :
                print("已更新该任务")
            else:
                print("未找到该任务")

        case "5":
            manage.checkall()

        case "6":
            print("请输入完成任务的id")
            data = input()
            a = manage.finish(int(data))
            if a :
                print("已完成该任务")
            else:
                print("未找到该任务")

        case "7":
            break

        case _:
            print("请输入1到5之间的数字")


if __name__ == "__main__":
    main()      