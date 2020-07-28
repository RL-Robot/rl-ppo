import numpy as np
from robotControl import RobotControl as rc
from time import sleep

class RobotEnv(object):
    def __init__(self):
        self.action_bound = [0.35, 0.63]
        self.d_Array = []
        self.stepCount = 0
        ##self.LF_state,self.RF_state,self.LB_state,self.RB_state = 90,90,90,90
    def step(self,action):
        if self.stepCount == 0:
            rc.start()
            sleep(2)
        done = False 
        r = 0
        action = np.clip(action, *self.action_bound)
        LF = abs(int(action[0]*180))  
        RF = abs(int(action[1]*180))
        LB = abs(int(action[2]*180))
        RB = abs(int(action[3]*180))  
        rc.MoveLeg(LF,RF,LB,RB)
        distance = rc.getDistance()
        d = float(distance)
        distance = float(distance)/100
        ##print(distance)
        self.LF_state,self.RF_state,self.LB_state,self.RB_state = LF,RF,LB,RB
        LFs,RFs,LBs,RBs = rc.getLegStatus()
        LFs = float(LFs)/180
        RFs = float(RFs)/180
        LBs = float(LBs)/180
        RBs = float(RBs)/180

        s = np.array([distance,LFs,RFs,LBs,RBs]) 
        
        ## reward calculation
        self.d_Array.append(d)
        if len(self.d_Array) >= 3:
            for i in self.d_Array[-2:len(self.d_Array)-5:-1]:
                    if i < self.d_Array[-1]:
                        if self.d_Array[-1]+1 != 0:
                            r -= (i/self.d_Array[-1])
                    elif i > self.d_Array[-1]:
                        if self.d_Array[-1] != 0:
                            r += i/self.d_Array[-1]
                    else:
                        pass
        ## check if done
        ##print(distance)
        if distance <= 0.15 and distance > 0.1:
            done = True
            r = 20 + 50- self.stepCount
            self.d_Array.clear()            
        elif self.stepCount >= 30:
           done = True
           self.stepCount = 0
           self.d_Array.clear() 
        elif self.d_Array[-1] < 0.1 and self.d_Array[-2] < 0.1:
            r -= 100
            done = True
            self.d_Array.clear()
        self.stepCount += 1
        
        return s,r,done
    def reset(self):
        rc.resetLeg()
        sleep(2)
        rc.reset()  
        sleep(2)
        distance = int(rc.getDistance())
        LF,RF,LB,RB = rc.getLegStatus()
        distance = float(distance)/100
        LF = float(LF)/180
        RF = float(RF)/180
        LB = float(LB)/180
        RB = float(RB)/180
        s = np.array([distance,LF,RF,LB,RB])
        self.stepCount = 0
        return s
    def render(self):
        pass
    def random_action(self):
        return np.random.rand(4)
        

if __name__ == "__main__":
    env = RobotEnv()
    sleep(2)
    while True:
        env.reset()
        for i in range(1):
            env.step(env.random_action())
            sleep(0.2)
            