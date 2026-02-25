from .development import DevelopmentConfig
from .base import BaseConfig

config_by_name = {
    "development": DevelopmentConfig,
    "base": BaseConfig
}