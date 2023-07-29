import random


class Flight:
    def __init__(self, flight, fix, time, squawk, routes, entry_points, arr, pseudo, lvl, dep='X'):
        self.route = random.choice(routes[fix]['routes'])
        self.flight = flight
        self.callsign = self.flight[0]
        self.acft_type = self.flight[2][:-1]
        self.dep_airport = self.flight[1]
        self.dep_airport = dep
        self.arr_airport = arr
        self.heading = None
        self.star()
        self.pseudo = pseudo
        self.start = str(time)
        self.lvl = lvl
        self.squawk = squawk
        self.lat = entry_points[fix][0]
        self.lon = entry_points[fix][1]

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
