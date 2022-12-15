import random
from argparse import ArgumentParser


restricted_heavies = ['B744', 'MD11', 'A388', 'B748', 'B742']

with open('eddf/flights.csv') as f:
    lines = f.readlines()
    flights = [line.split(';') for line in lines]


def hdg(heading):
    return str(int(heading * 2.88 + 0.5) << 2)


with open('eddf/entries.txt') as f:
    lines = f.readlines()
    entry_points = {}
    for line in lines:
        split = line.split(' ')
        entry_points[split[0]] = [split[1], split[2][:14]]


class Flight:
    def __init__(self, flight, fix, time, squawk):
        self.route = random.choice(routes[fix]['routes'])
        self.flight = flight
        self.callsign = self.flight[0]
        self.acft_type = self.flight[2][:-1]
        self.dep_airport = self.flight[1]
        self.dep_airport = 'X'
        self.arr_airport = 'EDDF'
        self.heading = None
        self.star()
        self.pseudo = 'EDDF_M_APP'
        self.start = str(time)
        self.lvl = '20000'
        self.squawk = squawk
        self.lat = entry_points[fix][0]
        self.lon = entry_points[fix][1]

    def star(self):
        if runway_in_use == 7:
            match self.route.split(' ')[-1]:
                case 'KERAX':
                    self.heading = hdg(220)
                    if self.acft_type in restricted_heavies:
                        self.route += ' KERAX3C/07'
                        self.reqalt = 'KERAX:12000'
                    else:
                        self.route += ' KERAX3D/07'
                        self.reqalt = 'KERAX:13000'
                case 'ROLIS':
                    self.heading = hdg(160)
                    if self.acft_type in restricted_heavies:
                        self.route += ' ROLIS3C/07'
                        self.reqalt = 'OSPUL:12000'
                    else:
                        self.route += ' ROLIS3D'
                        self.reqalt = 'ETARU:10000'
                case 'EMPAX':
                    self.heading = hdg(360)
                    self.route += ' EMPAX4C/07'
                    self.reqalt = 'ADNIS:10000'
                case 'FAWUR':
                    self.heading = hdg(320)
                    self.route += ' FAWUR2C/07'
                    self.reqalt = 'SPESA:11000'
                case 'SPESA':
                    self.heading = hdg(320)
                    self.route += ' SPESA3C/07'
                    self.reqalt = 'SPESA:11000'
                case 'UNOKO':
                    self.heading = hdg(80)
                    if self.acft_type in restricted_heavies:
                        self.route += ' UNOKO3C/07'
                        self.reqalt = 'RAMOB:13000'
                    else:
                        self.route += ' UNOKO3D/07'
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
                        self.route += ' KERAX3B/25'
                        self.reqalt = 'KERAX:10000'
                    else:
                        self.route += ' KERAX3A/25'
                        self.reqalt = 'KERAX:11000'
                case 'ROLIS':
                    self.heading = hdg(160)
                    if self.acft_type in restricted_heavies:
                        self.route += ' ROLIS3B/25'
                        self.reqalt = 'OSPUL:12000'
                    else:
                        self.route += ' ROLIS3A/25'
                        self.reqalt = 'ETARU:10000'
                case 'EMPAX':
                    self.heading = hdg(360)
                    self.route += ' EMPAX4B/25'
                    self.reqalt = 'ADNIS:10000'
                case 'FAWUR':
                    self.heading = hdg(320)
                    self.route += ' FAWUR2B/25'
                    self.reqalt = 'SPESA:11000'
                case 'SPESA':
                    self.heading = hdg(320)
                    self.route += ' SPESA3B/25'
                    self.reqalt = 'SPESA:11000'
                case 'UNOKO':
                    self.heading = hdg(80)
                    if self.acft_type in restricted_heavies:
                        self.route += ' UNOKO3B/25'
                        self.reqalt = 'RAMOB:13000'
                    else:
                        self.route += ' UNOKO3A/25'
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

    def make_entry(self):
        entry = ''
        entry += ':'.join(['@N', self.callsign, str(self.squawk), '1', self.lat, self.lon, self.lvl, '0', self.heading, '0\n'])
        entry += ':'.join(['$FP{0}'.format(self.callsign), '*A', 'I', self.acft_type, str(300), self.dep_airport, \
                           '1000', '1000', '390', self.arr_airport, '2', '50', '4', '00', 'EDDL', '/V/', self.route])
        entry += '\n'
        # entry += '$ROUTE:{0}\nSTART:{1}\nREQALT:{2}\n'.format(self.route, self.start, self.reqalt)
        entry += 'START:{0}\nREQALT:{1}\n'.format(self.start, self.reqalt)
        entry += 'INITIALPSEUDOPILOT:{0}\n\n'.format(self.pseudo)
        return entry


def create_sim(routes, t_final=120):
    acft = ''
    i = 0
    for t in range(t_final):
        for key, val in routes.items():
            if random.uniform(0, 1) < val['rate'] / 60 and val['block'] == 0:
                # Create aircraft
                flight = random.choice(flights)
                acft += Flight(flight, key, t, 1000).make_entry()
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
