import importlib
import pkgutil
from dataclasses import dataclass
import warnings
import logging

from utils.singleton import SingletonMetaclass

import features

@dataclass(frozen=True)
class Feature:
    feature_name: str

from domain.dtos.basetask import BaseTaskDTO
from domain.handlers.basetask_handler import BaseTaskHandler
from domain.validation.basetask_validator import BaseTaskValidator


@dataclass(frozen=True)
class TaskFeature(Feature):
    handler: type[BaseTaskHandler]
    validator: type[BaseTaskValidator]

logging.debug("Imported Feature Registry")

class TaskFeatureRegistry(metaclass=SingletonMetaclass):
    _registry = {}

    def __init__(self):
        self.load_features()

    @staticmethod
    def load_features():
        """Dynamically imports all modules in the features/ folder."""
        for loader, module_name, is_pkg in pkgutil.iter_modules(features.__path__):
            full_module_name = f"features.{module_name}"

            # This 'import_module' call triggers the code inside featureXY.py
            importlib.import_module(full_module_name)

    @classmethod
    def add_feature(cls, feature: Feature):
        logging.debug(f"Adding feature {feature.feature_name}")
        if feature.feature_name in cls._registry:
            warnings.warn(f"Tried to register feature {feature} with name {feature.feature_name}, but there is already a feature with that name! Skipping")
        else:
            cls._registry[feature.feature_name] = feature

    @classmethod
    def get(cls, feature_name: str) -> TaskFeature:
        if feature_name not in cls._registry.keys():
            raise ValueError(f"Unknown feature requested from registry: {feature_name}")
        else:
            return cls._registry[feature_name]

    @classmethod
    def get_feature(cls, feature_name: str) -> TaskFeature:
        return cls.get(feature_name)

