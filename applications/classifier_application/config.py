import yaml


class ClassifierAppConfig:
    """
    The application configuration parameters.

    :param filepath: Path of the configuration(.yaml) file
    """

    def __init__(self, filepath):
        self._app_config = self._load_yaml(filepath)
        self.source_directory = self._app_config["streams"]["input_folder"]
        self.app_fps = self._app_config["app_fps"]
        self.classifier_model = self._app_config["models"]["image_classifier"]
        self.process_idx = self._app_config["process_index"]

    def _load_yaml(self, filepath):
        with open(filepath, "r") as file:
            loaded_file = yaml.safe_load(file)
        return loaded_file
