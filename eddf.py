import random
from argparse import ArgumentParser
from base import hdg, flights_entries
from flight import Flight


restricted_heavies = ['B744', 'MD11', 'A388', 'B748', 'B742']

flights, entry_points = flights_entries('eddf')


class DFFlight(Flight):
    def __init__(self, flight, fix, time, squawk, routes, entry_points):
        super().__init__(flight, fix, time, squawk, routes, entry_points, arr='EDDF', pseudo='EDDF_M_APP', lvl='20000')

    def star(self):
        if runway_in_use == 7:
            match self.route.split(' ')[-1]:
                case 'KERAX':
                    self.heading = hdg(220)
                    if self.acft_type in restricted_heavies:
                        self.route += ' KERAX4C/07'
                        self.reqalt = 'KERAX:12000'
                    else:
                        self.route += ' KERAX4D/07'
                        self.reqalt = 'KERAX:13000'
                case 'ROLIS':
                    self.heading = hdg(160)
                    if self.acft_type in restricted_heavies:
                        self.route += ' ROLIS4C/07'
                        self.reqalt = 'OSPUL:12000'
                    else:
                        self.route += ' ROLIS4D/07'
                        self.reqalt = 'ETARU:10000'
                case 'EMPAX':
                    self.heading = hdg(360)
                    self.route += ' EMPAX5C/07'
                    self.reqalt = 'ADNIS:10000'
                case 'FAWUR':
                    self.heading = hdg(320)
                    self.route += ' FAWUR3C/07'
                    self.reqalt = 'SPESA:11000'
                case 'SPESA':
                    self.heading = hdg(320)
                    self.route += ' SPESA4C/07'
                    self.reqalt = 'SPESA:11000'
                case 'UNOKO':
                    self.heading = hdg(80)
                    if self.acft_type in restricted_heavies:
                        self.route += ' UNOKO4C/07'
                        self.reqalt = 'RAMOB:13000'
                    else:
                        self.route += ' UNOKO4D/07'
                        self.reqalt = 'RAMOB:11000'
                case 'RAMOB':
                    self.heading = hdg(60)
                    if self.acft_type in restricted_heavies:
                        self.route += ' DF431 DF631 DF632 DFFFM DF621 DF622 DF623 DF613 DF612 DF611 DF635 DF636 DF640 DF641 DF642 DF643 DF644'
                        self.reqalt = 'RAMOB:13000'
                    else:
                        self.route += ' DF431 DF432 DF439 DF441 DF442 DF443 DF444'
                        self.reqalt = 'RAMOB:11000'
        elif runway_in_use == 25:
            match self.route.split(' ')[-1]:
                case 'KERAX':
                    self.heading = hdg(220)
                    if self.acft_type in restricted_heavies:
                        self.route += ' KERAX4B/25'
                        self.reqalt = 'KERAX:10000'
                    else:
                        self.route += ' KERAX4A/25'
                        self.reqalt = 'KERAX:11000'
                case 'ROLIS':
                    self.heading = hdg(160)
                    if self.acft_type in restricted_heavies:
                        self.route += ' ROLIS4B/25'
                        self.reqalt = 'OSPUL:12000'
                    else:
                        self.route += ' ROLIS4A/25'
                        self.reqalt = 'ETARU:10000'
                case 'EMPAX':
                    self.heading = hdg(360)
                    self.route += ' EMPAX5B/25'
                    self.reqalt = 'ADNIS:10000'
                case 'FAWUR':
                    self.heading = hdg(320)
                    self.route += ' FAWUR3B/25'
                    self.reqalt = 'SPESA:11000'
                case 'SPESA':
                    self.heading = hdg(320)
                    self.route += ' SPESA4B/25'
                    self.reqalt = 'SPESA:11000'
                case 'UNOKO':
                    self.heading = hdg(80)
                    if self.acft_type in restricted_heavies:
                        self.route += ' UNOKO4B/25'
                        self.reqalt = 'RAMOB:13000'
                    else:
                        self.route += ' UNOKO4A/25'
                        self.reqalt = 'RAMOB:11000'
                case 'RAMOB':
                    self.heading = hdg(60)
                    if self.acft_type in restricted_heavies:
                        self.route += ' DF401 DF600 DF609 DF610 DF611 DF612 DF613 DF614 DF615 DF616'
                        self.reqalt = 'RAMOB:13000'
                    else:
                        self.route += ' DF401 DF402 DF403 DF409 DF410 DF411 DF412 DF413 DF414 DF415 DF416'
                        self.reqalt = 'RAMOB:11000'
        else:
            print('Wrong runway in use!')


def create_sim(routes, t_final=120):
    even_levels = ['']
    acft = ''
    i = 0
    for t in range(t_final):
        for key, val in routes.items():
            if random.uniform(0, 1) < val['rate'] / 60 and val['block'] == 0:
                # Create aircraft
                flight = random.choice(flights)
                acft += DFFlight(flight, key, t, 1000, routes, entry_points).make_entry()
                flights.remove(flight)
                routes[key]['block'] = 1
                i += 1
            else:
                if val['block'] > 0:
                    val['block'] -= 1
    print(i)
    return acft


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('riu', type=int, help='Runway in use, 7 vs 25')
    parser.add_argument('rates', type=int, nargs=5,
                        help='Rates of Entry points KERAX, ROLIS, EMPAX, SPESA, UNOKO')
    args = parser.parse_args()

    runway_in_use = args.riu

    routes = {
        'ROBEL': {
            'routes': ['ROBEL T178 KERAX', 'ROBEL KERAX'],
            'rate': args.rates[0],
            'block': 0,
        },
        'COL': {
            'routes': ['COL T911 ROLIS'],
            'rate': args.rates[1],
            'block': 0,
        },
        'LADOL': {
            'routes': ['LADOL T163 EMPAX'],
            'rate': args.rates[2],
            'block': 0,
        },
        'GIMAX': {
            'routes': ['GIMAX T161 FAWUR', 'GIMAX T161 SPESA'],
            'rate': args.rates[3],
            'block': 0,
        },
        'NIVNU': {
            'routes': ['NIVNU T180 UNOKO'],
            'rate': args.rates[4],
            'block': 0,
        },
    }

    with open('eddf/ils_definition_{0}.txt'.format(runway_in_use)) as f:
        ils = f.read()
    with open('eddf/airport_alt.txt') as f:
        ils += '\n'
        ils += f.read()
    with open('gen/controllers.txt') as f:
        ils += '\n'
        ils += f.read()
    with open('eddf/holdings.txt') as f:
        ils += '\n'
        ils += f.read()
    with open('gen/acft_performance.txt') as f:
        ils += '\n'
        ils += f.read()
    with open('eddf/dep_{0}.txt'.format(runway_in_use)) as f:
        deps = f.read()
    with open('eddf/specials.txt') as f:
        ils += '\n'
        ils += f.read()
        ils += '\n'

    output = create_sim(routes)

    with open('output_eddf.txt', 'w') as f:
        f.write(ils)
        f.write(output)
        f.write('\n')
        f.write(deps)
