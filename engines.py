__author__ = 'Andres'

import math
import time


def sinx(actor, stats):
    t = time.clock() - actor.sign.spawn_time
    actor.centerx -= stats.speed*math.cos(t*math.pi)


def siny(actor, stats):
    t = time.clock() - actor.sign.spawn_time
    actor.centery -= stats.speed*math.cos(t*math.pi)


def cosx(actor, stats):
    t = time.clock() - actor.sign.spawn_time
    actor.centerx += stats.speed*math.sin(t*math.pi)


def cosxx(actor, stats):
    t = time.clock() - actor.sign.spawn_time
    actor.centerx += stats.speed*math.sin(t*math.pi) - t


def cosy(actor, stats):
    t = time.clock() - actor.sign.spawn_time
    actor.centery += stats.speed*math.sin(t*math.pi)

def seeker_movement(actor, stats, hero):
    t = time.clock() - actor.sign.spawn_time
    dx, dy = actor.centerx - hero.centerx, hero.centery - actor.centery
    dist = math.hypot(dx,dy)
    dx, dy = dx / dist, dy / dist
    actor.centerx += (stats.speed * dx)
    actor.centery += (stats.speed * dy)
