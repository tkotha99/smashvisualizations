from smashggpy.models.Event import Event
from smashggpy.util import Initializer
from smashggpy.util.QueryQueueDaemon import QueryQueueDaemon
import json, math
from collections import OrderedDict
playerWinsbyGame = {}
playerTop8sbyGame = {}
supermajorsByGame = {}
if __name__ == '__main__':
    Initializer.initialize('3822cb179c0315eedcb1065625e2606b', 'info')
    with open('tournamentlist.txt') as fp:
        tournaments = fp.readlines()
    tournaments = [tournament.rstrip() for tournament in tournaments]
    for idx,tournament in enumerate(tournaments):
        # if idx == 2:
        #     break
        if '/' not in tournament:
            continue
        event = Event.get_by_slug(tournament.split('/')[0],tournament.split('/')[1])
        placings = event.query_event_standings()
        if event.get_videogame() in supermajorsByGame:
            supermajorsByGame[event.get_videogame()] += 1
        else:
            supermajorsByGame[event.get_videogame()] = 1
        for placing in placings:
            tup = '({}, {})'.format(placing.get_gamer_tag(), event.get_videogame())
            if tup not in playerWinsbyGame:
                playerWinsbyGame[tup]= {
                    'wins' : 0,
                    'attended' : 0,
                    'wins/attended': 0,
                    'wins/total': 0,
                    'wins/total/time': []
                }
            if tup not in playerTop8sbyGame:
                playerTop8sbyGame[tup]= {
                    'top8s' : 0,
                    'attended' : 0,
                    'top8s/attended': 0,
                    'top8s/total': 0,
                    'top8s/total/time': []
                }
            playerWinsbyGame[tup]['attended'] += 1
            playerTop8sbyGame[tup]['attended'] += 1
            playerWinsbyGame[tup]['wins/attended'] = playerWinsbyGame[tup]['wins'] / playerWinsbyGame[tup]['attended']
            playerWinsbyGame[tup]['wins/total'] = playerWinsbyGame[tup]['wins'] / supermajorsByGame[event.get_videogame()]
            playerTop8sbyGame[tup]['top8s/attended'] = playerTop8sbyGame[tup]['top8s'] / playerTop8sbyGame[tup]['attended']
            playerTop8sbyGame[tup]['top8s/total'] = playerTop8sbyGame[tup]['top8s'] / supermajorsByGame[event.get_videogame()]
            playerWinsbyGame[tup]['wins/total/time'].append(playerWinsbyGame[tup]['wins/total'])
            playerTop8sbyGame[tup]['top8s/total/time'].append(playerTop8sbyGame[tup]['top8s/total'])
            if placing.get_placement() > 7:
                continue
            if placing.get_placement() == 1:
                playerWinsbyGame[tup]['wins'] += 1
                playerWinsbyGame[tup]['wins/attended'] = playerWinsbyGame[tup]['wins'] / playerWinsbyGame[tup]['attended']
                playerWinsbyGame[tup]['wins/total'] = playerWinsbyGame[tup]['wins'] / supermajorsByGame[event.get_videogame()]
                playerWinsbyGame[tup]['wins/total/time'].append(playerWinsbyGame[tup]['wins/total'])
            playerTop8sbyGame[tup]['top8s'] += 1
            playerTop8sbyGame[tup]['top8s/attended'] = playerTop8sbyGame[tup]['top8s'] / playerTop8sbyGame[tup]['attended']
            playerTop8sbyGame[tup]['top8s/total'] = playerTop8sbyGame[tup]['top8s'] / supermajorsByGame[event.get_videogame()]
            playerTop8sbyGame[tup]['top8s/total/time'].append(playerTop8sbyGame[tup]['top8s/total'])

    with open('output.txt', 'w') as outfile:
        outfile.write('ordered by wins/attended\n')
        json.dump(OrderedDict({k : v['wins/attended'] for k,v in sorted(playerWinsbyGame.items(), key=lambda ratio: ratio[1]['wins/attended'], reverse= True) if v['wins/attended'] > 0.0}), outfile)
        outfile.write('\nordered by top8s/attended\n')
        json.dump(OrderedDict({k : v['top8s/attended'] for k,v in sorted(playerTop8sbyGame.items(), key=lambda ratio: ratio[1]['top8s/attended'], reverse= True) if v['top8s/attended'] > 0.0}), outfile)
        outfile.write('\nordered by wins/total\n')
        json.dump(OrderedDict({k : v['wins/total'] for k,v in sorted(playerWinsbyGame.items(), key=lambda ratio: ratio[1]['wins/total'], reverse= True) if v['wins/total'] > 0.0}), outfile)
        outfile.write('\nordered by top8s/total\n')
        json.dump(OrderedDict({k : v['top8s/total'] for k,v in sorted(playerTop8sbyGame.items(), key=lambda ratio: ratio[1]['top8s/total'], reverse= True) if v['top8s/attended'] > 0.0}), outfile)
        

    QueryQueueDaemon.kill_daemon()