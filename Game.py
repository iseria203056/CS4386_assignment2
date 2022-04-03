from random import shuffle
from copy import deepcopy
import AI
from time import time
from jpype import *
import ctypes
class Game():
    globle_name_set=set()
    def __init__(self,name,is_show = 'normal',Player_names=["player1","player2"], AI_names = ['AIPlaer','AIPlayer'],AI_languages=['PYTHON','Human'],debug = False ,Rules={"Shoot":False, "Pong": False, "Chow":False}):

        self.name=name
        self.debug = debug
        self.gametable= Gametable(debug)
        self.is_show=is_show #'mute','little','normal','full'

        self.players_list=[Player(self.gametable,Rules,Player_names[0],AI_names[0],AI_languages[0],self.is_show),
                            Player(self.gametable,Rules,Player_names[1],AI_names[1],AI_languages[1],self.is_show)]
        self.Rules=Rules
        self.gamestate=0
        self.game_round = 0
        self.turn = 0

    def play(self,r):
        self.game_round = r
        self.time_count={'whole_time':0,'round_time':[0]*r}

        for p in self.players_list:
            p.win_n=0
        whole_start_t = time()
        while(r>0):
            self.gametable.shuffle()
            self.start()
            self.turn=1
            r_start_t = time()
            while(self.gamestate==1):
                if self.is_show in ['normal','full']:
                    print("\n\nThe %d round"%self.turn)
                self.turn+=1
                i=0
                while i<2 and (self.gamestate==1):
                    
                    if self.players_list[i].draw(self.gametable):
                        if self.is_win(self.players_list[i]):
                            break

                    else:
                        if self.is_show != 'mute':
                            print("draw")
                        self.gamestate = 3
                        break

                    if self.players_list[i].drop(self.gametable,self.players_list[1-i])==False:
                        self.gametable=0
                        print("Player "+str(self.players_list[i].AI_name)+" gives invalid tile to drop. Game ends!!!")
                        return False
                    if True:
                        k=1-i
                        if self.players_list[k].action(self.gametable,self.players_list[1-k]):
                            if self.is_win(self.players_list[k]):
                                break
                            i = k
                            self.players_list[i].drop(self.gametable,self.players_list[1-i])
                    i += 1
            for p in self.players_list:
                p.reset()
            r_end_t = time()
            self.time_count['round_time'][self.game_round-r]=r_end_t-r_start_t
            r -= 1
            #print("end",self.turn)
        whole_end_t = time()
        self.time_count['whole_time'] = whole_end_t - whole_start_t

    def start(self):
        for i in range(0, 7):
            for p in self.players_list:
                p.draw(self.gametable)
        self.gamestate=1

    def is_win(self,p):
        if p.hu_judge():
            self.winner = p.name
            self.gamestate = 2
            p.win_n += 1
            if self.is_show != 'mute':
                p.show("Hu")
                print("!!!The winner is:", self.winner, "\n")
            return True
        return False

    def print_win_rate(self):
        for p in self.players_list:
                print(p.name+" ("+p.AI_name+") win rate: %f"%(p.win_n / self.game_round))

