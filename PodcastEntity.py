class PodcastEntity:
    def __init__(self, uid, name, url, amount, folderName, offset = 0, fromStrt = False, lastUpdated = ""):
        self.uid = uid
        self.name = name
        self.url = url
        self.amount = amount
        self.folderName = folderName
        self.offset = offset
        self.fromStart = fromStrt
        self.lastUpdated = lastUpdated
