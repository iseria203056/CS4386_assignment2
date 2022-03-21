#! python3
# coding = utf-8

import Game
import sys
import os

if True:
    name = "play_mahjong" 
    is_show = 'full'#display mode:mute，little（results only）， normal（key information），full（all information)
    #player1 plays first
    Player_names=["player1","player2"] 
    Rules={"Shoot":True, "Pong": True, "Chow":True}

    p1_language=sys.argv[1]
    p2_language=sys.argv[2]
    AI_languages=[p1_language,p2_language]

    
    if p1_language=="Human":
        AI_names = ['human','AIPlayer']
    elif p2_language == "Human":
        AI_names = ['AIPlayer','human']
    else:
        AI_names = ['AIPlayer','AIPlayer']

    if p1_language=="JAVA" or p2_language=="JAVA":
        import jpype
        jarpath = os.path.join(os.path.abspath('.'), 'java/AIPlayer.jar')
        jpype.startJVM(jpype.getDefaultJVMPath(), "-ea", "-Djava.class.path=%s" % jarpath)
        
        

    game = Game.Game( name ,
                      is_show = is_show ,
                      Player_names = Player_names ,
                      AI_names = AI_names ,
                      AI_languages=AI_languages,
                      debug = False ,
                      Rules = Rules )
    game.play(1)#play one round



