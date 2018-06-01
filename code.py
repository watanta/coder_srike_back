# -*- coding: utf-8 -*-
import sys
import math
import numpy as np

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.


class MyPod:
    def __init__(self):
        
        #自機の位置
        self.x = 0
        self.y = 0
        self.pre_x = 0
        self.pre_y = 0
        
        #chに対する角度
        self.angle = 0
        self.pre_angle =0
        self.angle_vel = 0
        
        #自機の速度
        self.vel_vector = (0,0)
        self.pre_vel_vector = (0,0)
        self.velocity = 0
        self.vertical_velocity_to_ch = 0
        self.horizonal_velocity_to_ch = 0
        
        #右水平に対しての速度ベクトルの角度
        self.angle_of_velvec_from_origin = 0
        
        #右水平に対して，自機からchを指すベクトルが何度か
        self.angle_of_ch_from_origin = 0
        
        self.angle_of_distination_from_origin = 0
        
        self.angle_of_ch_from_origin  = 0
        
        self.angle_of_facingdir_from_origin = 0
        
        #chの情報
        self.next_checkpoint_x = 0
        self.next_checkpoint_y = 0
        self.next_checkpoint_dist  = 0
        self.next_checkpoint_angle = 0
        self.vector_to_nextcheckpoint = (0,0)
        self.angle_of_velvec_from_nextcheckpoint = 0
        
        self.opponent_x = 0
        self.opponent_y = 0
        self.opponent_dist = 0
        
        self.offset_x = 0
        self.offset_y = 0
        
        self.boost_flag = True
        
        self.lap = 1
        self.checkpoint_positions =[]
        
        
        
        
        self.handle = 0
        self.thrust  = 0
        self.to_x = 0
        self.to_y = 0
        
    def cal_angle(self,v1,v2):
        #v2はv1に対して何度か
        x = v1
        y = v2
        
        dot_xy = np.dot(x,y)
        norm_x = np.linalg.norm(x)
        norm_y  =np.linalg.norm(y)
        cos = dot_xy / (norm_x * norm_y)
        rad = np.arccos(cos)
        
        if  np.cross(x,y) > 0:
            theta =  rad * 180 / np.pi
        else:
            theta = -rad * 180 / np.pi
       
        return theta
        
    def compute_params(self, x, y, next_checkpoint_x, next_checkpoint_y, next_checkpoint_dist, next_checkpoint_angle, opponent_x, opponent_y):
        #更新前の値を過去に
        self.pre_vel_vector = self.vel_vector
        self.pre_angle = self.angle
        self.pre_x = self.x
        self.pre_y = self.y
        
        #現在の値に更新
        self.x = x
        self.y = y
        self.angle = next_checkpoint_angle
        self.dist = next_checkpoint_dist
        self.opponent_x = opponent_x
        self.opponent_y = opponent_y
        self.next_checkpoint_x = next_checkpoint_x
        self.next_checkpoint_y = next_checkpoint_y
        self.next_checkpoint_dist = next_checkpoint_dist
        
        #現在の値からいろいろ計算
        self.compute_vel_vector()
        self.compute_angle_vel()
        self.compute_velocity()
        self.compute_vector_to_nextcheckpoint()
       
        self.compute_angle_of_ch_from_origin()
        self.compute_angle_of_velvec_from_origin()
        self.compute_angle_of_facingdir_from_origin()
        
        
        self.compute_angle_of_velvec_from_nextcheckpoint()
        self.compute_vertical_horizonal_vel_to_ch()
        self.compute_opponent_dist()
        self.compute_checkpoint_positions()
        self.compute_lap()
        
        #
        self.compute_handle()
        
        #出力計算
        self.compute_destination()
        self.compute_thrust()
        
        return
        
    def compute_vel_vector(self):
        self.vel_vector = (self.x - self.pre_x, self.y - self.pre_y)
        return
        
    def compute_angle_vel(self):
        self.angle_vel = self.angle - self.pre_angle
        return
        
    def compute_velocity(self):
        self.velocity =  math.sqrt(self.vel_vector[0]**2+self.vel_vector[1]**2)
        return
    
    def compute_vector_to_nextcheckpoint(self):
        self.vector_to_nextcheckpoint = (self.next_checkpoint_x - self.x, self.next_checkpoint_y - self.y)
        return
    
    def compute_angle_of_velvec_from_nextcheckpoint(self):
        
        x = np.array(self.vector_to_nextcheckpoint)
        y = np.array(self.vel_vector)
            
        self.angle_of_velvec_from_nextcheckpoint = self.cal_angle(x,y)
        
        return
    
    def compute_angle_of_velvec_from_origin(self):
        
        x = np.array((self.x +10, self.y))
        y = np.array(self.vel_vector)
        
        self.angle_of_velvec_from_origin = self.cal_angle(x, y)
        
        return
    
    def compute_angle_of_ch_from_origin(self):
        
        x = np.array((self.x +10, self.y))
        y = np.array((self.next_checkpoint_x, self.next_checkpoint_y))
        
        self.angle_of_ch_from_origin = self.cal_angle(x, y)
        
        return
        
    def compute_angle_of_facingdir_from_origin(self):
        self.angle_of_facingdir_from_origin = self.angle_of_ch_from_origin - self.angle
        return
    
    def compute_vertical_horizonal_vel_to_ch(self):
        
        self.vertical_velocity_to_ch = self.velocity * math.cos(math.radians(self.angle_of_velvec_from_nextcheckpoint))
        self.horizonal_velocity_to_ch = self.velocity * math.sin(math.radians(self.angle_of_velvec_from_nextcheckpoint))
        return
    
    def compute_opponent_dist(self):
        self.opponent_dist = math.sqrt((self.x - self.opponent_x)**2+(self.y - self.opponent_y)**2)
        return
    
    def compute_checkpoint_positions(self):
        checkpoint_position = (self.next_checkpoint_x, self.next_checkpoint_y)
        
        if checkpoint_position in self.checkpoint_positions:
            pass
        else:
            self.checkpoint_positions.append(checkpoint_position)
            
    def compute_lap(self):
        return       
    
    def compute_handle(self):
        
        self.handle = np.clip(self.angle, -18, 18)
        return
    
    def compute_destination(self):
        
        radius = 1000
        
        self.angle_of_distination_from_origin = self.angle_of_facingdir_from_origin + self.handle
        self.to_x = int(round(self.x + radius*math.cos(math.radians(self.angle_of_distination_from_origin))))
        self.to_y = int(round(self.y + radius*math.sin(math.radians(self.angle_of_distination_from_origin))))
        return
    
    def compute_thrust(self):
        
        if self.is_bad_direction() :
            self.thrust_off()
        elif self.is_near_checkpoint() and self.is_high_velocity() and self.is_velvec_angle_good() :
            self.thrust_low()
        #elif self.is_very_near_checkpoint or self.is_not_bad_direction() :
        #    self.thrust_low()
   
        else:
            self.thrust_full()
        return
    
    def thrust_off(self):
        self.thrust = 0
        print("Thrust_off", file=sys.stderr)
        return 
    
    def thrust_low(self):
        self.thrust = 25
        print("Thrust_low", file=sys.stderr)
        return 
        
    def thrust_half(self):
        self.thrust = 50
        print("Thrust_half", file=sys.stderr)
        return 
    
    def thrust_full(self):
        self.thrust = 100
        print("Thrust_full", file=sys.stderr)
        return

    def is_bad_direction(self):
        #ある角度内に次目標があるかどうか
        upper = 90
        lower = -90

        if (self.angle > upper) or (self.angle < lower):
            return True
        else:
            return False
    
    def is_not_bad_direction(self):
        #ある角度内に次目標があるかどうか
        upper = 90
        lower = -90

        if self.angle > upper or self.angle < lower:
            return True
        else:
            return False
            
    def is_good_direction(self):
        #ある角度内に次目標があるかどうか
        upper = 30
        lower = -30

        if self.angle > upper or self.angle < lower:
            return True
        else:
            return False
        
    def is_good_for_boost(self):
        #ブーストしていいかどうか
        if  (self.boost_flag == True) and self.next_checkpoint_dist > 5000 :
            return True
        else:
            return False
            
    def is_near_checkpoint(self):
        #閾値より目標までの距離が近いかどうか
        th = 1500
        if self.dist < th:
            return True
        else:
            return False
            
    def is_very_near_checkpoint(self):
        #閾値より目標までの距離がとても近いかどうか
        th = 1500
        if self.dist < th:
            return True
        else:
            return False
    
    def is_high_velocity(self):
        #閾値より速いかどうか
        th  = 200
        if self.velocity > th:
            return True
        else:
            return False
            
    def is_high_horizonal_velocity(self):
        th = 100
        if self.horizonal_velocity_to_ch > th:
            return True
        else:
            return False
            
    def is_attack_chance(self):
        th_dist = 500
        th_vel = 1000
        if self.opponent_dist < th_dist and self.velocity > th_vel :
            return True
        else:
            return False
        return
    
    def is_velvec_angle_good(self):
        if abs(self.angle_of_velvec_and_nextcheckpoint) < 50:
            return True
        else:
            return False
            
    def boost(self):
        self.boost_flag = False
        print(str(self.to_x) + " " + str(self.to_y) + " " + "BOOST")
        print("BOOST!!!!", file=sys.stderr)
        return
    
    def do_thrust(self):
        print(str(self.to_x) + " " + str(self.to_y) + " " + str(self.thrust))
        return

    def show_status(self):
        #全パラメータ出力
        print("x: ", self.x, file=sys.stderr)
        print("y: ", self.y, file=sys.stderr)
        print("to_x: ", self.to_x, file=sys.stderr)
        print("to_y: ", self.to_y, file=sys.stderr)
        print("handle :", self.handle, file=sys.stderr)
        print("thrust: ", self.thrust, file=sys.stderr)
        print("angle: ", self.angle, file=sys.stderr)
        print("dist: ", self.dist, file=sys.stderr)
        print("vel_vector: ", self.vel_vector, file=sys.stderr)
        print("velocity: ", self.velocity, file=sys.stderr)
        print("horizonal_vel_to_ch ",self.horizonal_velocity_to_ch, file=sys.stderr)
        print("vertical_vel_to_ch ",self.vertical_velocity_to_ch, file=sys.stderr)
        #print("offset_x :",self.offset_x, file=sys.stderr)
        #print("offset_y :",self.offset_y, file=sys.stderr)
        #print("angle_vel: ", self.angle_vel, file=sys.stderr)
        #print("vector_to_nextcheckpoint: ", self.vector_to_nextcheckpoint, file=sys.stderr)
        print("angle_of_velvec_from_nextcheckpoint: ", self.angle_of_velvec_from_nextcheckpoint, file=sys.stderr)
        #print("offset: ", self.offset, file=sys.stderr)
        #print("boost_flag: ", self.boost_flag, file=sys.stderr)
        #print("velvec_angle: ", self.is_velvec_angle_good(), file=sys.stderr)
        #print("near: ", self.is_near_checkpoint(), file=sys.stderr)
        #print("high_vel: ", self.is_high_velocity(), file=sys.stderr)
        #print("is_good_for_boost: ",self.is_good_for_boost(), file=sys.stderr)
        #print("is_high_horizonal_velocity :", self.is_high_horizonal_velocity(), file = sys.stderr)
        print("angle_of_velvec_from_origin :",self.angle_of_velvec_from_origin, file = sys.stderr)
        print("angel_of_distination_from_origin :", self.angle_of_distination_from_origin, file = sys.stderr)
        print("angle_of_ch_from_origin :", self.angle_of_ch_from_origin, file =sys.stderr)
        print("angle_of_facingdir_from_origin :", self.angle_of_facingdir_from_origin, file =sys.stderr)

        
mypod = MyPod()
     
    
# game loop
while True:
    
    
    # next_checkpoint_x: x position of the next check point
    # next_checkpoint_y: y position of the next check point
    # next_checkpoint_dist: distance to the next checkpoint
    # next_checkpoint_angle: angle between your pod orientation and the direction of the next checkpoint
    x, y, next_checkpoint_x, next_checkpoint_y, next_checkpoint_dist, next_checkpoint_angle = [int(i) for i in input().split()]
    opponent_x, opponent_y = [int(i) for i in input().split()]

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)

    mypod.compute_params(x, y, next_checkpoint_x, next_checkpoint_y, next_checkpoint_dist, next_checkpoint_angle, opponent_x, opponent_y )
    # You have to output the target position
    # followed by the power (0 <= thrust <= 100)
    # i.e.: "x y thrust"
    mypod.show_status()
    
    #if mypod.is_good_for_boost:
    #    mypod.boost()
    #else:
    mypod.do_thrust()
        
    
        
