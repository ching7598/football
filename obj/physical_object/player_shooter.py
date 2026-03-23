from obj.physical_object.player import Player, MemoryObj
from utils.physics_controller import Physis
from vpython import *
import math

        

class Player_shooter(Player):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
 
    def shoot(self,mem_ball,mem_target_goal):
        if mag(mem_ball.pos_center-self.leg_range.pos)<0.6:
            rel_spinVector=cross(self.axis,mem_target_goal.pos_center-self.pos_center)
            if rel_spinVector.y<(-1):
                self.turn_right(3)
            elif rel_spinVector.y>1 :
                self.turn_right(-3)
            else:
                self.kick_ball(mem_ball.realObj)
                return True
        return False
    
    def think(self):#只會一直找球並追著球跑，一旦追到球就轉身對準球門，然後全力射
        self.memory_update() 
        memBall=self.find_something("memBall","ball",life_sec_new=2)#找球
        
        
        
        mem_target_goal=self.memoryDict["target_goal_0"]
        if mem_target_goal is None:#如果還沒被指定到隊，沒有目標球門，就不動
            return
        
        if memBall is not None:
            if not self.shoot(memBall,mem_target_goal):
                self.chasing_object(memBall,0)
                   

            
  
                    
        
        
        
                    

        
    
            

