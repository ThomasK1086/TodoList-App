from domain.dtos.basetask import BaseTaskDTO
from domain.validation.basetask_validator import BaseTaskValidator


class SimpleTaskValidator(BaseTaskValidator):

    @classmethod
    def validate(cls, task: BaseTaskDTO) -> bool:
        return True