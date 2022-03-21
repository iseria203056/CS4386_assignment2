package com;
import java.util.ArrayList;
public class AIPlayer {
	String name="AIPlayer";
	ArrayList gametable_receive_tiles;
	ArrayList gametable_receive_cnt;
	ArrayList player_cnt;
	ArrayList player_cnt_p;
	ArrayList player_cnt_c;
	ArrayList oppo_cnt_p;
	ArrayList oppo_cnt_c;
	int player_last_draw;

	public void update_state(ArrayList gametable_receive_tiles1, ArrayList gametable_receive_cnt1, ArrayList player_cnt1, ArrayList player_cnt_p1, ArrayList player_cnt_c1,ArrayList oppo_cnt_p1,ArrayList oppo_cnt_c1){
		gametable_receive_tiles=gametable_receive_tiles1;
		gametable_receive_cnt=gametable_receive_cnt1;
		player_cnt=player_cnt1;
		player_cnt_p=player_cnt_p1;
		player_cnt_c=player_cnt_c1;
		oppo_cnt_p=oppo_cnt_p1;
		oppo_cnt_c=oppo_cnt_c1;
		
	}
	public boolean think_pong(){
		return true;
	}
	public int think_chow(){
		return 0;
	}
	

    public int think(){

		int choice=0;
	    for (int i=0;i<9;i++){
	    	//System.out.println(player_cnt.get(i));
	    	if ((long)player_cnt.get(i)>0){
	    		choice= i;
	    		return choice;
	    	}
	    }
	    return choice;
    }
}