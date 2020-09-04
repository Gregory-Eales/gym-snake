import gym
from gym import error, spaces, utils
from gym.utils import seeding
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
from pygame.locals import *
import numpy as np
from copy import copy

class SnakeEnv(gym.Env):
  metadata = {'render.modes': ['human']}

  def __init__(self, size=16):

      self.size = size
      self.window_size = 800
      self.scale = self.window_size/self.size
      self.reset()

      self.human_render = False

  def step(self, action):
    
      state = self.take_action(action)
      reward = self.get_reward()
      done = self.is_terminal

      return state, reward, done, {}

  def reset(self):

      self.state = np.zeros([self.size, self.size])
      self.player = [[self.size//2, self.size//2]]
      self.spawn_apple()
      self.is_terminal = False
      self.player_direction = 1
      self.points = 0

  def render(self, mode='human'):
      
      r = None

      if mode == 'human':

        if not self.human_render:
          pygame.init()


          infoObject = pygame.display.Info()
          #pygame.display.set_mode((infoObject.current_w, infoObject.current_h))
          self.window_size = int(infoObject.current_h*3/4) + int(infoObject.current_h*3/4)%self.size
          self.scale = self.window_size/self.size
          self.screen = pygame.display.set_mode([
            self.window_size,
            self.window_size])

          self.screen.fill((0, 0, 0))


        self.human_render = True

        pygame.init()
        self.screen = pygame.display.set_mode([
          self.window_size,
          self.window_size])

        self.screen.fill((0, 0, 0))
        
        for event in pygame.event.get():
          if event.type == pygame.QUIT:
              self.is_terminal = True


          if event.type == KEYDOWN:
            if event.key == K_w:
              r = 0

            if event.key == K_a:
              r = 1

            if event.key == K_s:
              r = 2

            if event.key == K_d:
              r = 3 

        self.screen.fill((0, 0, 0))
        self.draw_player()
        self.draw_apple()


        pygame.display.flip()

      return r

  def close(self):
      pass

  def draw_player(self):

    for coord in self.player:
      pygame.draw.rect(self.screen, (255, 255, 255), [coord[0]*self.scale, coord[1]*self.scale, self.scale, self.scale])

  def draw_apple(self):
    pygame.draw.rect(self.screen, (255, 255, 255), [self.apple[0]*self.scale, self.apple[1]*self.scale, self.scale, self.scale])

  def spawn_apple(self):

    self.apple = np.random.randint(0, self.size, [2]).tolist()

  def update_player(self):

    len_p = len(self.player)

    last_pos = copy(self.player[0])

    if len_p > 1:

      for i in reversed(range(len_p)):

        if i == 0:
          pass

        else:

          if len_p-1 == i:
            last_pos = copy(self.player[i])

          self.player[i] = copy(self.player[i-1])

    if self.player_direction == 0:
      
      if self.player[0][1] >= 1:
        self.player[0][1] -= 1

    if self.player_direction == 1:

      if self.player[0][0] >= 1:
        self.player[0][0] -= 1

    if self.player_direction == 2:

      if self.player[0][1] < self.size - 1:
        self.player[0][1] += 1

    if self.player_direction == 3:

      if self.player[0][0] < self.size - 1:
        self.player[0][0] += 1


    if self.player[0] in self.player[1:-1]:
      self.is_terminal = True

    return last_pos
    
  def is_colliding(self):

    if self.player[0][0] == self.apple[0] and self.player[0][1] == self.apple[1]:
      return True

    else:
      return False

  def take_action(self, action):

    if action != None:
      self.player_direction = action

    last_pos = self.update_player()

    if self.is_colliding():
      self.spawn_apple()
      self.points += 1
      self.player.append(last_pos)

    return self.to_array()

  def get_reward(self):

    # distance between apple and head
    # 1 for each apple
    # -10 for hitting a wall
    # 
    return self.points

  def to_array(self):

    self.state = np.zeros([self.size, self.size])

    self.state[self.apple[0]][self.apple[1]] = 0.33

    for link in self.player:

      if link == self.player[0]:
        self.state[link[0]][link[1]] = 1

      else:
        self.state[link[0]][link[1]] = 0.66

    return self.state

def main():
    import time

    t = time.time()
    env = SnakeEnv()

    for i in range(1000):
      action = env.render(mode='human')
      state, reward, done, info = env.step(action)

      if done: break

      time.sleep(0.1)
      #print(env.player)

    #sprint(state)
    print("Took {} seconds".format(round(time.time()-t, 4)))

if __name__ == "__main__":
  
  main()