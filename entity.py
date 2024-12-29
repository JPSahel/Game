import pygame
import random
class Entity:
    def __init__(self,hp,state,atk):
        self.hp = hp
        self.state = "Alive"
        self.atk = atk


    def checkState(self):
        if self.hp <= 0:
            self.state = "Dead"
    def attack(self,target):
        target.hp -= self.atk

    def heal(self):
        self.hp += 10

    def power(self,target):
        self.hp -= 20
        target.hp -= self.atk * 3
