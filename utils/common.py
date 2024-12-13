import json


def build_swagger_config_json():
    config_file_path = 'static/swagger/config.json'

    with open(config_file_path, 'r') as file:
        config_data = json.load(file)

    config_data['servers'] = [
        {"url": "http://localhost:5000"},
    ]

    new_config_file_path = 'static/swagger/config.json'

    with open(new_config_file_path, 'w') as new_file:
        json.dump(config_data, new_file, indent=2)