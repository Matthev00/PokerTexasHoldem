import csv


class MalformedRecordDataError(Exception):
    pass


def read_file(file_handle):
    ranking = []
    reader = csv.DictReader(file_handle)
    try:
        for row in reader:
            place = row['place']
            name = row['name']
            score = row['score']
            if None in row.values():
                raise MalformedRecordDataError("Missing column in line")
            score = int(score)
            record = [place, name, score]
            ranking.append(record)
    except csv.Error as e:
        raise MalformedRecordDataError(str(e))
    return ranking


def write_to_file(file_handle, ranking):
    writer = csv.DictWriter(file_handle, ['place', 'name', 'score'])
    writer.writeheader()
    for record in ranking:
        place = record[0]
        name = record[1]
        score = record[2]
        writer.writerow({
            'place': place,
            'name': name,
            'score': score
        })
