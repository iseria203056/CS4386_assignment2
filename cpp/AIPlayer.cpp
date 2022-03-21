#include <stdio.h>
#include <iostream>


#include <stdlib.h>
#include <string.h>
using namespace std;
class AIPlayer{
public:
    AIPlayer():name("AIPlayer"){
    	gametable_receive_tiles= new int*[22];
    	for (int i=0;i<22;i++){
    		gametable_receive_tiles[i]=new int[2];
    	}
    	gametable_receive_cnt=new int[9];
    	player_cnt=new int[9];
    	player_cnt_p=new int[9];
    	player_cnt_c=new int[9];
    	oppo_cnt_p=new int[9];
    	oppo_cnt_c=new int[9];
    	

    }
	void update_state(int c1[22][2],int c2[9],int c3[9], int c4[9], int c5[9],int c6[9],int c7[9]){

		for (int i=0;i<22;i++){
			for (int j=0;j<2;j++){
				gametable_receive_tiles[i][j]=c1[i][j];
			}
		}
		for (int i=0;i<9;i++){
			gametable_receive_cnt[i]=c2[i];
			player_cnt[i]=c3[i];
			player_cnt_p[i]=c4[i];
			player_cnt_c[i]=c5[i];
			oppo_cnt_p[i]=c6[i];
			oppo_cnt_c[i]=c7[i];
		
		}

		
	}

    bool think_pong(){
    	return true;
    }
    int think_chow(){
    	return 0;
    }

	int think(){
		static int choice=0;
	    for (int i=0;i<9;i++){
	    	//cout<<i<<","<<*(player_cnt+i)<<endl;

            	if (player_cnt[i]>0 ){
					choice=i;

					return choice;
                }

            
        }
        return choice;
	}

private:
	string name;

	int** gametable_receive_tiles;
	int* gametable_receive_cnt;
    int* player_cnt;
    int* player_cnt_p;
    int* player_cnt_c;
    int* oppo_cnt_p;
    int* oppo_cnt_c;
    
};



extern "C" {

AIPlayer py;

void update_state(int c1[22][2],int c2[9],int c3[9], int c4[9], int c5[9],int c6[9],int c7[9]){
    return py.update_state(c1,c2,c3,c4,c5,c6,c7);
}

int think_chow(){

	return py.think_chow();
}

bool think_pong(){
    return py.think_pong();
}

int think(){

	return py.think();

}
}
