import datetime
import os

from domain.dtos.simpletask import SimpleTaskDTO
from domain.handlers.simpletask_handler import SimpleTaskHandler
from infrastructure.persistance.sqlite.task_dbconn import TaskDatabaseInterface

test_tasks = [
    SimpleTaskDTO(-1, 0, "simple_task", "Water the plastic plants", datetime.date(2024, 1, 10), "They don't need it, but it makes them feel included."),
    SimpleTaskDTO(-1, 1, "simple_task", "Organize the 'random cables' drawer", datetime.date(2024, 1, 12), "Find out if that 2004 Nokia charger still works."),
    SimpleTaskDTO(-1, 2, "simple_task", "Write a strongly worded letter to a cloud", datetime.date(2024, 1, 15), "It's been blocking the sun for three days straight."),
    SimpleTaskDTO(-1, 0, "simple_task", "Teach the cat about macroeconomics", datetime.date(2024, 1, 18), "He needs to understand why treats are subject to inflation."),
    SimpleTaskDTO(-1, 1, "simple_task", "Debug the toaster", datetime.date(2024, 1, 20), "It keeps burning the toast on 'setting 2' but leaves it bread on 'setting 1'."),
    SimpleTaskDTO(-1, 2, "simple_task", "Practice silence", datetime.date(2024, 1, 22), "Stare at a wall for 10 minutes without thinking about pizza."),
    SimpleTaskDTO(-1, 0, "simple_task", "Alphabetize the spice rack", datetime.date(2024, 1, 25), "Why do I have three jars of paprika? Investigation needed."),
    SimpleTaskDTO(-1, 1, "simple_task", "Buy a cape", datetime.date(2024, 1, 28), "For dramatic exits from Zoom meetings."),
    SimpleTaskDTO(-1, 2, "simple_task", "Research teleportation", datetime.date(2024, 2, 1), "The commute to the kitchen is becoming unbearable."),
    SimpleTaskDTO(-1, 0, "simple_task", "Apologize to the houseplants", datetime.date(2024, 2, 3), "I forgot to water the real ones while watering the plastic ones."),
    SimpleTaskDTO(-1, 1, "simple_task", "Find the end of the internet", datetime.date(2024, 2, 5), "I suspect it's a 404 page in a basement in Switzerland."),
    SimpleTaskDTO(-1, 2, "simple_task", "Learn to juggle sourdough starters", datetime.date(2024, 2, 8), "A high-stakes kitchen hobby."),
    SimpleTaskDTO(-1, 0, "simple_task", "Name the dust bunnies", datetime.date(2024, 2, 10), "The one under the couch looks like a 'Barnaby'."),
    SimpleTaskDTO(-1, 1, "simple_task", "Update 'The List'", datetime.date(2024, 2, 12), "The list of people who haven't returned my pens."),
    SimpleTaskDTO(-1, 2, "simple_task", "Invent a new color", datetime.date(2024, 2, 14), "Something between 'existential dread' and 'neon lime'."),
    SimpleTaskDTO(-1, 0, "simple_task", "Read the manual for the fridge", datetime.date(2024, 2, 16), "Does the light actually stay on when I close the door?"),
    SimpleTaskDTO(-1, 1, "simple_task", "Calculate the weight of a thought", datetime.date(2024, 2, 18), "Specifically the thought of eating a second donut."),
    SimpleTaskDTO(-1, 2, "simple_task", "Configure the flux capacitor", datetime.date(2024, 2, 20), "Requires exactly 1.21 gigawatts and a lot of patience."),
    SimpleTaskDTO(-1, 0, "simple_task", "Start a rumor about a ghost", datetime.date(2024, 2, 22), "Tell the neighbors the attic is haunted by a Victorian tech lead."),
    SimpleTaskDTO(-1, 1, "simple_task", "Clean the keyboard", datetime.date(2024, 2, 25), "I found enough crumbs to reconstruct a small muffin.")
]

handler = SimpleTaskHandler()
db_interface = TaskDatabaseInterface(db_name="todolist.sqlite")
for dto in test_tasks:
    s = handler.serialize(dto)
    db_interface.save_task(**s)