class Player():

    globle_name_list=['']

    def __init__(self,gametable,Rules,name = str(len(globle_name_list)),AI_name = None,AI_language=None,is_show='normal'):
        self.gametable = gametable
        self.language=AI_language
        self.set_name(name)
        self.set_AI(AI_name)
        if is_show == 'little':
            is_show = 'mute'
        
        self.is_show = is_show
        self.reset()
        self.Rules=Rules
        self.win_n = 0

    def set_name(self,name):
        self.name=name
        Player.globle_name_list.append(name)

    def set_AI(self,AI_name):
        self.AI_name = AI_name
        self.AI = AI.init(self)

    def reset(self):
        self.cnt = [0] * 9  # 0-8:"W"
        self.cnt_p = [0] * 9
        self.cnt_c=[0]*9
        self.last_draw = -1
        self.peng = 0
        self.chi = 0
        self.state = True

    def show(self,type,tile = -1):
        if self.is_show == 'mute':
            pass
        elif self.is_show == 'normal':
            if type == 'Get tile':
                print(self.name, ":", type,  end=" ")
            elif type == 'Drop Tile':
                print(self.name,":", type, get_tile_name(tile), end="\n")
            elif type == 'Hu':
                print(self.name,":I Hu-ed!")
                self.show_tiles()
            else:
                print("wrong type")
        elif self.is_show == 'full':
            print(self.name, type, get_tile_name(tile))
            self.show_tiles()
        else:
            print("wrong display mode: should be mute,normal or full")

    def get_tiles_names(self):
        s = "Player: "+self.name+" -> "
        return s + get_Cnt_names(self.cnt)
    
    def show_tiles(self):
        print(self.get_tiles_names())


    def draw(self,gametable = None):
        if gametable == None:
            gametable = self.gametable

        t=gametable.draw()

        if t!="End":
            self.cnt[t]+=1
            self.last_draw=t
            self.show("Get tile",t)

            return True
        elif t=="End":
            return False

    def drop(self,gametable  = None,opponent=None):
        if gametable == None:
            gametable = self.gametable
        self.updateAI(gametable,opponent)
        t=self.AI.think()
        if self.cnt[t]<=0:
             return False
        if t==None:
            print(t)
        self.cnt[t] -= 1
        gametable._receive(self.name,t)
        self.show("Drop tile", t)
    def updateAI(self,gametable,opponent):

            
        python_a1=gametable.receive_tiles
        python_a2=gametable.receive_cnt
        python_a3=self.cnt
        python_a4=self.cnt_p
        python_a5=self.cnt_c
        python_a6=opponent.cnt_p
        python_a7=opponent.cnt_c

        if self.language=="PYTHON" or self.language=="Human":
            self.AI.update_state(python_a1,python_a2,python_a3,python_a4,python_a5,python_a6,python_a7)
        elif self.language=="JAVA":
            java_a1 = java.util.ArrayList()
            for i in range(len(python_a1)):
                pair= java.util.ArrayList()
                for j in range(2):
                    pair.add(python_a1[i][j])
                java_a1.add(pair)

            java_a2 = java.util.ArrayList()
            for i in range(len(python_a2)):
                java_a2.add(python_a2[i])

            java_a3=java.util.ArrayList()
            for i in range(len(python_a3)):
                java_a3.add(python_a3[i])

            java_a4=java.util.ArrayList()
            for i in range(len(python_a4)):
                java_a4.add(python_a4[i])

            java_a5=java.util.ArrayList()
            for i in range(len(python_a5)):
                java_a5.add(python_a5[i])
                
            java_a6=java.util.ArrayList()
            for i in range(len(python_a6)):
                java_a6.add(python_a6[i])

            java_a7=java.util.ArrayList()
            for i in range(len(python_a7)):
                java_a7.add(python_a7[i])
                
            self.AI.update_state(java_a1,java_a2,java_a3,java_a4,java_a5,java_a6,java_a7)
        else:
            l1=len(python_a1)

            int_arr2 = ctypes.c_int*2
            int_arr2n = int_arr2*22
            cpp_a1 = int_arr2n()
            for i in range(l1):
                for j in range(2):
                    cpp_a1[i][j]=ctypes.c_int(python_a1[i][j])
            for i in range(l1,12):
                for j in range(2):
                    cpp_a1[i][j]=ctypes.c_int(0)


            int_arr9 = ctypes.c_int*9
            cpp_a2 = int_arr9()
            for i in range(9):
                cpp_a2[i]=ctypes.c_int(python_a2[i])
            
            cpp_a3 = int_arr9()
            for i in range(9):
                cpp_a3[i]=ctypes.c_int(python_a3[i])
                

            cpp_a4 = int_arr9()
            for i in range(9):
                cpp_a4[i]=ctypes.c_int(python_a4[i])

            cpp_a5 = int_arr9()
            for i in range(9):
                cpp_a5[i]=ctypes.c_int(python_a5[i])
                
            cpp_a6 = int_arr9()
            for i in range(9):
                cpp_a6[i]=ctypes.c_int(python_a6[i])

            cpp_a7 = int_arr9()
            for i in range(9):
                cpp_a7[i]=ctypes.c_int(python_a7[i])
                
            self.AI.update_state(cpp_a1,cpp_a2,cpp_a3,cpp_a4,cpp_a5,cpp_a6,cpp_a7)
            

            
    def action(self,gametable = None,opponent=None):
        if gametable == None:
            gametable = self.gametable

        if self.Rules["Shoot"]:
            self.cnt[gametable.receive_tiles[-1][1]] += 1
            if self.hu_judge():
                if self.is_show in ["normal", "full"]:
                    print("player",gametable.receive_tiles[-1][0],"gives card shooting to",self.name,get_tile_name(gametable.receive_tiles[-1][1]),sep=" ")
                return True
            self.cnt[gametable.receive_tiles[-1][1]] -= 1

        if self.Rules["Pong"]:
            if self.cnt[gametable.receive_tiles[-1][1]]==2:

                self.cnt[gametable.receive_tiles[-1][1]] += 1
                if self.hu_judge():
                    return False
                self.cnt[gametable.receive_tiles[-1][1]] -= 1
                self.updateAI(gametable,opponent)
                if self.AI.think_pong():
                    self.cnt_p[gametable.receive_tiles[-1][1]]+=1
                    self.cnt[gametable.receive_tiles[-1][1]] -= 2
                    self.peng +=1
                    if self.is_show in ["normal","full"]:
                        print("\n",self.name,"pong player",gametable.receive_tiles[-1][0],"'s",get_tile_name(gametable.receive_tiles[-1][1]))
                    return True
        if self.Rules["Chow"]:
            tile=gametable.receive_tiles[-1][1]

            if (tile>0 and tile<8 and self.cnt[tile-1]>0 and self.cnt[tile+1]>0) or (tile<7 and self.cnt[tile+1]>0 and self.cnt[tile+2]>0) or (tile>1 and self.cnt[tile-2]>0 and self.cnt[tile-1]>0):
           
                self.cnt[gametable.receive_tiles[-1][1]] += 1
                if self.hu_judge():
                    return False
                self.cnt[gametable.receive_tiles[-1][1]] -= 1
                self.updateAI(gametable,opponent)
                choice=self.AI.think_chow()
                invalid_chow=False
                if choice>0:
                    if choice==1:
                        if (tile<7 and self.cnt[tile+1]>0 and self.cnt[tile+2]>0):
                            self.cnt_c[tile]+=1
                            self.cnt[tile+1] -= 1
                            self.cnt[tile+2] -= 1
                            self.chi +=1
                        else:
                            invalid_chow=True
                    elif choice==2:
                        if (tile>0 and tile<8 and self.cnt[tile-1]>0 and self.cnt[tile+1]>0):
                            self.cnt_c[tile-1]+=1
                            self.cnt[tile-1] -= 1
                            self.cnt[tile+1] -= 1
                            self.chi +=1
                        else:
                            invalid_chow=True
                    else:
                        if (tile>1 and self.cnt[tile-2]>0 and self.cnt[tile-1]>0):
                            self.cnt_c[tile-2]+=1
                            self.cnt[tile-2] -= 1
                            self.cnt[tile-1] -= 1
                            self.chi +=1
                        else:
                            invalid_chow=True

                    if self.is_show in ["normal","full"] and (invalid_chow==False):
                        print("\n",self.name,"chow player",gametable.receive_tiles[-1][0],"'s",get_tile_name(gametable.receive_tiles[-1][1]))
                    return True


        return False

        pass


    def hu_judge(self):
        tmp_ori = deepcopy(self.cnt)
        tmp = deepcopy(tmp_ori)
        for t in range(0,9):
            if (tmp[t] >= 2):
                tmp[t] -= 2
                ret = 0
                for j in range(0, 9):
                    while (j + 2 < 9 and tmp[j]>0 and tmp[j + 1]>0 and tmp[j + 2]>0):
                        tmp[j] -= 1
                        tmp[j + 1] -= 1
                        tmp[j + 2] -= 1
                        ret += 1
                    if (tmp[j] >= 3):
                        tmp[j] -= 3
                        ret += 1
                        
                tmp[t] += 2
                if (ret+self.peng+self.chi == 2):
                    return True
                else:
                    tmp=deepcopy(tmp_ori)
        return False
