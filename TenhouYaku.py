#! /usr/bin/python3

import TenhouDecoder
import collections
from Data import Data

YakuHanCounter = collections.namedtuple('YakuHanCounter', 'yaku han')

class YakuCounter(Data):
    def __init__(self, player_id):
        self.player_index = -1
        self.player_id = player_id
        self.hands = collections.Counter()
        self.closed = YakuHanCounter(collections.Counter(), collections.Counter())
        self.opened = YakuHanCounter(collections.Counter(), collections.Counter())
        self.all = YakuHanCounter(collections.Counter(), collections.Counter())

    def addGame(self, game):
        self.player_index = -1
        for idx, player in enumerate(game.players):
            if player.name == self.player_id:
                self.player_index = idx
                break
        for round in game.rounds:
            self.addRound(round)

    def addRound(self, round):
        for agari in round.agari:
            self.addAgari(agari)

    def addAgari(self, agari):
        counterYaku, counterHan = self.closed if agari.closed else self.opened
        allCounterYaku, allCounterHan = self.all
        self.hands["closed" if agari.closed else "opened"] += 1
        if self.player_index != -1 and self.player_index != agari.player:
            return
        if hasattr(agari, 'yaku'):
            for yaku, han in agari.yaku:
                counterYaku[yaku] += 1
                counterHan[yaku] += han
                allCounterYaku[yaku] += 1
                allCounterHan[yaku] += han
        if hasattr(agari, 'yakuman'):
            for yakuman in agari.yakuman:
                key = '___'+yakuman
                counterYaku[key] += 1
                counterHan[key] += 13
                allCounterYaku[key] += 1
                allCounterHan[key] += 13

if __name__ == '__main__':
    import sys
    import yaml
    counter = YakuCounter(None)
    for path in sys.argv[1:]:
        game = TenhouDecoder.Game()
        print(path)
        game.decode(open(path))
        counter.addGame(game)
    yaml.dump(counter.asdata(), sys.stdout, default_flow_style=False, allow_unicode=True)
