import random
from argparse import ArgumentParser
from flight import Flight
from base import flights_entries, hdg


flights, entry_points = flights_entries('eduu_tgo')


class UUFlight(Flight):
    def __init__(self, flight, fix, time, squawk, routes, entry_points, arr, dep, lvl, route):
        super().__init__(flight, fix, time, squawk, routes, entry_points, arr=arr, pseudo='EDUU_M_CTR', lvl=lvl, dep=dep)
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
                acft = UUFlight(flight, key, t, 1000, routes, entry_points, val['arrs'][choice], val['dep'], lvl, val['routes'][choice])
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
    parser.add_argument('rates', type=int, nargs=5,
                        help='Rates of Entry points DEGES, IBAGA, PITES, POGOL, DITAM')
    args = parser.parse_args()

    routes = {
        'DEGES': {
            'routes': ['DEGES Z1 ETAGO N869 AMOSA Z77 LONLI M726 LASGA T202 ATGUP',
                       'DEGES Z1 ETAGO HAREM LOHRE ELNAT P605 NOLGO'],
            'arrs': ['EDDB', 'EDDH'],
            'dep': 'LSZH',
            'rate': args.rates[0],
            'block': 0,
            'heading': 45,
            'reqalt': 'ALAGO:24000',
            'alts': ['18000']
        },
        'IBAGA': {
            'routes': ['IBAGA DKB TEDGO T724 RILAX'],
            'arrs': ['LSZH'],
            'dep': 'EDDB',
            'rate': args.rates[1],
            'block': 0,
            'heading': 199,
            'reqalt': 'DKB:32000',
            'alts': ['32000', '34000', '36000', '38000', '30000']
        },
        'PITES': {
            'routes': ['PITES KRH BATUB M738 MADEB'],
            'arrs': ['LOWI'],
            'dep': 'EGLL',
            'rate': args.rates[2],
            'block': 0,
            'heading': 117,
            'reqalt': '',
            'alts': ['27000', '29000', '31000', '33000', '35000', '37000', '39000']
        },
        'OBAKI': {
            'routes': ['OBAKI UM164 LUPEN T107 ROKIL'],
            'arrs': ['EDDM'],
            'dep': 'LFPG',
            'rate': args.rates[3],
            'block': 0,
            'heading': 78,
            'alts': ['27000', '29000', '31000', '33000', '35000', '37000', '39000'],
            'reqalt': ''
        },
        'SUREP': {
            'routes': ['SUREP N871 DITON T163 EMPAX EMPAX5B'],
            'arrs': ['EDDF'],
            'dep': 'LEPA',
            'rate': args.rates[4],
            'block': 0,
            'heading': 47,
            'alts': ['30000', '32000', '34000', '36000', '38000'],
            'reqalt': ''
        }
    }

    with open('eduu_tgo/controllers.txt') as f:
        ils = f.read()

    output = create_sim(routes)

    with open('output_eduu_tgo.txt', 'w') as f:
        f.write(ils)
        f.write(output)
        f.write('\n')
