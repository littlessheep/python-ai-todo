import json
from task import Task

class TaskMananger :
    def __init__ (self):
        self.tasks = []
        self.nextid = 0
        self.loadtasks()

    def addtask(self,name,content,start_time,end_time,priority):
        self.nextid = self.nextid + 1
        task = Task(self.nextid,name,content,start_time,end_time,priority)
        self.tasks.append(task)
        self.savetasks()

    def deletetask(self,task_id):
        for task in self.tasks:
            if task.task_id == task_id:
                self.tasks.remove(task)
                self.savetasks()
                return True
        return False

    def checktask(self, task_id):
        for task in self.tasks:
            if task.task_id == task_id:
                return task

    def edittask(self,task_id,name,content,start_time,end_time,priority):
        for task in self.tasks:
            if task.task_id == task_id:
               task.name = name
               task.content = content
               task.start_time = start_time
               task.end_time = end_time
               task.priority = priority
               self.savetasks()
               return True 
        return False

    def checkall(self):
        if len(self.tasks) == 0:
            print("当前没有任务")
        else:
            sorted_tasks = sorted(self.tasks, key= lambda task : task.priority)
        for task in sorted_tasks:
            print("当前任务id:" + str(task.task_id) )
            print("当前任务名字：" + task.name)
            print("当前任务内容：" + task.content)
            print("当前任务开始时间：" + task.start_time)
            print("当前任务结束时间:" + task.end_time)
            print("当前任务的状态是:" + str(task.status))
            print("当前任务的优先性是:" + str(task.priority))
            print()

    def finish(self,task_id):
        for task in self.tasks:
            if task.task_id == task_id:
                task.status = True
                return True
        return False


    def savetasks(self):
        data = []
        for task in self.tasks:
            task_data = {
                "task_id": task.task_id,
                "name" : task.name,
                "content" : task.content,
                "start_time": task.start_time,
                "end_time": task.end_time,
                "priority": task.priority,
                "status": task.status
            }
            data.append(task_data)
        with open("tasks.json" , "w",encoding= "utf-8") as f:
            json.dump(data,f,ensure_ascii=False ,indent=4)

    def loadtasks(self):
        try:
            with open("tasks.json", "r" , encoding="utf-8") as f:
                data = json.load(f)
                for item in data:
                    task = Task(
                        item["task_id"],
                        item["name"],
                        item["content"],
                        item["start_time"],
                        item["end_time"],
                        item["priority"],
                        item["status"],
                    )
                    self.tasks.append(task)
                    if task.task_id > self.nextid:
                        self.nextid = task.task_id
        except FileNotFoundError:
            pass

            