##



def get_tile_name(t):
    if t >= 0:
        if t <= 8:
            return str(t % 9 + 1)
        #+ Gametable.type[t // 9]
    return ''

def get_Tiles_names(tiles):
    names = ''
    for t in tiles:
        names += get_tile_name(t)+' '
    return names

def get_Cnt_names(cnt):
    names = ''
    for i in range(len(cnt)):
        e = cnt[i]
        while(e>0):
            names += get_tile_name(i)+' '
            e -= 1
    
    return names
    
    
    
    
class Gametable():
    type = ["W"]#the character tiles only

    def __init__(self,debug = False):
        self.Tiles=list(range(0,9))*4
        self.debug=debug


    def shuffle(self):
        self.draw_loc = 0
        self.receive_cnt = [0] * 9
        self.receive_tiles = []
        shuffle(self.Tiles)
    def draw(self):
        if self.draw_loc>=36:
            return "End"
        t=self.Tiles[self.draw_loc]
        self.draw_loc+=1

        return t

    def _receive(self,p_name,t):
        if p_name=="player1":
            int_p_name=1
        else:
            int_p_name=2
        #receive_tiles stores the history (steps) of the game
        #receive_cnt stores the dropped tiles 
        self.receive_tiles.append([int_p_name,t])
        self.receive_cnt[t] += 1
