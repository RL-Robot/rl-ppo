from env import RobotEnv
from rl import PPO
import numpy as np
import matplotlib.pyplot as plt
from time import sleep
env = RobotEnv()
ppo = PPO()
all_ep_r = []

EP_MAX = 50
EP_LEN = 30
GAMMA = 0.9
A_LR = 0.0001
C_LR = 0.0002
BATCH = 32
A_UPDATE_STEPS = 10
C_UPDATE_STEPS = 10
METHOD = [
    dict(name='kl_pen', kl_target=0.01, lam=0.5),   # KL penalty
    dict(name='clip', epsilon=0.2),                 # Clipped surrogate objective, find this is better
][0]        # choose the method for optimization
ppo.restore_model()
for ep in range(EP_MAX):
    if ep%3 == 0 and ep!=0:
        ppo.save_model()
    s = env.reset()
    print("please reset the robot position, it will move after 3 second!!!!!!!!!!!!!!")
    sleep(3)
    buffer_s, buffer_a, buffer_r = [], [], []
    ep_r = 0
    for t in range(EP_LEN):    # in one episode
        a = ppo.choose_action(s)
        s_, r, done = env.step(a)
        sleep(0.3)
        buffer_s.append(s)
        buffer_a.append(a)
        buffer_r.append(r)    
        s = s_
        ep_r += r
        
        # update ppo
        if (t+1) % BATCH == 0 or t == EP_LEN-1:
            
            v_s_ = ppo.get_v(s_)
            discounted_r = []
            for r in buffer_r[::-1]:
                v_s_ = r + GAMMA * v_s_
                discounted_r.append(v_s_)
            discounted_r.reverse()

            bs, ba, br = np.vstack(buffer_s), np.vstack(buffer_a), np.array(discounted_r)[:, np.newaxis]
            buffer_s, buffer_a, buffer_r = [], [], []
            ppo.update(bs, ba, br)            
        if done:
            break
    if ep == 0: all_ep_r.append(ep_r)
    else: all_ep_r.append(all_ep_r[-1]*0.9 + ep_r*0.1)
    print(
        'Ep: %i' % ep,
        "|Ep_r: %i" % ep_r,
        ("|Lam: %.4f" % METHOD['lam']) if METHOD['name'] == 'kl_pen' else '',
    )
plt.plot(np.arange(len(all_ep_r)), all_ep_r)
plt.xlabel('Episode');plt.ylabel('Moving averaged episode reward');plt.show()    