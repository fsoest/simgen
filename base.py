def hdg(heading):
    return str(int(heading * 2.88 + 0.5) << 2)


def flights_entries(path: str):
    with open(f'{path}/flights.csv') as f:
        lines = f.readlines()
        flights = [line.split(';') for line in lines]

    with open(f'{path}/entries.txt') as f:
        lines = f.readlines()
        entry_points = {}
        for line in lines:
            split = line.split(' ')
            entry_points[split[0]] = [split[1], split[2][:14]]

    return flights, entry_points
