import configparser
import os


class ConfigReader:

    _config = None

    @classmethod
    def load_config(cls):

        if cls._config is not None:
            return cls._config

        config_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "config",
            "config.ini"
        )

        if not os.path.exists(config_path):
            raise FileNotFoundError(
                f"Config file not found at path: {config_path}"
            )

        parser = configparser.ConfigParser()
        parser.read(config_path, encoding="utf-8")

        if "app" not in parser:
            raise KeyError("[app] section is missing in config.ini")

        cls._config = parser

        return cls._config

    @classmethod
    def get(cls, key):

        config = cls.load_config()

        if key not in config["app"]:
            raise KeyError(f"{key} not found in config.ini")

        return config["app"][key].strip()

    @classmethod
    def get_base_url(cls):
        return cls.get("base_url")

    @classmethod
    def get_browser(cls):
        return cls.get("browser")

    @classmethod
    def get_timeout(cls):
        return int(cls.get("timeout"))

    @classmethod
    def get_implicit_wait(cls):
        return int(cls.get("implicit_wait"))

    @classmethod
    def get_mobile_number(cls):
        return cls.get("mobile_number")

    @classmethod
    def is_headless(cls):
        return cls.get("headless").lower() == "true"