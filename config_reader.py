import yaml


class Config:
    def __init__(self):
        stream = open("config.yml", "r")
        docs = yaml.safe_load_all(stream)
        for doc in docs:
            for key,value in doc.items():
                if key == "baseURI":
                    self.BASE_URI = value
                if key == "makeFolders":
                    self.MAKE_FOLDERS = value
