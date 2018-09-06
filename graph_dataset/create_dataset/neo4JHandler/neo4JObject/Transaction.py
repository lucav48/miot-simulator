class Transaction:
    def __init__(self, c, s, d, dt, con, mes):
        self.code = str(c)
        self.source = s
        self.destination = d
        self.timestamp = dt
        self.context = con
        self.message = mes
