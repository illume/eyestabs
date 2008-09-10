""" represents the player

Has a bunch of methods to 

"""


class Player:
    def __init__(self):
        self.eye_balls = 2

        # should we have different currencies?
        # What about bank accounts?
        self.cash = 20.0


        self.fans = 1

        self.stalker_fans = 1
        self.psyco_stalkers = 1

        self.real_friends = 4


        self.fake_online_friends = {}

        self.fake_online_friends['facebook'] = 2
        self.fake_online_friends['myspace'] = 3
        self.fake_online_friends['friendster'] = 4
        self.fake_online_friends['linkedin'] = 10




    def be_stabbed(self):
        """ we get stabbed in the eye... what does it do to us?
        """
        raise NotImplementedError("arg!  I've been stabbed in the eye!  oh noes.")


















