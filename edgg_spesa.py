import random
from argparse import ArgumentParser
from flight import Flight
from base import flights_entries, hdg


flights, entry_points = flights_entries('edgg_spesa')


class DKBFlight(Flight):
    def __init__(self, flight, fix, time, squawk, routes, entry_points, arr, dep, lvl, route):
        super().__init__(flight, fix, time, squawk, routes, entry_points, arr=arr, pseudo='EDGG_M_CTR', lvl=lvl, dep=dep)
        self.route = route


def create_sim(routes, t_final=60):
    acfts = ''
    i = 0
    for t in range(t_final):
        for key, val in routes.items():
            if random.uniform(0, 1) < val['rate'] / 60 and val['block'] == 0:
                flight = random.choice(flights)
                choice = random.choice(range(len(val['routes'])))
                lvl = random.choice(val['alts'])
                acft = DKBFlight(flight, key, t, 1000, routes, entry_points, val['arrs'][choice], val['dep'], lvl, val['routes'][choice])
                if val['reqalt'] == '':
                    acft.reqalt = key + ':' + lvl
                else:
                    acft.reqalt = val['reqalt']
                acft.heading = hdg(val['heading'])
                if key != 'DEGES':
                    acfts += acft.make_entry(rfl=lvl[:3])
                elif key == 'DEGES':
                    acfts += acft.make_entry(['350', '340'][choice])
                flights.remove(flight)
                routes[key]['block'] = 1
                i += 1
            else:
                if val['block'] > 0:
                    val['block'] -= 1
    print(i)
    return acfts


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('rates', type=int, nargs=4,
                        help='Rates of Entry points ERNAS, DF159, EMPAX, DN107')
    args = parser.parse_args()

    routes = {
        'ERNAS': {
            'routes': ['ARSIN DCT SUBEN DCT AKINI T161 DEBHI DEBHI1B',
                       'SUBEN T161 DEBHI DEBHI1B'],
            'arrs': ['EDDF','EDDF'],
            'dep': 'EDDM',
            'rate': args.rates[0],
            'block': 0,
            'heading': 300,
            'reqalt': 'ASPAT:24000',
            'alts': ['30000', '32000', '34000', '36000', '38000']
        },
        'DF159': {
            'routes': ['DF159 AMTIX CINDY GIBSA COSJE SULUS L984 KULOK',
                       'DF159 AMTIX CINDY GIBSA COSJE SULUS L984 KULOK',
                       'DF159 AMTIX CINDY Z74 HAREM' ],
            'arrs': ['EDDB', 'EPWA', 'EDDM'],
            'dep': 'EDDF',
            'rate': args.rates[1],
            'block': 0,
            'heading': 119,
            'reqalt': 'AMTIX:11000',
            'alts': ['4000', '3500', '3000']
        },
        'EMPAX': {
            'routes': ['ESOKO GODRA LADOL T163 EMPAX EMPAX5B'],
            'arrs': ['EDDF'],
            'dep': 'LOWI',
            'rate': args.rates[2],
            'block': 0,
            'heading': 359,
            'reqalt': 'KOVAN:25000',
            'alts': ['30000', '32000', '34000', '36000', '38000'],
        },
        'DN107': {
            'routes': ['DN107 DN105 DN109 SUKAD T159 SPESA SPESA4B'],
            'arrs': ['EDDF'],
            'dep': 'EDDN',
            'rate': args.rates[3],
            'block': 0,
            'heading': 180,
            'reqalt': 'DN107:20000',
            'alts': ['7000'],
        }
    }

    with open('edgg_spesa/controllers.txt') as f:
        ils = f.read()

    output = create_sim(routes)

    with open('output_edgg_spesa.txt', 'w') as f:
        f.write(ils)
        f.write(output)
        f.write('\n')
