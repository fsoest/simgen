import random
from argparse import ArgumentParser


with open('edds/flights.csv') as f:
    lines = f.readlines()
    flights = [line.split(';') for line in lines]


def hdg(heading):
    return str(int(heading * 2.88 + 0.5) << 2)


with open('edds/entries.txt') as f:
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
        self.arr_airport = 'EDDS'
        self.heading = None
        self.star()
        self.pseudo = 'EDDS_M_APP'
        self.start = str(time)
        self.lvl = '18000'
        self.squawk = squawk
        self.lat = entry_points[fix][0]
        self.lon = entry_points[fix][1]

    def star(self):
        if runway_in_use == 7:
            match self.route.split(' ')[-1]:
                case 'BADSO':
                    self.heading = hdg(220)
                    self.route += ' BADSO07'
                    self.reqalt = 'INKAM:13000'
                case 'TEKSI':
                    self.heading = hdg(280)
                    self.route += ' TEKSI07'
                    self.reqalt = 'TEKSI:11000'
                case 'REUTL':
                    self.heading = hdg(360)
                    self.route += ' REUTL07'
                    self.reqalt = 'ARSUT:12000' if self.route.split(' ')[0] == 'LUPEN' else 'ARSUT:13000'
                case 'LBU':
                    self.heading = hdg(180)
                    self.route += ' LBU07'
                    self.reqalt = 'GEBNO:12000'
        elif runway_in_use == 25:
            match self.route.split(' ')[-1]:
                case 'BADSO':
                    self.heading = hdg(220)
                    self.route += ' BADSO25'
                    self.reqalt = 'INKAM:13000'
                case 'TEKSI':
                    self.heading = hdg(280)
                    self.route += ' TEKSI25'
                    self.reqalt = 'TEKSI:11000'
                case 'REUTL':
                    self.heading = hdg(360)
                    self.route += ' REUTL25'
                    self.reqalt = 'ARSUT:12000' if self.route.split(' ')[0] == 'LUPEN' else 'ARSUT:13000'
                case 'LBU':
                    self.heading = hdg(180)
                    self.route += ' LBU25'
                    self.reqalt = 'GEBNO:12000'
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
        entry += 'INITIALPSEUDOPILOT:{0}\n'.format(self.pseudo)
        entry += 'SIMDATA:{}:*:*:25:3:0\n\n'.format(self.callsign)
        return entry


def create_sim(t_final=120):
    acft = ''
    i = 0
    for t in range(t_final):
        for key, val in routes.items():
            if random.uniform(0, 1) < val['rate'] / 60 and val['block'] == 0:
                # Create aircraft
                flight = random.choice(flights)
                acft += Flight(flight, key, t, 1000).make_entry()
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
    parser.add_argument('riu', type=int, help='Runway in use, 7 vs 25')
    parser.add_argument('rates', type=int, nargs=5, help='Rates of Entry points BADSO, TEKSI, GARMO, LUPEN, LBU')
    args = parser.parse_args()

    runway_in_use = args.riu
    routes = {
        'UBENO': {
            'routes': ['UBENO N850 KRH T128 BADSO'],
            'rate': args.rates[0],
            'block': 0,
        },
        'RIDAR': {
            'routes': ['RIDAR Z79 ABGAS T129 TEKSI'],
            'rate': args.rates[1],
            'block': 0,
        },
        'GARMO': {
            'routes': ['GARMO T125 REUTL'],
            'rate': args.rates[2],
            'block': 0,
        },
        'LUPEN': {
            'routes': ['LUPEN T126 REUTL'],
            'rate': args.rates[3],
            'block': 0,
        },
        'TOSTU': {
            'routes': ['TOSTU T726 T726 LBU'],
            'rate': args.rates[4],
            'block': 0,
        },
    }

    with open('edds/ils_definition_{0}.txt'.format(runway_in_use)) as f:
        ils = f.read()
    with open('edds/airport_alt.txt') as f:
        ils += '\n'
        ils += f.read()
    with open('gen/controllers.txt') as f:
        ils += '\n'
        ils += f.read()
    with open('edds/holdings.txt') as f:
        ils += '\n'
        ils += f.read()
    with open('gen/acft_performance.txt') as f:
        ils += '\n'
        ils += f.read()
    with open('edds/dep_{0}.txt'.format(runway_in_use)) as f:
        deps = f.read()
    with open('edds/specials.txt') as f:
        ils += '\n'
        ils += f.read()
        ils += '\n'

    output = create_sim()

    with open('output_edds.txt', 'w') as f:
        f.write(ils)
        f.write(output)
        f.write('\n')
        f.write(deps)
