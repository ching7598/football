from vpython import *
from obj.physical_object.physicalobject import *;
import math;
import random;

class MemoryObj:
    def __init__(self,realObj,pos_center=None,velocity=vector(0,0,0),life_sec_new=3):
        self.velocity=velocity
        self.pos_center=pos_center
        self.realObj=realObj
        self.life_time_new=0
        self.life_time=0
        self.set_life_time_new(life_sec_new)        
        self.memory_update()

        
    def memory_fading(self):
        if self.life_time==0:
            return False
        else:
            self.life_time -=1
            return True
        
    def memory_update(self):
        if self.realObj is not None:# ex: position, not a real object
            if hasattr(self.realObj,"velocity"):
                self.velocity=self.realObj.velocity
            self.pos_center=self.realObj.pos_center
        self.life_time=self.life_time_new
        
    def set_life_time_new(self,sec):
        self.life_time_new=sec*Physis.fps



class MemoryPerson(MemoryObj):
    def __init__(self,teammate=False):
        super().__init__(**kwargs)
        self.temmate=teammate;
        

class Player(PhysicalObject):
    def __init__(self,obj_color=color.white,player_name="",**kwargs):
        super().__init__(**kwargs)
        self.showObj.visible = False
        del self.showObj
        
        self.typeName="player";
        self.name=player_name;
        self.mass=70
        self.waist=0.5 #計算球員碰撞用
        self.u_ground=10
        self.e_ground=0.1
        
        # --- 主體元件 ---
        self._rel = {
            "body":vector(0,0,0),
            "head": vector(0,1.5,0),
            "left_eye": vector(0.4,1.5,-0.2),
            "right_eye": vector(0.4,1.5,0.2),
            "leg_range": vector(0,-1,0),
            "back_text": vector(-0.18,0,-0.2)
        }
        
        
        self.showObj= box(pos=self.pos_center,length=0.5, height=2, width=1, color=self.obj_color)
        self.body=self.showObj;
        self.head = box(length=0.8, height=0.8, width=0.8, color=color.orange)
        # --- 眼睛 ---
        self.left_eye = sphere(radius=0.1, color=color.white)
        self.right_eye = sphere(radius=0.1, color=color.white)
        # --- 腿部活動範圍 (半透明球) ---
        self.leg_range = sphere(radius=1, color=color.green, opacity=0.2)
        # --- 中心位置 ---
        self.back_text=text(text="?",height=1,color=color.white,axis=vector(0,0,1))
        self.axis = self.body.axis  # 當前朝向
        self.update_body_parts();
        
        self.partList= {
            "body":self.body,
            "head": self.head,
            "left_eye": self.left_eye,
            "right_eye":self.right_eye ,
            "leg_range": self.leg_range,
            "back_text":self.back_text
        }
        
        self.abilityList={#注意這些數值是瞬間出力
            "runBurst":20000,
            "retreatBurst":10000,
            "strafeBurst":15000,
            "kickBurst":500
        }
        
        self.viewAngle=140;
        self.memoryDict={"start_position":MemoryObj(realObj=None,pos_center=self.pos_center,velocity=vector(0,0,0),life_sec_new=3600)}
        
    # ------------------------------------------------------------       

    def set_posCenter(self,point=None):
        if point is not None:
            self.pos_center=point;
        self.update_body_parts();
        
    def update_back_text(self,str_text):
        str_text=str(str_text)
        old_text=self.back_text
        new_text=text(text=str_text)
        new_text.pos,new_text.axis,new_text.height=old_text.pos,old_text.axis,old_text.height
        self._rel["back_text"]=vector(-0.18,0,-0.2*len(str_text))
        self.back_text=new_text
        self.partList["back_text"]=new_text
        old_text.visible=False
        del old_text
        


 
    def update_body_parts(self):
        self.body.pos=self.pos_center+self._rel["body"]
        self.head.pos=self.pos_center + self._rel["head"];
        self.left_eye.pos=self.pos_center+self._rel["left_eye"]
        self.right_eye.pos=self.pos_center+self._rel["right_eye"]
        self.leg_range.pos=self.pos_center+ self._rel["leg_range"]
        self.back_text.pos=self.pos_center+ self._rel["back_text"]
        
        
    def is_in_view(self,obj):
        delta_pos=obj.pos_center-self.pos_center
        delta_pos.y=0;
        dot_value=dot(delta_pos.norm(),self.axis.norm())
        return dot_value>math.cos(self.viewAngle/2)

    # ------------------------------------------------------------
    def run_forward(self, jump_force=None,degree_launch_angle=45):
        """整個玩家同步移動"""
        if degree_launch_angle>90:
            #print("use backpedal function when the playerer jump back")
            return;
        
        if not Physis.touch_ground(self):
            return;
        
        if jump_force is None:
            jump_force=self.abilityList["runBurst"]
        else:
            jump_force=min(jump_force,self.abilityList["runBurst"])
        
        angle=math.radians(degree_launch_angle)
        forward_horizontal=vector(self.axis.x,0,self.axis.z)
        jump_dir = forward_horizontal * math.cos(angle) + vector(0,1,0) * math.sin(angle)

        self.add_force(jump_dir.norm()*jump_force)

    # ------------------------------------------------------------
    
    def backpedal(self, jump_force=None,degree_launch_angle=45):
        """整個玩家同步移動"""
        if degree_launch_angle>90:
            #print("use run_forward function when the playerer jump forward")
            return;
        
        if not Physis.touch_ground(self):
            return;
        
        if jump_force is None:
            jump_force=self.abilityList["retreatBurst"]
        else:
            jump_force=min(jump_force,self.abilityList["retreatBurst"])
        
        angle=math.radians(degree_launch_angle)
        forward_horizontal=vector(self.axis.x,0,self.axis.z)
        jump_dir = forward_horizontal * math.cos(angle)*(-1) + vector(0,1,0) * math.sin(angle)

        self.add_force(jump_dir.norm()*jump_force)
        
    def right_shuffle(self, jump_force=None,degree_launch_angle=45):
        side_direction=cross(self.axis,self._rel["head"]);
        self.__shuffle(jump_force,degree_launch_angle,side_direction);
    
    def left_shuffle(self, jump_force=None,degree_launch_angle=45):
        side_direction=cross(self.axis,self._rel["head"])*(-1);
        self.__shuffle(jump_force,degree_launch_angle,side_direction);
        
    def __shuffle(self, jump_force=None,degree_launch_angle=45,side_direction=None):       
        
        if degree_launch_angle>90:
            #print("degree_launch_angle must < 90")
            return;
        if not Physis.touch_ground(self):
            return;
        
        if jump_force is None:
            jump_force=self.abilityList["strafeBurst"]
        else:
            jump_force=min(jump_force,self.abilityList["strafeBurst"])
        
        angle=math.radians(degree_launch_angle)
        forward_horizontal=side_direction
        jump_dir = side_direction * math.cos(angle)*(-1) + vector(0,1,0) * math.sin(angle)

        self.add_force(jump_dir.norm()*jump_force)

    

    # ------------------------------------------------------------
    def turn_right(self,degree):
        if abs(degree)>180:
            #print("player"+self.player_name+" spin too much");
            return;

        angle=-math.radians(degree);
        rot_axis=vector(0,1,0);
        
        for partName in ["body","head","left_eye","right_eye","leg_range","back_text"]:
        # 旋轉相對位置
            rel_pos=self._rel[partName];
            part=self.partList[partName];
            rel_pos_rotated = rel_pos.rotate(angle=angle, axis=rot_axis)
            # 更新位置
            self._rel[partName]=rel_pos_rotated;
            # 旋轉自身方向
            part.axis = part.axis.rotate(angle=angle, axis=rot_axis)
        # 更新身體方向
        
        self.axis.rotate(angle=angle, axis=rot_axis)
        self.update_body_parts()
    
    def kick_ball(self,ball,kick_force=None):
        dis_ball_player=mag(ball.pos_center-self.leg_range.pos)
        max_dis=self.leg_range.radius+ball.radius
        adjustBurst=self.abilityList["kickBurst"]*(1-(dis_ball_player/max_dis))
  
        
        #out of range    
        if dis_ball_player>max_dis:
            return;
            #print(self.name,":Out of range kicking!")
  
        #default of kick_force is direct kick forward with maxium effort
        if kick_force is None:
            kick_force=self.axis.norm()*adjustBurst;  

        angle= math.acos(max(-1,min(1,dot(kick_force.norm(),self.axis.norm()))))
        if angle > 1.57:
            adjustBurst=min(adjustBurst,100)
        
        #Exceeds the maximum force limit.
        if mag(kick_force)>adjustBurst:
            kick_force=kick_force.norm()*adjustBurst
            #print(self.name,":Exceeds the maximum force limit!")
            
        ball.add_force(kick_force)
