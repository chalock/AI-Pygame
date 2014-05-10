import physics as helper
from managers import score_manager as da_boss
from managers import sound_manager as dj
from models.entities import Hero
import enemy_wave_generator as mavericks

from queue import Queue


class GameState:
    def __init__(self):
        self.hero = Hero()
        self.score = 0 # Score increments from defeating enemies and picking up rupees
        self.paused = False
        self.win = False
        self.game_over = False
        self.projectile_list = [] # List of projectiles onscreen.
        self.rupee_list = [] # List of present rupees onscreen.
        self.enemy_list = [] # List of present enemies of one wave.
        self.wave_queue = Queue() # List used as a queue of waves
        self.initialize_waves() # Initialize all of the waves into the the wave queue
        self.next_wave() # Start First Wave

    def toggle_paused(self):
        self.paused = not self.paused

    def update_rupees(self):
        for i in range(0, len(self.rupee_list)):
            collision = helper.check_collision(self.hero, self.rupee_list[i])
            self.rupee_list[i].move()
            if collision:
                dj.play_beep()
                self.score += da_boss.calculate_score("RUPEE") # Increment Score
                del self.rupee_list[i]
                break


    def update_pews(self):
        for pew in range(len(self.projectile_list)):
            if self.projectile_list[pew].is_out_of_screen():
                del self.projectile_list[pew]
                break
        for pew in self.projectile_list:
            pew.move()


    def hero_fire(self):
        pew = self.hero.fire_bullet()
        self.projectile_list.append(pew)


    def update_enemies(self):
        for projectile in self.projectile_list:
            for enemy_index in range(len(self.enemy_list)):
                if helper.check_collision(projectile, self.enemy_list[enemy_index]):
                    self.rupee_list.append(self.enemy_list[enemy_index].drop())
                    self.score += 300
                    del self.enemy_list[enemy_index]
                    break
        
        for enemy_index in range(len(self.enemy_list)):
            if self.enemy_list[enemy_index].right < 0 :
                del self.enemy_list[enemy_index]
                break

        # For the laser detection
        for enemy_index in range(len(self.enemy_list)):
            if self.hero.is_firing_laser:
                if helper.check_collision(self.enemy_list[enemy_index], self.hero.laser):
                    self.rupee_list.append(self.enemy_list[enemy_index].drop())
                    self.score += 300
                    del self.enemy_list[enemy_index]
                    break


        for enemy in self.enemy_list:
            enemy.move()

        if len(self.enemy_list) == 0:
            self.next_wave()

    def initialize_waves(self):
        wave_1 = mavericks.generate_inverse_v_shaped_wave()
        wave_2 = mavericks.generate_diagonal_wave_1()
        wave_3 = mavericks.generate_diagonal_wave_2()
        wave_4 = mavericks.generate_vertical_wave()
        wave_5 = mavericks.generate_vertical_wave()
        wave_6 = mavericks.generate_diagonal_wave_2()
        wave_7 = mavericks.generate_diagonal_wave_1()
        wave_8 = mavericks.generate_inverse_v_shaped_wave()
        self.wave_queue.enqueue(wave_1)
        self.wave_queue.enqueue(wave_2)
        self.wave_queue.enqueue(wave_3)
        self.wave_queue.enqueue(wave_4)
        self.wave_queue.enqueue(wave_5)
        self.wave_queue.enqueue(wave_6)
        self.wave_queue.enqueue(wave_7)
        self.wave_queue.enqueue(wave_8)


    def next_wave(self):
        if self.wave_queue.size > 0:
            self.enemy_list = self.wave_queue.dequeue()
        else:
            self.win = True


