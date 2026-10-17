from openai import OpenAI
from dotenv import load_dotenv
from taskmanager import TaskMananger
import os
import json

load_dotenv()
api_key = os.getenv("DEEPSEEK_API_KEY")
client = OpenAI(api_key = api_key,
                base_url="https://api.deepseek.com")
response = client.chat.completions.create(
    model = "deepseek-flash",
    messages=[
        {
            "role":"user",
            "content": """
            请帮我创建一个todo任务。
            用户需求：
            明天上午学习两小时python，优先级比较高。
            请严格按照以下JSON格式返回：
            {
            "name":"任务名称",
            "content":"任务内容",
            "start_time":"开始时间",
            "end_time":"结束时间",
            "priority":"任务优先级",
            }

            不要添加其他的文字，注意只有数字1，2，3，1表示优先级最高，3表示优先级最低。
            """
        }
    ]
)
ai_result = response.choices[0].message.content
task_data = json.loads(ai_result)
manage = TaskMananger()
manage.addtask(
    task_data["name"],
    task_data["content"],
    task_data["start_time"],
    task_data["end_time"],
    task_data["priority"]
)