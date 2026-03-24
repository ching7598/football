from obj.physical_object.player import Player, MemoryObj
from utils.physics_controller import Physis
from vpython import *
import math

        

class Player_wiper(Player):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.memoryDict["threat_dis"]=MemoryObj(value=18,realObj=None,pos_center=self.pos_center,velocity=vector(0,0,0),life_sec_new=3600)
        self.memoryDict["defend_dis"]=MemoryObj(value=35,realObj=None,pos_center=self.pos_center,velocity=vector(0,0,0),life_sec_new=3600)
 
    def wipe_out(self,mem_ball,angle):
        if mag(mem_ball.pos_center-self.leg_range.pos)<(self.leg_range.radius+mem_ball.realObj.radius):
            wipe_force=(self.axis+vector(0,0.7,0)+vector(0,0,1)*math.tan(angle)).norm()*self.abilityList["kickBurst"]
            self.kick_ball( mem_ball.realObj,kick_force=wipe_force)
            return True
        return False
        
        
    
    def think(self):
        self.memory_update() 
        memBall=self.find_something("memBall","ball")#找球     
       
        
        mem_defend_goal=self.memoryDict["defend_goal_0"]
        if mem_defend_goal is None:#如果還沒被指定到隊，沒有目標球門，就不動
            return
        
        
        
        if memBall is not None:
            defend_dis=self.memoryDict["defend_dis"].value
            threat_dis=self.memoryDict["threat_dis"].value
            
            dis_ball_goal=(memBall.pos_center-mem_defend_goal.pos_center).mag           
            if dis_ball_goal>defend_dis:
                self.think_wait_starting()            
            elif dis_ball_goal>threat_dis:
                if self.chasing_object(memBall,self.leg_range.radius*0.6):
                    mem_target_goal=self.memoryDict["target_goal_0"]
                    goal_self_vector=mem_target_goal.pos_center-self.pos_center
                    angle=math.radians(math.acos(dot(self.axis,goal_self_vector.norm() )))
                    rel_spinVector=cross(self.axis,mem_target_goal.pos_center-self.pos_center)
                    sign=(rel_spinVector.y>0)-(rel_spinVector.y<0) #取正負號
                    if angle<15:
                        self.wipe_out(memBall,(-1)*sign*angle)
                    else:
                        self.turn_right((-1)*sign*angle)
            else:
                if self.chasing_object(memBall,memBall.realObj.radius+self.leg_range.radius):
                    goal_self_vector=mem_defend_goal.pos_center-self.pos_center
                    angle=math.radians(math.acos(dot(self.axis,goal_self_vector.norm() )))     
                    if angle>30:
                        self.wipe_out(mem_ball,0)
                    else:
                        rel_spinVector=cross(self.axis,mem_defend_goal.pos_center-self.pos_center)
                        sign=(rel_spinVector.y>0)-(rel_spinVector.y<0) #取正負號
                        self.wipe_out(memBall,sign*angle)

            
  
                    
        
        
        
                    

        
    
            

