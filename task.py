class Task:
  def __init__(self,task_id,name,content,start_time,end_time,priority,status = False):
    self.task_id = task_id
    self.name = name
    self.content = content
    self.start_time = start_time
    self.end_time = end_time
    self.status = status
    self.priority = priority
