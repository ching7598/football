from vpython import *
from obj.physical_object.physicalobject import *;
import math;
import random;

class MemoryObj:
    def __init__(self,realObj,pos_center=None,velocity=None):
        self.pos_center=pos_center
        self.velocity=velocity
        self.realObj=realObj
    def memory_update(self):
        self.velocity=self.realObj.velocity
        self.pos_center=self.realObj.pos_center


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
        self.mass=70;
        self.u_ground=10
        self.e_ground=0.1
        
        # --- 主體元件 ---
        self._rel = {
            "body":vector(0,0,0),
            "head": vector(0,1.5,0),
            "left_eye": vector(0.4,1.5,-0.2),
            "right_eye": vector(0.4,1.5,0.2),
            "leg_range": vector(0,-1,0)
        }
        
        
        self.showObj= box(pos=self.pos_center,length=0.5, height=2, width=1, color=self.obj_color)
        self.body=self.showObj;
        self.head = box(length=0.8, height=0.8, width=0.8, color=color.orange)
        # --- 眼睛 ---
        self.left_eye = sphere(radius=0.1, color=color.white)
        self.right_eye = sphere(radius=0.1, color=color.white)
        # --- 腿部活動範圍 (半透明球) ---
        self.leg_range = sphere(radius=1.2, color=color.green, opacity=0.2)
        # --- 中心位置 ---
        self.axis = self.body.axis  # 當前朝向
        self.update_body_parts();
        
        self.partList= {
            "body":self.body,
            "head": self.head,
            "left_eye": self.left_eye,
            "right_eye":self.right_eye ,
            "leg_range": self.leg_range
        }
        
        self.abilityList={#注意這些數值是瞬間出力
            "runBurst":20000,
            "retreatBurst":10000,
            "strafeBurst":15000,
            "kickBurst":500
        }
        
        self.viewAngle=140;
        self.memoryDict={}
        
    # ------------------------------------------------------------       

    def set_posCenter(self,point=None):
        if point is not None:
            self.pos_center=point;
        self.update_body_parts();


 
    def update_body_parts(self):
        self.body.pos=self.pos_center+self._rel["body"]
        self.head.pos=self.pos_center + self._rel["head"];
        self.left_eye.pos=self.pos_center+self._rel["left_eye"]
        self.right_eye.pos=self.pos_center+self._rel["right_eye"]
        self.leg_range.pos=self.pos_center+ self._rel["leg_range"]
        
    def is_in_view(self,obj):
        delta_pos=obj.pos_center-self.pos_center
        delta_pos.y=0;
        dot_value=dot(delta_pos.norm(),self.axis.norm())
        return dot_value>math.cos(self.viewAngle/2)

    # ------------------------------------------------------------
    def run_forward(self, jump_force=None,degree_launch_angle=45):
        """整個玩家同步移動"""
        if degree_launch_angle>90:
            print("use backpedal function when the playerer jump back")
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
            print("use run_forward function when the playerer jump forward")
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
            print("degree_launch_angle must < 90")
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
            print("player"+self.player_name+" spin too much");
            return;

        angle=-math.radians(degree);
        rot_axis=vector(0,1,0);
        
        for partName in ["body","head","left_eye","right_eye","leg_range"]:
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
        #default of kick_force is direct kick forward with maxium effort
        if kick_force is None:
            kick_force=self.axis.norm()*self.abilityList["kickBurst"];  
        
        #out of range    
        if mag(ball.pos_center-self.leg_range.pos)>(ball.radius+self.leg_range.radius):
            return;
            print(self.name,":Out of range kicking!")
        
        #Exceeds the maximum force limit.
        if mag(kick_force)>self.abilityList["kickBurst"]:
            kick_force=kick_force.norm()*self.abilityList["kickBurst"]
            print(self.name,":Exceeds the maximum force limit!")
            
        ball.add_force(kick_force)
# ------------------------------------------------------------   
    def belongTeam(self,team):
        self.memoryDict["myTeam"]=team;
        self.memoryDict["targetGoalList"]=team.targetGoalList
    
    def think(self):
        myTeam=self.memoryDict.get("myTeam");
        #targetGoal=self.memoryDict.get("targetGoal");
        
        #先確定場上有沒有球、球門
        memBall=self.memoryDict.get("memBall");
        
        if memBall is None :#印象中沒有球，先右轉看看能否看到
            self.turn_right(3);
            for obj in self.ground.onGround:
                if self.is_in_view(obj):
                    if obj.typeName=="ball":
                        memBall=MemoryObj(obj)
                        memBall.memory_update()
                        self.memoryDict["memBall"]=memBall;
            return;
            
        #先寫一個只會追著球跑，一旦追到球就踢出去的傢伙
        if self.is_in_view(memBall.realObj):
            memBall.memory_update();
        else:
            memBall.pos_center+=(memBall.velocity*Physis.dt)
        
        if mag(memBall.pos_center-self.pos_center)<0.5:
            self.kick_ball(memBall.realObj)
        else:
            rel_spinVector=cross(self.axis,memBall.pos_center-self.pos_center)
            if rel_spinVector.y<0:            
                self.turn_right(3);
            elif rel_spinVector.y>0:
                self.turn_right(-3);
            self.run_forward((memBall.pos_center-self.pos_center).mag*(self.abilityList.get("runBurst")/2))
            
        
        



        
            
  
                    
        
        
        
                    

        
    
            

