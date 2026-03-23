from obj.static_object.static_object import *
from obj.physical_object.physicalobject import *;
from obj.physical_object.player import *;
from obj.physical_object.player_shooter import *;

class Team:
    def __init__(self,name="Myteam",color=color.white):
        self.name=name;
        self.playerDict={};
        self.color=color;
        self.defendGoalList=list();
        self.targetGoalList=list();
    
    def add_player(self,player,number):
        player.set_color(self.color)
        player.belongTeam(self)
        player.update_back_text(number)
        self.playerDict[number]=player
                
        
    def add_defendGoal(self,goal):
        self.defendGoalList.append(goal)
        goal.belongTeam=self
    
    def add_targetGoal(self,goal):
        self.targetGoalList.append(goal)
        
    

class FieldManager:
    def __init__(self,name="MyField",field_length=100,field_width=60):
        self.name=name;
        self.ground_thickness=0.01;
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
        #print(self.name+": static object complete!");
        
        self.scoreLabelDict={};
        self.teamList=list();
        self.ballList=list();
        self.playerList=list();
        
        self.all_going_home=True
        self.wait_starting_ball=True
        self.starting_team=None

    def ball_outside(self,ball):
        
        length_vector=self.ground.axis
        width_vector=length_vector.cross(self.ground.showObj.up)
        
        delta_pos=ball.pos_center-self.ground.pos_center
        pos_as_width=dot(delta_pos,width_vector)
        pos_as_length=dot(delta_pos,length_vector)
        outSide=False
        while abs(pos_as_width)>(self.ground.field_width/2):
            outSide=True
            sign=(pos_as_width>0)-(pos_as_width<0)
            ball.set_posCenter(ball.pos_center-width_vector*sign)
            delta_pos=ball.pos_center-self.ground.pos_center
            pos_as_width=dot(delta_pos,width_vector)
        while abs(pos_as_length)>(self.ground.field_length/2):
            outSide=True
            sign=(pos_as_length>0)-(pos_as_length<0)
            ball.set_posCenter(ball.pos_center-length_vector*sign)
            delta_pos=ball.pos_center-self.ground.pos_center
            pos_as_length=dot(delta_pos,length_vector)
        
        if outSide:
            Physis.position_when_onGround(ball)
        return outSide
        
        
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
        ground=self.ground
        score_label=label(text="0",height=30,color=team.color)
        self.scoreLabelDict[team]=score_label
        score_label.pos=ground.pos_center+vector(len(self.scoreLabelDict)*5,ground.ground_thickness+10,ground.field_width/2)
        self.starting_team=team
        
   
    def next_state(self):
        
        if self.all_going_home:
            all_home=True
            for team in self.teamList:
                target_pos=team.targetGoalList[0].pos_center
                defense_pos=team.defendGoalList[0].pos_center
                for player in team.playerDict.values():
                    player.think_wait_starting()
                    player.next_state()
                    all_home=all_home and (mag(player.pos_center-target_pos) > mag(player.pos_center-defense_pos))
            self.all_going_home=not all_home
            return
        elif self.wait_starting_ball:
            for team in self.teamList:
                if team==self.starting_team:
                    for player in team.playerDict.values():
                        player.think()
                        player.next_state()
                else:
                    for player in team.playerDict.values():
                        player.think_wait_starting()
                        player.next_state()
            ball_moved=False
            for ball in self.ballList:
                ball.next_state()
                ball_moved=ball_moved or (mag(ball.velocity)>1)
            self.wait_starting_ball=not ball_moved
            return
        
        n=len(self.playerList)
        for i in range(n):#更新球員狀態
            player=self.playerList[i]
            for j in range(i+1,n):#檢查跟其他球員碰撞
                other_player=self.playerList[j]
                Physis.player_collision(player,other_player)                
            player.think()
            player.next_state()
            
        for ball in self.ballList:#更新球狀態
            if self.ball_outside(ball): 
                ball.velocity=vector(0,0,0)
                #print("Ball outside!") 
            else:
                #看是否進球
                for team in self.teamList:
                    for goal in team.targetGoalList:
                        if goal.ball_touch_goal(ball):
                            Physis.position_when_onGround(ball,0,0)
                            ball.velocity=vector(0,0,0)
                            score_label=self.scoreLabelDict[team]
                            score_label.text=str(int(score_label.text)+1)
                            self.all_going_home=True
                            self.wait_starting_ball=True
                            self.starting_team=goal.belongTeam
            ball.next_state()
        


    

    
        
