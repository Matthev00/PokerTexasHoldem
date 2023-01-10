from ranking_io import read_file, write_to_file


class RankingPathNotFound(FileNotFoundError):
    def __init__(self):
        super().__init__("Could not open ranking database")


class RankingPermissionError(PermissionError):
    def __init__(self):
        super().__init__("You do not have permission to open the database")


class Database:
    def __init__(self):
        self.ranking = []

    def load_from_file(self, path='ranking.txt'):
        try:
            with open(path, 'r') as file_handle:
                self.ranking = read_file(file_handle)
        except FileNotFoundError:
            raise RankingPathNotFound()
        except PermissionError:
            raise RankingPermissionError()

    def save_to_file(self, path='ranking.txt'):
        try:
            with open(path, 'w') as file_handle:
                write_to_file(file_handle, self.ranking)
        except PermissionError:
            raise RankingPermissionError()

    def add_to_ranking(self, record):
        self.load_from_file()
        name, score = record
        place = 0
        for row in self.ranking:
            if score >= row[2]:
                place = row[0]
                break
        if place == 0:
            place = str(len(self.ranking)+1)
        new_record = [place, name, score]
        self.ranking.append(new_record)
        self.ranking = sorted(self.ranking, key=lambda x: x[2], reverse=True)
        self.ranking[0][0] = '1'
        for i in range(1, len(self.ranking)):
            if self.ranking[i][2] < self.ranking[i-1][2]:
                self.ranking[i][0] = str(i+1)
            elif self.ranking[i][2] == self.ranking[i-1][2]:
                self.ranking[i][0] = str(i)
        self.save_to_file()
        return place

    def print_ranking(self, num):
        place = 'Place'
        name = 'Name'
        score = 'Score'
        print(f'{place:>5}{name:>20}{score:>7}')
        for i in range(0, num):
            place = self.ranking[i][0]
            name = self.ranking[i][1]
            score = self.ranking[i][2]
            print(f'{place:>5}{name:>20}{score:>7}')
