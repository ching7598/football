from obj.physical_object.player import Player, MemoryObj
from utils.physics_controller import Physis
from vpython import *
import math

        

class Player_shooter(Player):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
 
    
    def think(self):
        self.memory_update() #記憶按照所見更新，看不見的記憶淡忘或清除
        memBall=self.find_something("memBall","ball")#找球
    
        mem_target_goal=self.memoryDict["target_goal_0"]
        if mem_target_goal is None:#如果還沒被指定到隊，沒有目標球門，就不動
            return
        
        #只會一直找球並追著球跑，一旦追到球就主身對準球門，然後全力射
        if memBall is None:
            self.turn_right(3)
            return
        
        if mag(memBall.pos_center-self.leg_range.pos)<0.6:
            rel_spinVector=cross(self.axis,mem_target_goal.pos_center-self.pos_center)
            if rel_spinVector.y<(-0.2):
                self.turn_right(3)
            elif rel_spinVector.y> 0.2:
                self.turn_right(-3)
            else:
                self.kick_ball(memBall.realObj)
            
        else:        
            rel_spinVector=cross(self.axis,memBall.pos_center-self.pos_center)
            if rel_spinVector.y<0:            
                self.turn_right(3)
            elif rel_spinVector.y>0:
                self.turn_right(-3)
            if self.is_in_view(memBall.realObj):
                self.run_forward((memBall.pos_center-self.pos_center).mag*(self.abilityList.get("runBurst")/2))
            return

            
        

        
        



        
            
  
                    
        
        
        
                    

        
    
            

