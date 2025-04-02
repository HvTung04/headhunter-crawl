import pandas as pd

class OutputSheet:
    def __init__(self, data):
        self.sheet = pd.DataFrame(data)

    def save(self, file_path):
        self.sheet.to_excel(file_path, index=True)