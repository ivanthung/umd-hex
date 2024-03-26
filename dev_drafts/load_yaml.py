""" Loading yaml data."""

import yaml
from dotmap import DotMap

config_path = 'dev_drafts/user_configs.yaml'

with open(config_path, 'r') as file:
    config_data = yaml.safe_load(file)

config = DotMap(config_data)

if __name__ == '__main__':
    print(config.user_id)
    print(config.local.building_profiles[0].path)