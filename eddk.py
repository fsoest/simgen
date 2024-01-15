import random
from argparse import ArgumentParser
from base import hdg, flights_entries
from flight import Flight

airport = 'eddk'
flights, entry_points = flights_entries(airport)


class DSFlight(Flight):
    def __init__(self, flight, fix, time, squawk, routes, entry_points):
        super().__init__(flight, fix, time, squawk, routes, entry_points, arr='EDDK', pseudo='EDDK_M_APP', lvl='21000')

    def star(self):
        if runway_in_use == 14:
            match self.route.split(' ')[-1]:
                case 'DEPOK':
                    self.heading = hdg(23)
                    self.route += ' DEPOK1V'
                    self.reqalt = 'NIVNU:18000'
                case 'GULKO':
                    self.heading = hdg(325)
                    self.route += ' GULKO1V'
                    self.reqalt = 'GULKO:11000'
                case 'KOPAG':
                    self.heading = hdg(238)
                    self.route += ' KOPAG2V'
                    self.reqalt = 'KOPAG:12000'
                case 'ERNEP':
                    self.heading = hdg(258)
                    self.route += ' ERNEP1V'
                    self.reqalt = 'ERNEP:10000'
        elif runway_in_use == 32:
            match self.route.split(' ')[-1]:
                case 'DEPOK':
                    self.heading = hdg(23)
                    self.route += ' DEPOK1C'
                    self.reqalt = 'NIVNU:18000'
                case 'GULKO':
                    self.heading = hdg(325)
                    self.route += ' GULKO1C'
                    self.reqalt = 'GULKO:11000'
                case 'KOPAG':
                    self.heading = hdg(238)
                    self.route += ' KOPAG2C'
                    self.reqalt = 'KOPAG:12000'
                case 'ERNEP':
                    self.heading = hdg(258)
                    self.route += ' ERNEP1C'
                    self.reqalt = 'ERNEP:10000'
        else:
            print('Wrong runway in use!')


def create_sim(t_final=120):
    acft = ''
    i = 0
    for t in range(t_final):
        for key, val in routes.items():
            if random.uniform(0, 1) < val['rate'] / 60 and val['block'] == 0:
                # Create aircraft
                flight = random.choice(flights)
                acft += DSFlight(flight, key, t, 1000, routes, entry_points).make_entry()
                flights.remove(flight)
                routes[key]['block'] = 2
                i += 1
            else:
                if val['block'] > 0:
                    val['block'] -= 1
    print(i)
    return acft


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('riu', type=int, help='Runway in use, 14 vs 32')
    parser.add_argument('rates', type=int, nargs=4, help='Rates of Entry points ADUSU(DEPOK), TABUM(GULKO), ESADU(KOPAG), BEBLA(BEBLA)')
    args = parser.parse_args()

    runway_in_use = args.riu
    routes = {
        'ADUSU': {
            'routes': ['ADUSU T856 DEPOK'],
            'rate': args.rates[0],
            'block': 0,
        },
        'TABUM': {
            'routes': ['TABUM T840 GULKO'],
            'rate': args.rates[1],
            'block': 0,
        },
        'ESADU': {
            'routes': ['ESADU T858 KOPAG'],
            'rate': args.rates[2],
            'block': 0,
        },
        'BEBLA': {
            'routes': ['BEBLA Y221 EBANA T841 ERNEP'],
            'rate': args.rates[3],
            'block': 0,
        },
    }

    with open(f'{airport}/ils_definition_{runway_in_use}.txt') as f:
        ils = f.read()
    with open(f'{airport}/airport_alt.txt') as f:
        ils += '\n'
        ils += f.read()
    with open('gen/controllers.txt') as f:
        ils += '\n'
        ils += f.read()
    with open(f'{airport}/holdings.txt') as f:
        ils += '\n'
        ils += f.read()
    with open('gen/acft_performance.txt') as f:
        ils += '\n'
        ils += f.read()
    with open(f'{airport}/dep_{runway_in_use}.txt') as f:
        deps = f.read()
    with open(f'{airport}/specials.txt') as f:
        ils += '\n'
        ils += f.read()
        ils += '\n'

    output = create_sim()

    with open(f'output_{airport}.txt', 'w') as f:
        f.write(ils)
        f.write(output)
        f.write('\n')
        f.write(deps)
