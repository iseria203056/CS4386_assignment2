import Game
from ctypes import *
def init(player):
    print(player.AI_name,player.language)
    if player.AI_name == None:
        player.AI_name = player.name

    if player.AI_name == 'AIPlayer':
        if player.language=="CPP":
            import sys
            aiplayer=CDLL('./cpp/aiplayer.so')
            print("===========")
        elif player.language=="JAVA":
            import jpype
            AIPlayer = jpype.JClass('com.AIPlayer')
            aiplayer=AIPlayer()
        else:
            from python.AIPlayer import AIPlayer
            aiplayer=AIPlayer()
            
        return aiplayer
    elif player.AI_name == 'human':
        return human()
    else:
        print("no%s"%player.AI_name)
        return None

class human():
    def __init__(self):
        self.name='human'

    def Print_tiles(self):
        print("Your current tiles:")
        T_list = [None] * 8
        k = 0
        for t in range(0, 9):
            e = self.player_cnt[t]
            if e:
                t_name = Game.get_tile_name(t)
                while (e > 0):
                    T_list[k] = t
                    print(t_name, end="\t")
                    k += 1
                    e -= 1
        print()
        return k, T_list

    def Print_peng_tiles(self):
        out=""
        for i in range(0, 9):
            e = self.player_cnt_p[i]
            if e:
                t_name = Game.get_tile_name(i)
                while (e > 0):
                    out += t_name+"x3\t"
                    e -= 1
        if out == "":
            print("Tiles you have pong:\tNone\n")
        else:
            out += "\n"
            print("Tiles you have pong:\t",out)
            
    def Print_chow_tiles(self):
        out=""
        for i in range(0, 9):
            e = self.player_cnt_c[i]
            if e:
                t_name = Game.get_tile_name(i)
                while (e > 0):
                    out += t_name+" "+Game.get_tile_name(i+1)+" "+Game.get_tile_name(i+2)+"\t"
                    e -= 1
        if out == "":
            print("Tiles you have chow:\tNone\n")
        else:
            out += "\n"
            print("Tiles you have chow:\t",out)

    def update_state(self,gametable_receive_tiles,gametable_receive_cnt,player_cnt,player_cnt_p,player_cnt_c,oppo_cnt_p,oppo_cnt_c):
        self.gametable_receive_tiles=gametable_receive_tiles
        self.gametable_receive_cnt=gametable_receive_cnt
        self.player_cnt = player_cnt
        self.player_cnt_p = player_cnt_p
        self.player_cnt_c = player_cnt_c
        self.oppo_cnt_p=oppo_cnt_p
        self.oppo_cnt_c=oppo_cnt_c
            
    def think_pong(self):
        self.Print_tiles()
        print("You can pong: ",Game.get_tile_name(self.gametable_receive_tiles[-1][1]),"\ndo you want to pong？(1yes,2no)")
        ans=input()
        if ans =="1":
            return True
        elif ans == "2":
            return False
        
    def think_chow(self):
        self.Print_tiles()
        print("You can chow: ",Game.get_tile_name(self.gametable_receive_tiles[-1][1]),"\ndo you want to chow？(1,2,3,0)")
        ans=input()
        tile=self.gametable_receive_tiles[-1][1]
        if ans =="1":
            return 1

        elif ans == "2":
            return 2

        elif ans =="3":
            return 3

        else:
            print("you don't want to chow" )
            return 0
        return 0
        
    def think(self):

        print("Tiles have been droped:",end="\t")
        for t in range(0,9):
            if self.gametable_receive_cnt[t]:
                print(Game.get_tile_name(t),"x",self.gametable_receive_cnt[t],end="\t")
        print("\n")

        self.Print_peng_tiles()
        self.Print_chow_tiles()
        k,T_list = self.Print_tiles()
        

        print("\n")
        print("Input the tile you want to drop")
        o = input()
        return int(o)-1




