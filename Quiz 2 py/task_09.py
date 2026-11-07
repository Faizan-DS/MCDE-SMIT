
def read_errors(path):
    with open(path, "r") as file:
        for number, line in enumerate(file, 1):
            try:
                date, level, message = line.strip().split(" | ")

                if level == "ERROR":
                    yield number, date, message

            except ValueError:
                continue


def summarize_errors(path):
    summary = {}

    for number, timestamp, message in read_errors(path):
        date = timestamp.split()[0]
        summary[date] = summary.get(date, 0) + 1

    return summary


for error in read_errors("logs.txt"):
    print(error)

print(summarize_errors("logs.txt"))
