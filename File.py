import csv


class File:

    def create_csv(self, filename, fields, content):
        with open(filename, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fields)
            writer.writeheader()
            for row in content:
                writer.writerow(row)

    def read_txt(self, filename):
        content = []
        with open(filename, 'r') as txtFile:
            for row in txtFile:
                content.append(row)
        return content
