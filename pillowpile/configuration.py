import os
import yaml

def read(config_file_path: str = None):
    default_config = yaml.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'server.yaml'), 'r'))
    real_path = config_file_path if config_file_path else 'server.yaml'
    if not os.path.exists(real_path):
        return default_config

    custom_config = yaml.load(open(real_path, 'r'))
    return {**default_config, **custom_config}
