from vpython import *
from utils.physics_controller import *

class trianglePlane:
    def __init__(self,vertexA=vector(0,5,0),vertexB=vector(14.14,5,-5),vertexC=vector(14.14,5,5)):
        self.set_vertex
                
    def set_vertex(self,vertexA=None,vertexB=None,vertexC=None):
        if vertexA is not None:
            self.vertexA=vertexA;
        if vertexB is not None:
            self.vertexB=vertexB;
        if vertexC is not None:
            self.vertexC=vertexC;
        self.pos_center=(self.vertexA+self.vertexB+self.vertexC)/3
    def ball_distance(self,ball):
        return Physis.ball_triangle_plane_distance(self.vertexA,self.vertexB,self.vertexC,ball)


class StaticObject:
    def __init__(self,pos_center=vector(0,0,0),obj_color=color.white,face_degree=0):
        self.pos_center=pos_center;
        self.obj_color=obj_color;
        self.axis=Physis.f_facing_axis(face_degree);
        self.showObj=box(pos=self.pos_center,size=vector(1,1,1),color=self.obj_color,axis=self.axis);
        self.typeName="staticObject";
        self.ground=None;
    def set_posCenter(self,point=None):
        if point is not None:
            self.pos_center=point;
        self.showObj.pos=self.pos_center;
    def set_color(self,input_color=None):
        if input_color is not None:
            self.obj_color=input_color;
        self.showObj.color=self.obj_color;
    def whatIsIt(self):
        return self.typeName;

        

   

class Ground(StaticObject):
    def __init__(self,field_length=100,ground_thickness=10,field_width=60,**kwargs):
        super().__init__(**kwargs)
        self.field_length=field_length;
        self.ground_thickness=ground_thickness;
        self.field_width=field_width;
        self.set_size();
        self.obj_color=color.green;
        self.set_color();
        self.onGround=list();
        self.typeName="ground";
    def set_size(self,field_length=None,ground_thickness=None,field_width=None):
        if field_length is not None:
            self.field_length=field_length;
        if ground_thickness is not None:
            self.ground_thickness=ground_thickness;
        if field_width is not None:
            self.field_width=field_width;  
        self.showObj.size=vector(self.field_length,self.ground_thickness,self.field_width);    
         
 

class Goal(StaticObject):
    def __init__(self,goal_depth=2,goal_height=2.4,goal_width=7.3,**kwargs):
        super().__init__(**kwargs)
        self.goal_depth,self.goal_height,self.goal_width=goal_depth,goal_height,goal_width;
        self.front_planes=[trianglePlane(),trianglePlane()];
        self.set_front_planes();
        self.set_size();
        self.showObj.opacity=0.3;
        self.typeName="goal";

    
    def set_front_planes(self):
        face_vector=self.axis.norm();
        up_vector=self.showObj.up.norm();
        side_vector=cross(face_vector,up_vector)
        vertex1=self.pos_center+face_vector*(self.goal_depth)/2+up_vector*(self.goal_height)/2+side_vector*(self.goal_width)/2
        vertex2=vertex1-up_vector*self.goal_height;
        vertex3=vertex1-side_vector*self.goal_width;
        self.front_planes[0].set_vertex(vertex1,vertex2,vertex3);
        vertex1=vertex3-up_vector*self.goal_height;
        self.front_planes[1].set_vertex(vertex1,vertex3,vertex2);
        
    
    def set_size(self,goal_depth=None,goal_height=None,goal_width=None):
        if goal_depth is not None:
            self.goal_depth=goal_depth;
        if goal_height is not None:
            self.goal_height=goal_height;
        if goal_width is not None:
            self.goal_width=goal_width;    
        self.showObj.size=vector(self.goal_depth,self.goal_height,self.goal_width);
        self.set_front_planes()
        
    def set_goalLineCenter(self,point=vector(0,0,0)):
        self.pos_center=point-((self.goal_depth/2)*self.axis.norm())+vector(0,self.goal_height/2,0);
        self.set_posCenter();
        self.set_front_planes();
    
        
    def ball_inside(self,ball):
        if (ball.pos_center-self.pos_center).mag > (self.goal_width/2):
            return(False)
        else:
            touch_front_plane=False;
            for plane in self.front_planes:
                touch_front_plane=touch_front_plane or (plane.ball_distance(ball)==0)
            return touch_front_plane
        
    
    
class FieldLine(StaticObject):
    def __init__(self,width=0.2,length=60,**kwargs):
        super().__init__(**kwargs)
        self.thickness=0.01
        self.width,self.length=width,length;
        self.set_size();
        self.typeName="fieldLine";
    def set_size(self,width=None,length=None):
        if width is not None:
            self.width=width;
        if length is not None:
            self.length=length;            
        self.showObj.size=vector(self.width,self.thickness,self.length)

