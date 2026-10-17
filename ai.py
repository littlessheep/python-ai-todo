import json
from openai import OpenAI
from dotenv import load_dotenv
from taskmanager import TaskMananger
import os
manage = TaskMananger()
def read_tasks():
    try:
        with open("tasks.json","r",encoding="utf-8") as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        print("没有找到文件")
def format_tasks(tasks):
    result = ""
    for task in tasks:
        result+= f"任务id:{task['task_id']}\n"
        result+= f"任务名称：{task['name']}\n"
        result+= f"任务内容：{task['content']}\n"
        result+= f"开始时间：{task['start_time']}\n"
        result+= f"结束时间:{task['end_time']}\n"
        result+= f"状态:{task['status']}\n"
        result+= f"优先级：{task['priority']}\n"
    return result
tasks = read_tasks()
task_text = format_tasks(tasks)
load_dotenv()
api_key = os.getenv("DEEPSEEK_API_KEY")
client = OpenAI(api_key = api_key,
                base_url= "https://api.deepseek.com")
while True:
    user_input = input("你想让我做什么：")
    tasks = read_tasks()
    task_text = format_tasks(tasks)
    prompt = f"""
    你是我的todo助手，

    下面是我的任务：

    {task_text}

    这是我刚刚对你的要求：

    {user_input}
    请根据我的任务和我的要求决定应该执行什么操作，优先度只有1-3，1最为紧急，3最为宽松

    如果用户要求创建任务，请严格按照下面的JSON格式返回：

    {{
        "action": "create_task",
        "name": "任务名称",
        "content": "任务内容",
        "start_time": "开始时间",
        "end_time": "结束时间",
        "priority": "优先度"
    }}

    如果用户要求删除任务，请严格按照下面的JSON格式返回：
    {{
        "action": "delete_task",
        "id":"任务id"
    }}

    如果用户要求查看任务，请严格按照下面的json格式返回：
    {{
        "action": "check_task",
        "id":"任务id"
    }}

    如果用户要求编辑任务，请严格按照下面的json格式返回：
    {{
        "action": "edit_task",
        "id":"任务id"
        "name": "任务名称",
        "content": "任务内容",
        "start_time": "开始时间",
        "end_time": "结束时间",
        "priority": "优先度"
    }}

    如果用户要求查看所有任务，请严格按照下面的json格式返回：
    {{
        "action": "checkall_task",
        "id":"任务id"
        "name": "任务名称",
        "content": "任务内容",
        "start_time": "开始时间",
        "end_time": "结束时间",
        "priority": "优先度"
    }}

    如果客户说他完成了一项任务，请查询相关数据，按照下面的json格式返回：
    {{
        "action": "finish_task",
        "id":"任务id"
    }}

    如果用户只是要求分析任务，则返回：

    {{
        "action": "analyze",
        "message": "你的分析内容"
    }}
    
    如果用户要求退出，则返回：
    {{
        "action":"exit"
    }}

    如果用户要求执行一个或者多个操作的时候，请统一把上述格式的内容写在下面的actions数组中。
    必须按照用户要求的顺序排序操作。如果用户只要求一个操作，actions数组中只包含一个操作。
    不要在actions数组之外输出任何其他字段。
    {
        "actions":[
        
        ]
    }
    不要输出JSON以外的内容。
    """
    response = client.chat.completions.create(
        model = "deepseek-flash",
        messages = [
            {
                "role":"user",
                "content": prompt
            }
        ]
    )
    result = response.choices[0].message.content
    datas = json.loads(result)#从json的字符串变成字典
    for data in datas:
        if data["action"] == "create_task":
            name = data["name"]
            content = data["content"]
            start_time = data["start_time"]
            end_time = data["end_time"]
            priority = data["priority"]
            manage.addtask(name,content,start_time,end_time,priority)


        elif data["action"] =="delete_task":
            manage.deletetask(int(data["id"]))

        elif data["action"] == "check_task":
            manage.checktask(int(data["id"]))

        elif data["action"] == "edit_task":
            manage.edittask(int(data["id"]),data["name"],data["content"],data["start_time"],data["end_time"],int(data["priority"]))

        elif data["action"] == "checkall_task":
            manage.checkall()

        elif data["action"] == "finish_task":
            manage.finish(int(data["id"]))

        elif data["action"] == "analyze":
            print(data["message"])

        elif data["action"] == "exit":
            break

