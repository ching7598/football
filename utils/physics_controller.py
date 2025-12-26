from vpython import *
import math



class Physis:
    g = vector(0, -9.8, 0)
    min_acceleration=0.1
    min_velocity=0.1
    
    fps = 60        # 每秒更新 60 次
    dt = 1 / fps    # 每次迴圈代表的模擬時間（秒） 
    
    def __init__(self):
        pass;
        
    @staticmethod
    def f_facing_axis(degree):
        angle_rad=math.radians(degree)
        return vector(math.cos(angle_rad), 0, math.sin(angle_rad))
        
    @staticmethod
    def update_physis(obj):
        obj.acceleration=obj.force/obj.mass;
        obj.force=vector(0,0,0); ##造成加速度後，這個外力就該清掉
        if obj.acceleration.mag<=Physis.min_acceleration: ##避免原地顫動
           obj.acceleration=vector(0,0,0);
        obj.velocity+=obj.acceleration*Physis.dt;
        if obj.velocity.mag<=Physis.min_velocity:  ##避免原地顫動
           obj.velocity=vector(0,0,0);
        obj.set_posCenter(obj.pos_center+obj.velocity*Physis.dt);
        
    @staticmethod
    def position_when_onGround(obj,posX=None,posZ=None):
        ground_thickness=obj.ground.ground_thickness;
        if posX is None:
            posX=obj.pos_center.x
        if posZ is None:
            posZ=obj.pos_center.z
        if obj.whatIsIt()== "ball":
            obj.set_posCenter(vector(posX,(ground_thickness/2)+obj.radius,posZ))
        elif obj.whatIsIt()=="player" :
            obj.set_posCenter(vector(posX,(ground_thickness/2)+(obj.body.height/2),posZ))
        else:
            raise TypeError("未知物件型別")
   
    @staticmethod
    def touch_ground(physical_obj):
        obj_center_tall=0;
        ground=physical_obj.ground;
        if physical_obj.whatIsIt()== "ball":
            obj_center_tall=physical_obj.radius;
        if physical_obj.whatIsIt()=="player":
            obj_center_tall=physical_obj.body.height/2;
        touchGround=((physical_obj.pos_center.y-ground.pos_center.y)<=(obj_center_tall+(ground.ground_thickness/2))); 
        return touchGround;

    @staticmethod
    def interaction_of_ground(physical_obj):
        if Physis.touch_ground(physical_obj):
           Physis.friction_of_ground(physical_obj);
           if physical_obj.velocity.y<0:
               Physis.bounce_from_ground(physical_obj);
           Physis.position_when_onGround(physical_obj);
  
            
    
    @staticmethod
    def bounce_from_ground(physical_obj):
        vy=physical_obj.velocity.y*physical_obj.e_ground*(-1);
        physical_obj.velocity.y=vy;   

        
    
    @staticmethod
    def friction_of_ground(physical_obj):
        if Physis.touch_ground(physical_obj):
            u,mass=physical_obj.u_ground,physical_obj.mass;
            v=vector(physical_obj.velocity.x,0,physical_obj.velocity.z);
            f_friction=v.hat*(mass*Physis.g.mag*u)*(-1)
            physical_obj.add_force(f_friction);
            return f_friction;
        else:
            return vector(0,0,0)
    
    @staticmethod
    def ball_triangle_plane_distance(p1, p2, p3, ball, eps=1e-6):
        ballObj = ball.showObj
        # === Step 1: 平面法向量 ===
        normal = cross(p2 - p1, p3 - p1)
        n_mag = mag(normal)
        if n_mag < eps:
            raise ValueError("three points colinear, can't define triangle")

        n_hat = normal / n_mag  # 單位法向量

        # === Step 2: 有號球心到平面距離 ===
        signed_center_dist = dot(n_hat, ballObj.pos - p1)
        abs_center_dist = abs(signed_center_dist)

        # === Step 3: 球面到平面距離（有號） ===
        signed_surface_dist = signed_center_dist - ballObj.radius

        # === Step 4: 若球心距離已大於半徑，才有必要檢查三角形內 ===
        if abs_center_dist <= ballObj.radius + eps:
            # 投影點
            projection = ballObj.pos - signed_center_dist * n_hat

            # Barycentric 判斷是否在三角形內
            v0 = p3 - p1
            v1 = p2 - p1
            v2 = projection - p1

            dot00 = dot(v0, v0)
            dot01 = dot(v0, v1)
            dot02 = dot(v0, v2)
            dot11 = dot(v1, v1)
            dot12 = dot(v1, v2)

            denom = dot00 * dot11 - dot01 * dot01
            if abs(denom) > eps:
                u = (dot11 * dot02 - dot01 * dot12) / denom
                v = (dot00 * dot12 - dot01 * dot02) / denom

                if (u >= -eps) and (v >= -eps) and (u + v <= 1 + eps):
                    # 球確實觸碰到「三角形平面」
                    return 0.0

        # === Step 5: 未觸碰，回傳球面到平面距離（含正負號） ===
        return signed_surface_dist
        
    
    
            
    @staticmethod
    def gravity(physical_obj):
        physical_obj.add_force((Physis.g)*physical_obj.mass);
    