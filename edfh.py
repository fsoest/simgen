import random
from argparse import ArgumentParser
from base import hdg, flights_entries
from flight import Flight


flights, entry_points = flights_entries('edfh')


class DSFlight(Flight):
    def __init__(self, flight, fix, time, squawk, routes, entry_points):
        super().__init__(flight, fix, time, squawk, routes, entry_points, arr='EDFH', pseudo='EDFH_M_APP', lvl='18000')

    def star(self):
        if runway_in_use == 3:
            match self.route.split(' ')[-1]:
                case 'EMGOD':
                    self.heading = hdg(207)
                    self.route += ' EMGOD3K'
                    self.reqalt = 'EMGOD:10000'
                case 'ROPUV':
                    self.heading = hdg(135)
                    self.route += ' ROPUV3K'
                    self.reqalt = 'SUXIM:15000'
                case 'OLGIL':
                    self.heading = hdg(264)
                    self.route += ' OLGIL1J'
                    self.reqalt = 'OLGIL:14000'
                case 'OLIVI':
                    self.heading = hdg(263)
                    self.route += ' OLIVI1J'
                    self.reqalt = 'OLIVI:10000'
        elif runway_in_use == 21:
            match self.route.split(' ')[-1]:
                case 'ROPUV':
                    self.heading = hdg(119)
                    self.route += ' ROPUV3A'
                    self.reqalt = 'SUXIM:15000'
                case 'ROLIS':
                    self.heading = hdg(241)
                    self.route += ' ROLIS3A'
                    self.reqalt = 'ROLIS:10000'
                case 'OLGIL':
                    self.heading = hdg(295)
                    self.route += ' OLGIL3B'
                    self.reqalt = 'OLGIL:14000'
                case 'OLIVI':
                    self.heading = hdg(349)
                    self.route += ' OLIVI3B'
                    self.reqalt = 'OLIVI:10000'
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
    parser.add_argument('riu', type=int, help='Runway in use, 3 vs 21')
    parser.add_argument('rates', type=int, nargs=5, help='Rates of Entry points OHMAR, SPI, KETEG, LEPSA, XIDOD')
    args = parser.parse_args()

    runway_in_use = args.riu
    routes = {
        'OHMAR': {
            'routes': ['OHMAR Z658 EMGOD'] if runway_in_use == 3 else ['OHMAR Z658 ROLIS'],
            'rate': args.rates[0],
            'block': 0,
        },
        'SPI': {
            'routes': ['SPI Q50 ARCKY L607 ROPUV'],
            'rate': args.rates[1],
            'block': 0,
        },
        'KETEG': {
            'routes': ['KETEG Z3 VATAK T840 EGAKA Z123 NOKDI Z104 OLGIL'],
            'rate': args.rates[2],
            'block': 0,
        },
        'LEPSA': {
            'routes': ['LEPSA Z104 OLGIL'],
            'rate': args.rates[2],
            'block': 0,
        },
        'XIDOD': {
            'routes': ['XIDOD Q762 OLIVI'],
            'rate': args.rates[3],
            'block': 0,
        },
        # 'OHMAR': {
        #     'routes': ['OHMAR Z658 ROLIS'],
        #     'rate': args.rates[4],
        #     'block': 0,
        # },
    }

    with open('edfh/ils_definition_{0}.txt'.format(runway_in_use)) as f:
        ils = f.read()
    with open('edfh/airport_alt.txt') as f:
        ils += '\n'
        ils += f.read()
    with open('gen/controllers.txt') as f:
        ils += '\n'
        ils += f.read()
    with open('edfh/holdings.txt') as f:
        ils += '\n'
        ils += f.read()
    with open('gen/acft_performance.txt') as f:
        ils += '\n'
        ils += f.read()
    with open('edfh/dep_{0}.txt'.format(runway_in_use)) as f:
        deps = f.read()
    with open('edfh/specials.txt') as f:
        ils += '\n'
        ils += f.read()
        ils += '\n'

    output = create_sim()

    with open('output_edfh.txt', 'w') as f:
        f.write(ils)
        f.write(output)
        f.write('\n')
        f.write(deps)
