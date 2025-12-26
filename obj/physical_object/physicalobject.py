from obj.static_object.static_object import *;
from utils.physics_controller import *;

class PhysicalObject(StaticObject):
    def __init__(
        self,
        velocity=vector(0,0,0),acceleration=vector(0,0,0),
        force=vector(0,0,0),u_ground=0.1,
        mass=1,
        e_ground=1, #coefficient of restitution between self and ground,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.velocity=velocity;
        self.acceleration=acceleration;
        self.force=force;
        self.u_ground=u_ground;
        self.e_ground=e_ground;
        self.mass=mass;
        self.typeName="physicalObject";
    def next_state(self):
        Physis.gravity(self);
        Physis.interaction_of_ground(self);
        Physis.update_physis(self);
    def add_force(self,addedforce=vector(0,0,0)):
        self.force+=addedforce;


        

class Ball(PhysicalObject):
    def __init__(self,radius=0.5,u_ground=0.5,e_ground=0.5,mass=0.43,**kwargs):
       super().__init__(**kwargs)
       self.radius=radius; 
       self.showObj.visible = False
       self.typeName="ball";
       self.e_ground=e_ground;
       del self.showObj
        # 建立球體
       self.showObj = sphere(pos=self.pos_center, radius=self.radius, color=self.obj_color)

   
  