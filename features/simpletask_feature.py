from core.registry import TaskFeature, TaskFeatureRegistry

from domain.dtos.simpletask import SimpleTaskDTO, SimpleTaskFactory
from domain.handlers.simpletask_handler import SimpleTaskHandler
from domain.validation.simpletask_validator import SimpleTaskValidator


import logging

#from ui.widgets.simpletask import SimpleTaskDetails

simple_task_feature = TaskFeature(
    feature_name="simple_task",
    handler=SimpleTaskHandler,
    validator=SimpleTaskValidator,
    #detailview=SimpleTaskDetails,

)


TaskFeatureRegistry.add_feature(simple_task_feature)
logging.debug(f"Added SimpleTaskFeature to registry")