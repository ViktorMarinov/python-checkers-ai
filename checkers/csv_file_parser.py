import csv


class CsvFileParser:
    def __init__(self, file_name):
        self.content = []
        self.__load_file(file_name)

    def __load_file(self, file_name):
        with open(file_name, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                self.content.append(row)

    def get_as_list(self):
        return map(lambda row: row[:8], self.content[:8])