# ------------------------------------------------------------   
    def belongTeam(self,team):
        for i in range(len(team.targetGoalList)):
            goal=team.targetGoalList[i]
            self.memoryDict["target_goal_"+str(i)]=MemoryObj(goal,life_sec_new=3600)
        for i in range(len(team.defendGoalList)):
            goal=team.defendGoalList[i]
            self.memoryDict["defend_goal_"+str(i)]=MemoryObj(goal,life_sec_new=3600)
    
    def memory_update(self):#記憶按照所見更新，看不見的記憶淡忘或清除
        for key,mobj in list(self.memoryDict.items()): 
            if not mobj.memory_fading():
                self.memoryDict.pop(key)
            elif self.is_in_view(mobj):
                mobj.memory_update()
            else:
                mobj.pos_center+=(mobj.velocity*Physis.dt)
                
                
    def find_something(self,memory_name_in_dic,type_name,life_sec_new=None): #轉頭從視野中找物件，但記憶中還有就不找
        subject=self.memoryDict.get(memory_name_in_dic)
        if subject is not None:
            return subject
        else:
            for obj in self.ground.onGround:
                    if self.is_in_view(obj):
                        if obj.typeName==type_name:
                            subject=MemoryObj(obj,life_sec_new=life_sec_new)
                            self.memoryDict[memory_name_in_dic]=subject;
                            return subject
            self.turn_right(3)
            return None

    def chasing_object(self,mem_obj,goal_distance=0.5): 
        ball_possession=mag(mem_obj.pos_center-self.leg_range.pos)<goal_distance

        if ball_possession:
            return True
        else:
            rel_spinVector=cross(self.axis,mem_obj.pos_center-self.pos_center) 
            if rel_spinVector.y<0:            
                self.turn_right(3)
            elif rel_spinVector.y>0:
                self.turn_right(-3)
            #self.run_forward((mem_obj.pos_center-self.pos_center).mag*(self.abilityList.get("runBurst")/2))
            forward_speed=dot(self.velocity,self.axis)#因為self.axis.mag永遠是1，dot就是分速度大小
            self.run_forward(((mem_obj.pos_center-self.pos_center).mag/Physis.dt-forward_speed)*self.mass/Physis.dt)
        return False

    def think_wait_starting(self):
        self.chasing_object(self.memoryDict.get("start_position"),2)
    
    def think(self):#先寫一個只會一直找球並追著球跑，一旦追到球就踢出去的傢伙
        self.memory_update() 
        memBall=self.find_something("memBall","ball",life_sec_new=2)#找球
        #targetGoal=self.find_something("targetGoal","goal")
        
        
        if memBall is not None:
                if self.chasing_object(memBall,memBall.realObj.radius+self.leg_range.radius):
                    self.kick_ball(memBall.realObj)


        

            
        

        
        



        
            
  
                    
        
        
        
                    

        
    
            

