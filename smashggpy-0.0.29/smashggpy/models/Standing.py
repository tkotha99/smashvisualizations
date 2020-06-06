class Standing(object):

    def __init__(self, id, gid, gamer_tag, placement):
        self.id = id
        self.gamer_id = gid
        self.gamer_tag = gamer_tag
        self.placement = placement
    
    def __str__(self):
        return "Placement: {}, Player: {}".format(self.placement, self.gamer_tag)


    @staticmethod
    def parse(data):
        return Standing(
            data['id'],
            data['entrant']['participants'][0]['player']['id'],
            data['entrant']['participants'][0]['player']['gamerTag'],
            data['placement']
        )

    # GETTERS
    def get_id(self):
        return self.id

    def get_gamer_id(self):
        return self.gamer_id

    def get_gamer_tag(self):
        return self.gamer_tag
    
    def get_placement(self):
        return self.placement
    