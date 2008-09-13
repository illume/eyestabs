""" represents the player

Has a bunch of methods to 

"""


class Player:
    def __init__(self):
        self.eye_balls = 2
        self.spare_eye_balls = 0


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


    def get_stats_text(self):
        """
        """

        s = """eye_balls:%s
spare eye balls:%s
cash: $%s
fans:%s
stalker_fans:%s
psyco_stalkers:%s
real_friends:%s
fake_online_friends['facebook']:%s
fake_online_friends['myspace']:%s
fake_online_friends['friendster']:%s
fake_online_friends['linkedin']:%s""" % (self.eye_balls,
        self.spare_eye_balls,
        self.cash,
        self.fans,
        self.stalker_fans,
        self.psyco_stalkers,
        self.real_friends,
        self.fake_online_friends['facebook'],
        self.fake_online_friends['myspace'],
        self.fake_online_friends['friendster'],
        self.fake_online_friends['linkedin'],
        )
        return s



    def be_stabbed(self):
        """ we get stabbed in the eye... what does it do to us?
        """
        raise NotImplementedError("arg!  I've been stabbed in the eye!  oh noes.")








player = Player()









