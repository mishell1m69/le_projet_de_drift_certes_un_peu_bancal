import constants as ct
import math

def line(x1,y1,x2,y2,c):
    xt = x2-x1
    yt = y2-y1
    mt = max(abs(xt),abs(yt))
    for i in range(int(mt)):
        ct.RENDER_BUFFER.set_at((x1+xt*i/mt,y1+ yt*i/mt), c)
        
def angle_to_vec(ang):
    return [math.cos(ang),math.sin(ang)]


def dist(x1,y1,x2,y2):
    return math.sqrt((x2-x1)**2+(y2-y1)**2)

def getvect(x1,y1,x2,y2):
    return [x2-x1,y2-y1]

def normalize(vect,length=1):
    actual_length = dist(0,0,vect[0],vect[1])
    if actual_length ==0:
        return vect
    return [length*vect[0] / actual_length, length*vect[1] / actual_length]

def vec_to_angle(vec):
    n = normalize(vec)
    return math.atan2(n[1], n[0])

def perp_vec(vec):
    return [vec[1],-vec[0]]

def scalar(vec1,vec2):
    return vec1[0]*vec2[0] + vec1[1]*vec2[1]
        