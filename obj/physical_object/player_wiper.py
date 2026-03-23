from obj.physical_object.player import Player, MemoryObj
from utils.physics_controller import Physis
from vpython import *
import math

        

class Player_wiper(Player):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.memoryDict["threat_dis"]=MemoryObj(35,life_time_new=3600*Physis.fps)
 
    def wipe_out(self,mem_ball,mem_defend_goal):
        if mag(mem_ball.pos_center-self.leg_range.pos)<(self.leg_range.radius+ball.radius):
            wipe_force=(mem_defend_goal.realObj.axis+vector(0,1,0))*self.abilityList["500"]
            self.kick_ball( mem_ball.realObj,kick_force=wipe_force)
            return True
        return False
        
    def back_to_defend_area(self,rush):
        
    
    def think(self):#只會一直找球並追著球跑，一旦追到球就轉身對準球門，然後全力射
        self.memory_update() 
        memBall=self.find_something("memBall","ball")#找球
        
       
        
        mem_defend_goal=self.memoryDict["defend_goal_0"]
        if mem_defend_goal is None:#如果還沒被指定到隊，沒有目標球門，就不動
            return
        
        
        
        if memBall is not None:
            threat_dis=self.memoryDict["threat_dis"]
            
            dis_ball_goal=mag(memBall.pos_center-mem_defend_goal.pos_center)            
            if dis_ball_goal>threat_dis:
                self.back_to_defend_area()
            
            elif diss_ball_goal short:
                if ball ahead:
                    chase
                    wipe
                else:
                    if ball_go_goal:
                        chase
                        back wipe
                    else:
                        chase
                        front wipe

            
  
                    
        
        
        
                    

        
    
            

