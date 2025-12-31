from obj.static_object.static_object import *
from obj.physical_object.physicalobject import *;
from obj.physical_object.player import *;

class Team:
    def __init__(self,name="Myteam",color=color.red):
        self.name=name;
        self.playerDict={};
        self.color=color;
        self.defendGoalList=list();
        self.targetGoalList=list();
    
    def add_player(self,player,number):
        player.set_color(self.color)
        player.belongTeam(self)
        self.playerDict[number]=player
        
        
    def add_defendGoal(self,goal):
        self.defendGoalList.append(goal)
    
    def add_targetGoal(self,goal):
        self.targetGoalList.append(goal)
        
    

class FieldManager:
    def __init__(self,name="MyField",field_length=100,field_width=60):
        self.name=name;
        self.ground_thickness=10;
        self.ground=Ground(
            field_length=field_length,
            ground_thickness=self.ground_thickness,
            field_width=field_width
        );
        self.leftGoal=Goal(face_degree=0);
        self.leftGoal.set_goalLineCenter(vector(-field_length/2,self.ground_thickness/2,0));
        self.rightGoal=Goal(face_degree=180);
        self.rightGoal.set_goalLineCenter(vector(field_length/2,self.ground_thickness/2,0));
        self.centerLine=FieldLine(length=self.ground.field_width);
        self.centerLine.set_posCenter(self.ground.pos_center+vector(0,self.ground_thickness/2,0));
        print(self.name+": static object complete!");
        
        self.teamList=list();
        self.ballList=list();
        self.playerList=list();

    def ball_outside(self,ball):
        delta_pos=ball.pos_center-self.ground.pos_center
        width_vector=self.ground.axis
        length_vector=width_vector.cross(self.ground.showObj.up)
        return abs(dot(detl_pos,width_vector))>(self.ground.field_width/2) or abs(dot(detl_pos,length_vector))>(self.ground.field_length/2)
        
        
    def push_into_field(self,physbj=None,posX=None,posZ=None):
        physbj.ground=self.ground;
        Physis.position_when_onGround(physbj,posX,posZ);
        self.ground.onGround.append(physbj);
        if physbj.whatIsIt()=="ball":
            self.ballList.append(physbj);
        elif physbj.whatIsIt()=="player":
            self.playerList.append(physbj); 

    def add_team(self,team):
        self.teamList.append(team)
   
    def next_state(self):
        for player in self.playerList:
            player.think();
            player.next_state();
        for ball in self.ballList:            
            if (self.leftGoal.ball_touch_goal(ball)) or (self.rightGoal.ball_touch_goal(ball)):
                Physis.position_when_onGround(ball,0,0)
                ball.velocity=vector(0,0,0)
            if self.ball_outside(ball):
                Physis.position_when_onGround(ball)
                ball.velocity=vector(0,0,0)
            else:
                ball.next_state()
        


    

    
        
