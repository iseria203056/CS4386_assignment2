import Game

class AIPlayer():
    def __init__(self):
        self.name='AIPlayer'

    def update_state(self,gametable_receive_tiles,gametable_receive_cnt,player_cnt,player_cnt_p,player_cnt_c,oppo_cnt_p,oppo_cnt_c):
        self.gametable_receive_tiles=gametable_receive_tiles
        self.gametable_receive_cnt=gametable_receive_cnt
        self.player_cnt = player_cnt
        self.player_cnt_p = player_cnt_p
        self.player_cnt_c = player_cnt_c
        self.oppo_cnt_p=oppo_cnt_p
        self.oppo_cnt_c=oppo_cnt_c
        
    def think_pong(self):
        #return true or false
        return True;
    def think_chow(self):
        #return 1,2,3 or 0
        return 0
    def think(self):
        for i in range(0, 9):
            if self.player_cnt[i] > 0:
                return i




