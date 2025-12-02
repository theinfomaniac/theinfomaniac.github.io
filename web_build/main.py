
from cmu_graphics import *

import random

import os

from PIL import Image

SEAL_SIZE = 60

INITIAL_HUNGER = 80

INITIAL_HEALTH = 100

INITIAL_HAPPINESS = 70

INITIAL_ENERGY = 100

IMAGES_DIR = os.path.dirname(__file__)  

def try_load_image(filename, default=None):

    """Try to load an image file, return None if not found"""

    try:

        path = os.path.join(IMAGES_DIR, filename)

        if os.path.exists(path):

            img = Image.open(path)

            return CMUImage(img)

        return default

    except Exception as e:

        print(f"Could not load {filename}: {e}")

        return default

class TycoonManager:

    def __init__(self):

        self.fish_coins = 0

        self.lifetime_coins = 0

        self.pearls = 0 

        self.click_power = 1

        self.auto_income = 0

        self.sanctuary_rating = 0

        self.current_tab = 'BUILD' 

        self.scroll_y = 0

        self.max_scroll = 0

        self.buildings = {

            'bucket': {'name': 'Fish Bucket', 'count': 0, 'cost': 15, 'income': 0.5, 'desc': 'A simple bucket to hold fish.', 'icon': 'tycoon_icon_bucket.png'},

            'penguin': {'name': 'Penguin Helper', 'count': 0, 'cost': 100, 'income': 4, 'desc': 'Hires a penguin to catch fish.', 'icon': 'tycoon_icon_penguin.png'},

            'platform': {'name': 'Ice Platform', 'count': 0, 'cost': 500, 'income': 12, 'desc': 'More space for seals to relax.', 'icon': 'ice.png'},

            'boat': {'name': 'Tour Boat', 'count': 0, 'cost': 2000, 'income': 45, 'desc': 'Tourists pay to see the seals.', 'icon': 'tycoon_icon_boat.png'},

            'research': {'name': 'Research Lab', 'count': 0, 'cost': 8000, 'income': 150, 'desc': 'Scientific funding for seal study.', 'icon': 'tycoon_icon_research.png'},

            'aquarium': {'name': 'Mega Aquarium', 'count': 0, 'cost': 50000, 'income': 600, 'desc': 'A world-class seal habitat.', 'icon': 'tycoon_icon_aquarium.png'},

            'drone': {'name': 'Fish Drone', 'count': 0, 'cost': 300000, 'income': 1200, 'desc': 'Automated fishing drone.', 'icon': 'tycoon_icon_drone.png'},

            'satellite': {'name': 'Seal Satellite', 'count': 0, 'cost': 1000000, 'income': 5000, 'desc': 'Track seals from space.', 'icon': 'tycoon_icon_satellite.png'},

            'underwater_base': {'name': 'Underwater Base', 'count': 0, 'cost': 5000000, 'income': 15000, 'desc': 'A secret base for seals.', 'icon': 'tycoon_icon_base.png'},

            'moon_colony': {'name': 'Moon Colony', 'count': 0, 'cost': 100000000, 'income': 100000, 'desc': 'Seals on the moon!', 'icon': 'tycoon_icon_moon.png'}

        }

        self.upgrades = {

            'sharp_claws': {'name': 'Sharper Claws', 'cost': 500, 'type': 'click_mult', 'value': 2, 'desc': 'Click Power x2', 'owned': False},

            'big_buckets': {'name': 'Bigger Buckets', 'cost': 1000, 'type': 'build_mult', 'target': 'bucket', 'value': 2, 'desc': 'Buckets are twice as effective', 'owned': False},

            'penguin_union': {'name': 'Penguin Union', 'cost': 5000, 'type': 'build_mult', 'target': 'penguin', 'value': 2, 'desc': 'Penguins work harder', 'owned': False},

            'gold_fish': {'name': 'Golden Fish', 'cost': 25000, 'type': 'global_mult', 'value': 1.5, 'desc': 'All income x1.5', 'owned': False},

            'click_master': {'name': 'Click Master', 'cost': 50000, 'type': 'click_mult', 'value': 5, 'desc': 'Click Power x5', 'owned': False},

            'marketing': {'name': 'Viral Marketing', 'cost': 100000, 'type': 'global_mult', 'value': 2.0, 'desc': 'All income x2.0', 'owned': False},

            'drone_battery': {'name': 'Better Batteries', 'cost': 1000000, 'type': 'build_mult', 'target': 'drone', 'value': 2, 'desc': 'Drones last longer', 'owned': False},

            'base_shield': {'name': 'Base Shielding', 'cost': 20000000, 'type': 'build_mult', 'target': 'underwater_base', 'value': 2, 'desc': 'Protects the base', 'owned': False},

            'moon_cheese': {'name': 'Moon Cheese', 'cost': 500000000, 'type': 'build_mult', 'target': 'moon_colony', 'value': 3, 'desc': 'Moon is made of cheese', 'owned': False}

        }

        self.skills = {

            'pearl_power': {'name': 'Pearl Power', 'cost': 1, 'desc': '+10% Income per Pearl (Passive)', 'level': 0, 'max': 1}, 

            'click_frenzy': {'name': 'Click Frenzy', 'cost': 5, 'desc': 'Clicks are 5x stronger', 'level': 0, 'max': 5},

            'cheaper_builds': {'name': 'Efficient Build', 'cost': 10, 'desc': 'Buildings cost 10% less', 'level': 0, 'max': 5},

            'offline_gains': {'name': 'Time Warp', 'cost': 25, 'desc': 'Start with 5% of previous coins', 'level': 0, 'max': 1},

            'golden_touch': {'name': 'Golden Touch', 'cost': 50, 'desc': 'Clicks give +1% of CPS', 'level': 0, 'max': 5},

            'angel_investor': {'name': 'Angel Investor', 'cost': 100, 'desc': 'Start with 1 free building of each type', 'level': 0, 'max': 1}

        }

        self.click_particles = [] 

    def click(self):

        power = self.click_power

        if self.upgrades['sharp_claws']['owned']:

            power *= 2

        if self.upgrades['click_master']['owned']:

            power *= 5

        power *= (1 + self.skills['click_frenzy']['level'] * 4)

        if self.skills['golden_touch']['level'] > 0:

            cps_bonus = self.auto_income * (0.01 * self.skills['golden_touch']['level'])

            power += cps_bonus

        power *= (1 + self.pearls * 0.1)

        self.fish_coins += power

        self.lifetime_coins += power

        return power

    def buy_building(self, key):

        building = self.buildings[key]

        discount = 1.0 - (self.skills['cheaper_builds']['level'] * 0.1)

        base_cost = building['cost'] * (1.15 ** building['count'])

        cost = int(base_cost * discount)

        if self.fish_coins >= cost:

            self.fish_coins -= cost

            building['count'] += 1

            self.recalculate_income()

            return True

        return False

    def buy_upgrade(self, key):

        upgrade = self.upgrades[key]

        if not upgrade['owned'] and self.fish_coins >= upgrade['cost']:

            self.fish_coins -= upgrade['cost']

            upgrade['owned'] = True

            self.recalculate_income()

            if upgrade['type'] == 'click_mult':

                pass 

            return True

        return False

    def buy_skill(self, key):

        skill = self.skills[key]

        if skill['level'] < skill['max'] and self.pearls >= skill['cost']:

            self.pearls -= skill['cost']

            skill['level'] += 1

            self.recalculate_income()

            return True

        return False

    def recalculate_income(self):

        income = 0

        for key, b in self.buildings.items():

            b_income = b['income'] * b['count']

            if key == 'bucket' and self.upgrades['big_buckets']['owned']:

                b_income *= 2

            if key == 'penguin' and self.upgrades['penguin_union']['owned']:

                b_income *= 2

            if key == 'drone' and self.upgrades['drone_battery']['owned']:

                b_income *= 2

            if key == 'underwater_base' and self.upgrades['base_shield']['owned']:

                b_income *= 2

            if key == 'moon_colony' and self.upgrades['moon_cheese']['owned']:

                b_income *= 3

            income += b_income

        if self.upgrades['gold_fish']['owned']:

            income *= 1.5

        if self.upgrades['marketing']['owned']:

            income *= 2.0

        income *= (1 + self.pearls * 0.1)

        self.auto_income = income

    def rebirth(self):

        import math

        if self.lifetime_coins < 1000:

            return False

        new_pearls = int(math.sqrt(self.lifetime_coins / 1000))

        if new_pearls <= self.pearls:

            return False 

        gained = int(math.sqrt(self.fish_coins / 5000))

        if gained < 1:

            return False

        self.pearls += gained

        self.fish_coins = 0

        for b in self.buildings.values():

            b['count'] = 0

        if self.skills['angel_investor']['level'] > 0:

            for b in self.buildings.values():

                b['count'] = 1

        for u in self.upgrades.values():

            u['owned'] = False

        self.recalculate_income()

        return gained

    def update(self):

        inc = self.auto_income / 60

        self.fish_coins += inc

        self.lifetime_coins += inc

        for p in self.click_particles:

            p['life'] -= 1

            p['y'] -= 1

        self.click_particles = [p for p in self.click_particles if p['life'] > 0]

    def add_particle(self, x, y, amount):

        text = f"+{amount}" if isinstance(amount, (int, float)) else str(amount)

        if isinstance(amount, (int, float)):

            if amount >= 1000000: text = f"+{amount/1000000:.1f}M"

            elif amount >= 1000: text = f"+{amount/1000:.1f}K"

            else: text = f"+{int(amount)}"

        self.click_particles.append({

            'x': x, 'y': y, 'text': text, 'life': 40, 'color': 'lightGreen'

        })

class FloatingFish:

    def __init__(self, max_width, max_height):

        self.x_pct = random.uniform(-0.1, 1.1)

        self.y_pct = random.uniform(0.1, 0.9)

        self.speed = random.uniform(0.0005, 0.004)

        self.size_pct = random.uniform(0.05, 0.09)

        self.direction = random.choice([-1, 1])

        self.swim_offset = random.randint(0, 100)

        self.fish_type_index = 0 

    def move(self, time):

        self.x_pct += self.speed * self.direction

        if self.x_pct > 1.15:

            self.x_pct = -0.15

        elif self.x_pct < -0.15:

            self.x_pct = 1.15

    def draw(self, time, width, height, fish_image=None, fish_flipped_image=None):

        import math

        wobble = math.sin((time + self.swim_offset) / 10) * (height * 0.007)

        x = self.x_pct * width

        y = self.y_pct * height

        size = self.size_pct * min(width, height)

        if fish_image:

            is_miku = (self.fish_type_index == 4)

            img_to_use = fish_image

            if is_miku:

                if self.direction == 1 and fish_flipped_image:

                    img_to_use = fish_flipped_image

                elif self.direction == -1:

                    img_to_use = fish_image

            else:

                if self.direction == -1 and fish_flipped_image:

                    img_to_use = fish_flipped_image

                elif self.direction == 1:

                    img_to_use = fish_image

            drawImage(img_to_use, x, y + wobble, width=size, height=size*0.6, align='center')

        else:

            drawOval(x, y + wobble, size, size * 0.6, 

                    fill=rgb(255, 150, 50), opacity=60)

            tail_x = x - (size/2 * self.direction)

            tail_size = size * 0.3

            drawPolygon(tail_x, y + wobble,

                       tail_x - tail_size * self.direction, y + wobble - tail_size * 0.5,

                       tail_x - tail_size * self.direction, y + wobble + tail_size * 0.5,

                       fill=rgb(255, 130, 30), opacity=60)

class Bubble:

    def __init__(self):

        self.x_pct = random.uniform(0, 1)

        self.y_pct = random.uniform(0.4, 1.1)

        self.speed = random.uniform(0.001, 0.003)

        self.size_pct = random.uniform(0.01, 0.025)

    def move(self):

        self.y_pct -= self.speed

        if self.y_pct < -0.02:

            self.y_pct = 1.05

            self.x_pct = random.uniform(0, 1)

    def draw(self, width, height, custom_image=None):

        x = self.x_pct * width

        y = self.y_pct * height

        size = self.size_pct * min(width, height)

        if custom_image:

            drawImage(custom_image, x, y, width=size*2, height=size*2, align='center', opacity=70)

        else:

            drawCircle(x, y, size, fill='white', opacity=70)

            drawCircle(x - size/3, y - size/3, size/2, fill='white', opacity=80)

class LightParticle:

    def __init__(self):

        self.x_pct = random.uniform(0, 1)

        self.y_pct = random.uniform(-0.1, 0.6)

        self.speed = random.uniform(0.0003, 0.001)

        self.size_pct = random.uniform(0.002, 0.006)

        self.drift = random.uniform(-0.0005, 0.0005)

    def move(self):

        self.y_pct += self.speed

        self.x_pct += self.drift

        if self.y_pct > 1.1:

            self.y_pct = -0.1

            self.x_pct = random.uniform(0, 1)

        if self.x_pct < -0.1 or self.x_pct > 1.1:

            self.x_pct = random.uniform(0, 1)

    def draw(self, width, height, time):

        import math

        x = self.x_pct * width

        y = self.y_pct * height

        size = self.size_pct * min(width, height)

        opacity = 20 + abs(math.sin(time / 20 + self.x_pct * 10)) * 30

        drawStar(x, y, size, 4, fill='white', opacity=opacity)

class GameStats:

    def __init__(self):

        self.hunger = INITIAL_HUNGER

        self.health = INITIAL_HEALTH

        self.max_health = INITIAL_HEALTH

        self.happiness = INITIAL_HAPPINESS

        self.energy = INITIAL_ENERGY

        self.day = 1

        self.age_days = 0

        self.orca_threat = 5  

        self.mother_chance = 2  

        self.visibility = 50  

        self.exp = 0

        self.lv = 1

    def daily_decay(self):

        """Natural daily stat decay"""

        self.hunger = max(0, self.hunger - random.randint(15, 25))

        self.energy = max(0, self.energy - random.randint(10, 20))

        self.happiness = max(0, self.happiness - random.randint(5, 15))

        if self.hunger < 30:

            self.health = max(0, self.health - random.randint(5, 15))

        if self.energy < 20:

            self.health = max(0, self.health - random.randint(3, 10))

    def is_alive(self):

        return self.health > 0 and self.hunger > 0

    def increase_threats(self):

        """Increase orca threat and mother chance each day"""

        self.orca_threat = min(95, self.orca_threat + random.randint(1, 2))

        self.mother_chance = min(90, self.mother_chance + random.randint(1, 2))

    def gain_exp(self, amount):

        self.exp += amount

        while self.exp >= 50 * self.lv:

            self.exp -= 50 * self.lv

            self.lv += 1

            self.max_health += 20

            self.health = self.max_health

            return True 

        return False

class Action:

    def __init__(self, name, description, effects, visibility_change=0, exploration_bonus=0):

        self.name = name

        self.description = description

        self.effects = effects  

        self.visibility_change = visibility_change  

        self.exploration_bonus = exploration_bonus  

def draw_seal_default(x, y, size, emotion='happy'):

    """Draw the seal character with default graphics"""

    drawOval(x + size * 0.08, y + size * 0.12, size * 1.15, size * 0.85, fill='black', opacity=15)

    drawOval(x + size * 0.04, y + size * 0.06, size * 1.08, size * 0.78, fill='black', opacity=12)

    drawOval(x, y, size * 1.03, size * 0.73, fill='lightCyan', opacity=8)

    drawOval(x, y, size * 1.05, size * 0.75, fill=rgb(85, 95, 105))

    drawOval(x, y, size, size * 0.7, fill=rgb(110, 120, 130))

    drawOval(x - size * 0.05, y + size * 0.05, size * 0.85, size * 0.55, fill=rgb(130, 140, 150))

    drawOval(x + size * 0.3, y + size * 0.15, size * 0.25, size * 0.15, fill=rgb(90, 100, 110), rotateAngle=-25)

    head_x = x + size * 0.35

    head_y = y - size * 0.1

    drawCircle(head_x, head_y, size * 0.38, fill=rgb(100, 110, 120))

    drawCircle(head_x - size * 0.05, head_y, size * 0.35, fill=rgb(125, 135, 145))

    drawOval(x - size * 0.28, y + size * 0.1, size * 0.28, size * 0.18, fill=rgb(85, 95, 105), rotateAngle=35)

    drawOval(x - size * 0.15, y + size * 0.12, size * 0.28, size * 0.18, fill=rgb(85, 95, 105), rotateAngle=-35)

    drawOval(x, y + size * 0.1, size * 0.65, size * 0.45, fill=rgb(180, 190, 200), opacity=50)

    drawOval(x, y + size * 0.12, size * 0.55, size * 0.38, fill=rgb(210, 215, 220), opacity=40)

    eye_y = head_y + size * 0.02

    eye_spacing = size * 0.15

    if emotion == 'happy':

        drawArc(head_x - eye_spacing, eye_y, size * 0.12, size * 0.09, 0, 180, fill='black')

        drawArc(head_x + eye_spacing, eye_y, size * 0.12, size * 0.09, 0, 180, fill='black')

    elif emotion == 'sad':

        drawCircle(head_x - eye_spacing, eye_y, size * 0.06, fill='black')

        drawCircle(head_x + eye_spacing, eye_y, size * 0.06, fill='black')

        drawOval(head_x - eye_spacing, eye_y + size * 0.12, size * 0.04, size * 0.08, fill='lightBlue', opacity=80)

    elif emotion == 'tired':

        drawLine(head_x - eye_spacing - size * 0.06, eye_y, head_x - eye_spacing + size * 0.06, eye_y, lineWidth=2.5)

        drawLine(head_x + eye_spacing - size * 0.06, eye_y, head_x + eye_spacing + size * 0.06, eye_y, lineWidth=2.5)

    else:  

        drawCircle(head_x - eye_spacing, eye_y, size * 0.06, fill='black')

        drawCircle(head_x + eye_spacing, eye_y, size * 0.06, fill='black')

        drawCircle(head_x - eye_spacing - size * 0.02, eye_y - size * 0.02, size * 0.025, fill='white')

        drawCircle(head_x + eye_spacing - size * 0.02, eye_y - size * 0.02, size * 0.025, fill='white')

    nose_y = head_y + size * 0.12

    drawOval(head_x, nose_y, size * 0.1, size * 0.08, fill='black')

    drawCircle(head_x - size * 0.02, nose_y - size * 0.02, size * 0.02, fill='gray', opacity=60)

    for i in range(-1, 2):

        whisker_y = nose_y + i * size * 0.08

        drawLine(head_x, nose_y, head_x + size * 0.35, whisker_y, lineWidth=1, fill=rgb(80, 80, 80))

        drawLine(head_x, nose_y, head_x - size * 0.35, whisker_y, lineWidth=1, fill=rgb(80, 80, 80))

def get_available_actions():

    return [

        Action('HIDE', 

               'Hide from predators (SAFEST)',

               {'energy': +20, 'happiness': -10},

               visibility_change=-30, exploration_bonus=0),

        Action('REST', 

               'Rest in a safe place',

               {'energy': +35, 'health': +5, 'happiness': +5},

               visibility_change=-20, exploration_bonus=0),

        Action('FORAGE',

               'Look for food close by',

               {'hunger': +25, 'energy': -10},

               visibility_change=+5, exploration_bonus=5),

        Action('HUNT',

               'Hunt for fish (risky but rewarding)',

               {'hunger': +40, 'energy': -20, 'happiness': +10},

               visibility_change=+15, exploration_bonus=10),

        Action('PLAY',

               'Play while staying alert',

               {'happiness': +30, 'energy': -15},

               visibility_change=+10, exploration_bonus=8),

        Action('EXPLORE',

               'Explore nearby areas',

               {'happiness': +15, 'energy': -25},

               visibility_change=+20, exploration_bonus=20),

        Action('VENTURE',

               'Venture far from safety',

               {'happiness': +20, 'energy': -35, 'health': -5},

               visibility_change=+35, exploration_bonus=35),

        Action('SEARCH',

               'Actively search for mother (VERY RISKY)',

               {'energy': -40, 'health': -10, 'happiness': +25},

               visibility_change=+45, exploration_bonus=50),

    ]

def check_orca_encounter(stats, action):

    """Check if you encounter an orca"""

    actual_threat = stats.orca_threat * (stats.visibility / 50)

    if random.randint(0, 100) < actual_threat:

        return True

    return False

def check_mother_found(stats, action):

    """Check if you find your mother"""

    actual_chance = stats.mother_chance + (action.exploration_bonus * 0.3)

    if random.randint(0, 100) < actual_chance:

        return True

    return False

def get_random_event():

    """Returns a random minor event"""

    if random.randint(0, 100) < 20:  

        events = [

            ('[BONUS] Found extra fish!', {'hunger': +15, 'happiness': +10}),

            ('[FRIEND] Made penguin friends!', {'happiness': +20}),

            ('[HAZARD] Strong currents drained energy.', {'energy': -15}),

            ('[WEATHER] Beautiful day lifted spirits!', {'happiness': +15}),

            ('[FIND] Discovered a safe resting spot!', {'health': +10}),

            ('[HUMAN] A kind human threw you a fish!', {'hunger': +20, 'happiness': +10}),

            ('[HUMAN] A tourist took a cute photo!', {'happiness': +15}),

            ('[HUMAN] Researchers observed you safely.', {'happiness': +5}),

            ('[HUMAN] A mean human threw a rock!', {'health': -10, 'happiness': -10}),

            ('[HUMAN] Loud humans scared you away.', {'energy': -10, 'happiness': -5}),

            ('[HUMAN] Plastic trash got stuck on you!', {'health': -5, 'happiness': -15}),

            ('[BOAT] Fishing boat dropped scraps!', {'hunger': +25}),

            ('[BOAT] Gentle wake was fun to surf!', {'happiness': +10, 'energy': +5}),

            ('[BOAT] Propeller noise hurt your ears.', {'happiness': -15}),

            ('[BOAT] Oil spill! Yuck!', {'health': -5, 'happiness': -10}),

            ('[BOAT] Speedboat came too close!', {'energy': -15, 'happiness': -5}),

        ]

        return random.choice(events)

    return None

def get_stat_image(stat_images, stat_name, value):

    """Get the appropriate stat icon based on value (0, 25, 50, 75, 100)"""

    if stat_name not in stat_images or not stat_images[stat_name]:

        return None

    if value <= 12.5:

        level = 0

    elif value <= 37.5:

        level = 25

    elif value <= 62.5:

        level = 50

    elif value <= 87.5:

        level = 75

    else:

        level = 100

    img = stat_images[stat_name].get(level, None)

    if img:

        return img

    for fallback_level in [100, 75, 50, 25, 0]:

        if fallback_level in stat_images[stat_name]:

            return stat_images[stat_name][fallback_level]

    return None

class Button:

    def __init__(self, x, y, width, height, text, action, custom_image=None, custom_hover_image=None):

        self.x_pct = x

        self.y_pct = y

        self.width_pct = width

        self.height_pct = height

        self.text = text

        self.action = action

        self.hovered = False

        self.custom_image = custom_image

        self.custom_hover_image = custom_hover_image

        self.x = x

        self.y = y

        self.width = width

        self.height = height

    def is_clicked(self, mouseX, mouseY):

        return (self.x - self.width//2 < mouseX < self.x + self.width//2 and

                self.y - self.height//2 < mouseY < self.y + self.height//2)

    def draw(self, button_image=None, button_hover_image=None, app_width=800, app_height=900):

        shadow_offset = self.width * 0.025

        drawRect(self.x + shadow_offset, self.y + shadow_offset, self.width, self.height, 

                fill='black', opacity=40, align='center')

        if self.hovered and self.custom_hover_image:

            drawImage(self.custom_hover_image, self.x, self.y, width=self.width, height=self.height, align='center')

        elif self.custom_image:

            drawImage(self.custom_image, self.x, self.y, width=self.width, height=self.height, align='center')

        elif self.hovered and button_hover_image:

            drawImage(button_hover_image, self.x, self.y, width=self.width, height=self.height, align='center')

        elif button_image:

            drawImage(button_image, self.x, self.y, width=self.width, height=self.height, align='center')

        else:

            if self.hovered:

                bg_color = rgb(80, 150, 200)

                border_color = 'yellow'

                border_width = max(2, int(self.width * 0.025))

            else:

                bg_color = rgb(50, 100, 150)

                border_color = 'white'

                border_width = max(1, int(self.width * 0.016))

            drawRect(self.x, self.y, self.width, self.height, 

                    fill=bg_color, border=border_color, borderWidth=border_width, align='center')

            drawRect(self.x, self.y - self.height * 0.2, self.width * 0.9, self.height * 0.3,

                    fill='white', opacity=15, align='center')

            if self.hovered:

                glow_size = self.width * 0.03

                drawRect(self.x, self.y, self.width + glow_size, self.height + glow_size,

                        fill='yellow', opacity=10, align='center')

        text_size = max(10, int(min(app_width, app_height) * 0.032))

        drawLabel(self.text, self.x + 1, self.y + 1, size=text_size, bold=True, fill='black', font='ArcadeClassic')

        drawLabel(self.text, self.x, self.y, size=text_size, bold=True, fill='white', font='ArcadeClassic')

class PlayerSoul:

    """The player's 'soul' - a small heart they control in the battle box"""

    def __init__(self, box_x, box_y, box_w, box_h):

        self.box_x = box_x  

        self.box_y = box_y

        self.box_w = box_w

        self.box_h = box_h

        self.x = box_x + box_w / 2  

        self.y = box_y + box_h / 2

        self.size = 24  

        self.speed = 4

        self.invincible_frames = 0

    def move(self, dx, dy):

        """Move the soul within the battle box bounds"""

        new_x = self.x + dx * self.speed

        new_y = self.y + dy * self.speed

        padding = self.size / 2

        self.x = max(self.box_x + padding, min(self.box_x + self.box_w - padding, new_x))

        self.y = max(self.box_y + padding, min(self.box_y + self.box_h - padding, new_y))

    def update_box(self, box_x, box_y, box_w, box_h):

        """Update the battle box dimensions (for window resizing)"""

        rel_x = (self.x - self.box_x) / self.box_w if self.box_w > 0 else 0.5

        rel_y = (self.y - self.box_y) / self.box_h if self.box_h > 0 else 0.5

        self.box_x = box_x

        self.box_y = box_y

        self.box_w = box_w

        self.box_h = box_h

        self.x = box_x + rel_x * box_w

        self.y = box_y + rel_y * box_h

    def draw(self, soul_image=None):

        """Draw the player's soul as a heart"""

        if self.invincible_frames > 0:

            if (self.invincible_frames // 3) % 2 == 0:

                return

        if soul_image:

            drawImage(soul_image, self.x, self.y, width=self.size, height=self.size, align='center')

        else:

            drawCircle(self.x - self.size * 0.2, self.y - self.size * 0.15, self.size * 0.35, fill='red')

            drawCircle(self.x + self.size * 0.2, self.y - self.size * 0.15, self.size * 0.35, fill='red')

            drawPolygon(self.x - self.size * 0.45, self.y - self.size * 0.1,

                       self.x + self.size * 0.45, self.y - self.size * 0.1,

                       self.x, self.y + self.size * 0.45,

                       fill='red')

class OrcaBoss:

    """The orca boss enemy"""

    def __init__(self):

        self.max_health = 100

        self.health = 100

        self.display_health = 100 

        self.phase = 1  

        self.attack_timer = 0

        self.current_attack = None

        self.hurt_frames = 0

        self.mercy_meter = 0  

        self.spared = False

    def take_damage(self, amount):

        """Take damage and trigger hurt animation"""

        self.health = max(0, self.health - amount)

        self.hurt_frames = 15

    def update(self):

        """Update boss state"""

        if self.display_health > self.health:

            self.display_health -= (self.display_health - self.health) * 0.1

            if self.display_health - self.health < 0.5:

                self.display_health = self.health

    def is_defeated(self):

        return self.health <= 0 or self.spared

class Projectile:

    """A projectile that the player must dodge"""

    def __init__(self, x, y, vx, vy, proj_type='bone', size=25, update_func=None):

        self.x = x

        self.y = y

        self.vx = vx

        self.vy = vy

        self.type = proj_type  

        self.size = size

        self.rotation = 0

        self.active = True

        self.timer = 0

        self.initial_y = y

        self.update_func = update_func

    def update(self, box_x=0, box_y=0, box_w=0, box_h=0):

        """Move the projectile"""

        self.timer += 1

        if self.update_func:

            self.update_func(self, box_x, box_y, box_w, box_h)

        else:

            self.x += self.vx

            self.y += self.vy

            self.rotation += 5

    def is_in_bounds(self, box_x, box_y, box_w, box_h):

        """Check if projectile is still in the battle box area (with margin)"""

        margin = 100

        return (box_x - margin < self.x < box_x + box_w + margin and

                box_y - margin < self.y < box_y + box_h + margin)

    def collides_with(self, soul):

        """Check collision with player soul"""

        dist = ((self.x - soul.x)**2 + (self.y - soul.y)**2)**0.5

        return dist < (self.size + soul.size) / 2

    def draw(self, proj_images=None):

        """Draw the projectile"""

        if proj_images and self.type in proj_images and proj_images[self.type]:

            drawImage(proj_images[self.type], self.x, self.y, 

                     width=self.size, height=self.size, align='center',

                     rotateAngle=self.rotation)

        else:

            if self.type == 'bone':

                drawRect(self.x, self.y, self.size * 1.5, self.size * 0.4, 

                        fill='white', align='center', rotateAngle=self.rotation)

                drawCircle(self.x - self.size * 0.5, self.y, self.size * 0.3, fill='white')

                drawCircle(self.x + self.size * 0.5, self.y, self.size * 0.3, fill='white')

            elif self.type == 'bubble':

                drawCircle(self.x, self.y, self.size * 0.5, fill=rgb(100, 180, 255), opacity=70)

                drawCircle(self.x - self.size * 0.15, self.y - self.size * 0.15, 

                          self.size * 0.15, fill='white', opacity=50)

            elif self.type == 'tooth':

                drawPolygon(self.x, self.y - self.size * 0.6,

                           self.x - self.size * 0.3, self.y + self.size * 0.4,

                           self.x + self.size * 0.3, self.y + self.size * 0.4,

                           fill='white', border='gray', borderWidth=1)

            elif self.type == 'wave':

                drawOval(self.x, self.y, self.size, self.size * 0.5, 

                        fill=rgb(50, 150, 200), opacity=80)

            elif self.type == 'warning':

                color = 'red' if (self.timer // 4) % 2 == 0 else 'orange'

                if self.vx == 0: 

                    drawRect(self.x, self.y, self.size, 1000, fill=color, opacity=50, align='center')

                else: 

                    drawRect(self.x, self.y, 1000, self.size, fill=color, opacity=50, align='center')

class FishingMinigame:

    """Mini-game for catching difficult fish"""

    def __init__(self, app_width, app_height, fish_assets):

        self.w = app_width

        self.h = app_height

        self.fish_assets = fish_assets

        self.fish_img = None

        self.fish_flipped_img = None

        if fish_assets:

            idx = random.randint(0, len(fish_assets) - 1)

            self.fish_img = fish_assets[idx]['normal']

            self.fish_flipped_img = fish_assets[idx]['flipped']

            self.is_miku = (idx == 4) 

        self.difficulty = random.random() 

        if self.difficulty > 0.9: 

            self.food_reward = 40

            self.exp_reward = 30

            self.bar_speed = 25 

            self.target_scale = 0.10 

            self.fish_name = "LEGENDARY FISH"

        elif self.difficulty > 0.6: 

            self.food_reward = 25

            self.exp_reward = 20

            self.bar_speed = 20 

            self.target_scale = 0.12

            self.fish_name = "Big Fish"

        else: 

            self.food_reward = 15

            self.exp_reward = 10

            self.bar_speed = 15 

            self.target_scale = 0.15

            self.fish_name = "Small Fish"

        self.box_w = min(self.w, self.h) * 0.7

        self.box_h = 100

        self.box_x = (self.w - self.box_w) / 2

        self.box_y = (self.h * 0.6) - (self.box_h / 2)

        self.target_w = self.box_w * self.target_scale

        max_offset = (self.box_w - self.target_w) / 2 - 10

        self.target_offset = random.randint(int(-max_offset), int(max_offset))

        self.bar_pos = -self.box_w / 2

        self.bar_dir = 1

        self.active = True

        self.result = None 

        self.message = "PRESS Z!"

        self.message_timer = 0

        self.fish_x = self.w / 2

        self.fish_y = self.box_y - 80

        self.fish_wobble = 0

    def update(self):

        if not self.active:

            if self.message_timer > 0:

                self.message_timer -= 1

            return

        self.bar_pos += self.bar_speed * self.bar_dir

        limit = self.box_w / 2 - 10

        if self.bar_pos > limit:

            self.bar_pos = limit

            self.bar_dir = -1

        elif self.bar_pos < -limit:

            self.bar_pos = -limit

            self.bar_dir = 1

        self.fish_wobble += 0.1

    def handle_key_press(self, key):

        key_lower = key.lower() if isinstance(key, str) else key

        if not self.active:

            if key_lower in ['z', 'enter', 'space']:

                self.message_timer = 0

            return

        if key_lower in ['z', 'enter', 'space']:

            self.attempt_catch()

    def handle_mouse_press(self, x, y):

        if not self.active:

            self.message_timer = 0

            return

        self.attempt_catch()

    def attempt_catch(self):

        self.active = False

        dist = abs(self.bar_pos - self.target_offset)

        hit_window = self.target_w / 2

        if dist <= hit_window:

            self.result = 'caught'

            self.message = f"+{self.food_reward} Food +{self.exp_reward} EXP!"

        else:

            self.result = 'escaped'

            self.message = "IT GOT AWAY..."

        self.message_timer = 60

    def draw(self, app):

        import math

        drawRect(0, 0, self.w, self.h, fill='black', opacity=70)

        drawLabel("FISHING MINIGAME", self.w/2, self.h * 0.2, size=30, fill='white', bold=True, font='Determination Mono')

        fish_y = self.fish_y + math.sin(self.fish_wobble) * 10

        if self.fish_img:

            img = self.fish_flipped_img if self.bar_dir < 0 and not self.is_miku else self.fish_img

            if self.is_miku and self.bar_dir > 0: img = self.fish_flipped_img 

            drawImage(img, self.fish_x, fish_y, width=80, height=50, align='center')

        if hasattr(app, 'fishing_bg_image') and app.fishing_bg_image:

             drawImage(app.fishing_bg_image, self.box_x, self.box_y, width=self.box_w, height=self.box_h)

        else:

            drawRect(self.box_x, self.box_y, self.box_w, self.box_h, fill='black', border='white', borderWidth=4)

        center_x = self.box_x + self.box_w / 2

        target_x = center_x + self.target_offset

        if hasattr(app, 'fishing_target_image') and app.fishing_target_image:

             drawImage(app.fishing_target_image, target_x, self.box_y + self.box_h/2, 

                      width=self.target_w, height=self.box_h * 0.9, align='center')

        else:

            drawRect(target_x - self.target_w/2, self.box_y + 4, 

                     self.target_w, self.box_h - 8, 

                     fill=rgb(100, 255, 100), opacity=60, border='lightGreen')

        bar_x = center_x + self.bar_pos

        if hasattr(app, 'fight_bar_image') and app.fight_bar_image:

            drawImage(app.fight_bar_image, bar_x, self.box_y + self.box_h/2, 

                     width=16, height=self.box_h * 0.9, align='center')

        else:

            drawRect(bar_x - 4, self.box_y + 10, 8, self.box_h - 20, fill='white', border='black', borderWidth=1)

        msg_color = 'yellow' if self.active else ('lightGreen' if self.result == 'caught' else 'red')

        drawLabel(self.message, self.w/2, self.box_y - 30, size=20, fill=msg_color, bold=True, font='Determination Mono')

class BossBattle:

    """Manages the entire boss battle state"""

    def __init__(self, app_width, app_height):

        self.w = app_width

        self.h = app_height

        self.phase = 'player_turn'  

        self.update_dimensions(app_width, app_height)

        self.soul = PlayerSoul(self.box_x, self.box_y, self.box_w, self.box_h)

        self.orca = OrcaBoss()

        self.projectiles = []

        self.player_hp = 20

        self.player_max_hp = 20

        self.player_lv = 1

        self.phase = 'player_turn'  

        self.turn_timer = 0

        self.attack_duration = 180  

        self.full_message = 'The orca blocks your path!'

        self.display_message = ''

        self.char_index = 0

        self.type_timer = 0

        self.message_timer = 120

        self.current_pattern = 0

        self.pattern_timer = 0

        self.menu_selection = 0  

        self.submenu_selection = 0

        self.heals_remaining = 3

        self.fight_bar_pos = 0

        self.fight_bar_speed = 15

        self.fight_bar_dir = 1

        self.inventory = [

            {'name': 'Fatty Fish', 'heal': 10, 'desc': 'Heals 10 HP'},

            {'name': 'Kelp', 'heal': 5, 'desc': 'Heals 5 HP'},

            {'name': 'Ice Chunk', 'heal': 2, 'desc': 'Heals 2 HP'}

        ]

        self.keys_held = {'w': False, 'a': False, 's': False, 'd': False,

                         'up': False, 'left': False, 'down': False, 'right': False}

    def set_message(self, text, duration=60):

        """Set a new message with typewriter effect"""

        self.full_message = text

        self.display_message = ''

        self.char_index = 0

        self.type_timer = 0

        self.message_timer = duration

    def update_dimensions(self, w, h):

        """Update all dimensions based on window size"""

        self.w = w

        self.h = h

        self.menu_w = self.w * 0.85

        self.menu_h = self.h * 0.35

        self.menu_x = (self.w - self.menu_w) / 2

        self.menu_y_pos = (self.h * 0.63) - (self.menu_h / 2) 

        box_size = min(self.w, self.h) * 0.35

        self.attack_w = box_size

        self.attack_h = box_size

        self.attack_x = (self.w - self.attack_w) / 2

        self.attack_y = (self.h * 0.63) - (self.attack_h / 2) 

        if hasattr(self, 'phase') and self.phase == 'dodging':

            self.set_box_shape('square')

        else:

            self.set_box_shape('rectangle')

        self.menu_y = self.h * 0.92

    def set_box_shape(self, shape):

        """Set the battle box shape to 'rectangle' or 'square'"""

        if shape == 'square':

            self.box_x = self.attack_x

            self.box_y = self.attack_y

            self.box_w = self.attack_w

            self.box_h = self.attack_h

        else:

            self.box_x = self.menu_x

            self.box_y = self.menu_y_pos

            self.box_w = self.menu_w

            self.box_h = self.menu_h

        if hasattr(self, 'soul'):

            self.soul.update_box(self.box_x, self.box_y, self.box_w, self.box_h)

            if shape == 'square': 

                self.soul.size = 28

            else: 

                self.soul.size = 16

        self.menu_y = self.h * 0.92

        self.btn_w = self.w * 0.2

        self.btn_h = self.h * 0.06

        spacing = self.w * 0.22

        start_x = (self.w - (spacing * 3)) / 2

        self.btn_positions = [start_x + i * spacing for i in range(4)]

    def start_attack_phase(self, attack_type):

        """Start the dodging phase with a specific attack pattern"""

        self.phase = 'dodging'

        self.set_box_shape('square')

        self.turn_timer = self.attack_duration

        self.current_pattern = attack_type

        self.pattern_timer = 0

        self.projectiles = []

        self.set_message('Dodge the attacks!', 60)

        self.soul.x = self.box_x + self.box_w / 2

        self.soul.y = self.box_y + self.box_h / 2

    def spawn_attack_pattern(self):

        """Spawn projectiles based on current attack pattern"""

        import math

    def spawn_attack_pattern(self):

        """Spawn projectiles based on current attack pattern"""

        import math

        if self.current_pattern == 0:

            if self.pattern_timer % 50 == 0:

                gap_size = 60

                gap_y = self.box_y + 20 + random.random() * (self.box_h - gap_size - 40)

                w = 10

                speed = 4

                self.projectiles.append(Projectile(self.box_x + self.box_w, self.box_y, -speed, 0, 'bone', 30))

                self.projectiles.append(Projectile(self.box_x + self.box_w, gap_y + gap_size, -speed, 0, 'bone', 30))

                if random.random() < 0.3:

                     self.projectiles.append(Projectile(self.box_x + random.random() * self.box_w, self.box_y - 20, 0, speed, 'bone', 30))

        elif self.current_pattern == 1:

            if self.pattern_timer % 15 == 0:

                def sine_update(p, bx, by, bw, bh):

                    p.x += p.vx

                    p.y = p.initial_y + math.sin(p.timer * 0.15) * 60

                    p.rotation += 5

                initial_y = self.box_y + self.box_h/2 + (random.random()*100 - 50)

                p = Projectile(self.box_x + self.box_w, initial_y, -4, 0, 'bubble', 25, update_func=sine_update)

                p.initial_y = initial_y

                self.projectiles.append(p)

        elif self.current_pattern == 2:

            if self.pattern_timer % 30 == 0:

                start_x = self.box_x + random.random() * self.box_w

                start_y = self.box_y

                dx = self.soul.x - start_x

                dy = self.soul.y - start_y

                mag = (dx**2 + dy**2)**0.5

                speed = 6

                self.projectiles.append(Projectile(start_x, start_y, (dx/mag)*speed, (dy/mag)*speed, 'tooth', 26))

                if random.random() < 0.5:

                    side_x = self.box_x if random.random() < 0.5 else self.box_x + self.box_w

                    side_y = self.box_y + random.random() * self.box_h

                    dx2 = self.soul.x - side_x

                    dy2 = self.soul.y - side_y

                    mag2 = (dx2**2 + dy2**2)**0.5

                    self.projectiles.append(Projectile(side_x, side_y, (dx2/mag2)*speed, (dy2/mag2)*speed, 'tooth', 26))

        elif self.current_pattern == 3:

            if self.pattern_timer in [10, 60, 110, 160]:

                def bounce_update(p, bx, by, bw, bh):

                    p.x += p.vx

                    p.y += p.vy

                    if p.x <= bx or p.x + p.size >= bx + bw: p.vx *= -1

                    if p.y <= by or p.y + p.size >= by + bh: p.vy *= -1

                    p.rotation += 5

                vx = 5 if random.random() > 0.5 else -5

                vy = 5 if random.random() > 0.5 else -5

                p = Projectile(self.box_x + self.box_w/2, self.box_y + self.box_h/2, vx, vy, 'wave', 32, update_func=bounce_update)

                self.projectiles.append(p)

        elif self.current_pattern == 4:

            if self.pattern_timer % 6 == 0:

                x = self.box_x + random.random() * self.box_w

                speed = 5 + random.random() * 4

                self.projectiles.append(Projectile(x, self.box_y, 0, speed, 'bubble', 22))

                if self.pattern_timer % 30 == 0:

                     self.projectiles.append(Projectile(self.box_x, self.box_y + random.random() * self.box_h, 5, 0, 'bubble', 22))

        elif self.current_pattern == 5:

            if self.pattern_timer % 40 == 0:

                y = self.box_y + random.random() * self.box_h

                speed = 4

                self.projectiles.append(Projectile(self.box_x, y, speed, 0, 'wave', 30))

                y2 = self.box_y + random.random() * self.box_h

                self.projectiles.append(Projectile(self.box_x + self.box_w, y2, -speed, 0, 'wave', 30))

        elif self.current_pattern == 6:

            if self.pattern_timer % 100 == 0:

                center_x = self.soul.x

                center_y = self.soul.y

                radius = 180

                count = 14

                for i in range(count):

                    angle = (i / count) * math.pi * 2

                    px = center_x + math.cos(angle) * radius

                    py = center_y + math.sin(angle) * radius

                    speed = 2.5

                    dx = center_x - px

                    dy = center_y - py

                    mag = (dx**2 + dy**2)**0.5

                    vx = (dx / mag) * speed

                    vy = (dy / mag) * speed

                    self.projectiles.append(Projectile(px, py, vx, vy, 'tooth', 25))

                radius2 = 240

                for i in range(count):

                    angle = ((i + 0.5) / count) * math.pi * 2

                    px = center_x + math.cos(angle) * radius2

                    py = center_y + math.sin(angle) * radius2

                    speed = 3

                    dx = center_x - px

                    dy = center_y - py

                    mag = (dx**2 + dy**2)**0.5

                    vx = (dx / mag) * speed

                    vy = (dy / mag) * speed

                    self.projectiles.append(Projectile(px, py, vx, vy, 'tooth', 25))

        elif self.current_pattern == 7:

            if self.pattern_timer % 45 == 0:

                count = random.randint(2, 3)

                is_vertical = random.random() > 0.5

                for i in range(count):

                    if is_vertical:

                        x = self.box_x + 20 + random.random() * (self.box_w - 40)

                        start_y = self.box_y + 25

                        def blast_update(p, bx, by, bw, bh):

                            p.timer += 1

                            if p.timer < 30: 

                                p.type = 'warning'

                                p.size = 20

                            elif p.timer == 30: 

                                p.type = 'bone'

                                p.size = 40

                                p.vy = 15

                            else:

                                p.y += p.vy

                        p = Projectile(x, start_y, 0, 0, 'warning', 20, update_func=blast_update)

                        self.projectiles.append(p)

                    else:

                        y = self.box_y + 20 + random.random() * (self.box_h - 40)

                        start_x = self.box_x + 25

                        def blast_update(p, bx, by, bw, bh):

                            p.timer += 1

                            if p.timer < 30: 

                                p.type = 'warning'

                                p.size = 20

                            elif p.timer == 30: 

                                p.type = 'bone'

                                p.size = 40

                                p.vx = 15

                            else:

                                p.x += p.vx

                        p = Projectile(start_x, y, 0, 0, 'warning', 20, update_func=blast_update)

                        p.rotation = 90

                        self.projectiles.append(p)

        elif self.current_pattern == 8:

            if self.pattern_timer % 90 == 0:

                spacing = 60

                rows = int(self.box_h / spacing)

                cols = int(self.box_w / spacing)

                for i in range(rows):

                    y = self.box_y + (i + 0.5) * spacing

                    speed = 3

                    if i % 2 == 0:

                        self.projectiles.append(Projectile(self.box_x, y, speed, 0, 'bubble', 20))

                    else:

                        self.projectiles.append(Projectile(self.box_x + self.box_w, y, -speed, 0, 'bubble', 20))

                def delayed_spawn(p, bx, by, bw, bh):

                    p.timer += 1

                    if p.timer == 45:

                        pass

                for j in range(cols):

                    x = self.box_x + (j + 0.5) * spacing

                    speed = 3

                    if j % 2 == 0:

                        self.projectiles.append(Projectile(x, self.box_y, 0, speed, 'bubble', 20))

                    else:

                        self.projectiles.append(Projectile(x, self.box_y + self.box_h, 0, -speed, 'bubble', 20))

        elif self.current_pattern == 9:

            if self.pattern_timer % 40 == 0:

                x = self.box_x + random.random() * self.box_w

                def star_update(p, bx, by, bw, bh):

                    p.timer += 1

                    p.y += p.vy

                    p.rotation += 10

                    if p.timer == 45:

                        p.active = False

                        for i in range(8):

                            angle = (i / 8) * math.pi * 2

                            speed = 4

                            vx = math.cos(angle) * speed

                            vy = math.sin(angle) * speed

                            pass 

                self.projectiles.append(Projectile(x, self.box_y - 40, 0, 6, 'tooth', 40))

                for i in range(3):

                    sx = x + (random.random() - 0.5) * 60

                    self.projectiles.append(Projectile(sx, self.box_y - 60 - random.random()*40, 0, 7, 'tooth', 15))

        elif self.current_pattern == 10:

            if self.pattern_timer % 50 == 0:

                col_w = 40

                cols = int(self.box_w / col_w)

                target_col = random.randint(0, cols-1)

                x = self.box_x + target_col * col_w + col_w/2

                def lightning_update(p, bx, by, bw, bh):

                    p.timer += 1

                    if p.timer < 30: 

                        p.type = 'warning'

                        p.size = 30

                    elif p.timer < 45: 

                        p.type = 'bone' 

                        p.size = 30

                    else:

                        p.active = False

                for i in range(10):

                    y = self.box_y + i * (self.box_h / 10)

                    p = Projectile(x, y, 0, 0, 'warning', 30, update_func=lightning_update)

                    self.projectiles.append(p)

        elif self.current_pattern == 11:

            if self.pattern_timer % 60 == 0:

                side = random.choice(['left', 'right'])

                if side == 'left':

                    start_x = self.box_x - 20

                    vx = 5

                else:

                    start_x = self.box_x + self.box_w + 20

                    vx = -5

                for i in range(5):

                    angle_offset = (i - 2) * 0.2

                    vy = math.sin(angle_offset) * 5

                    self.projectiles.append(Projectile(start_x, self.box_y + self.box_h/2, vx, vy, 'bubble', 20))

                y = self.box_y + self.box_h/2

                def beam_update(p, bx, by, bw, bh):

                    p.timer += 1

                    if p.timer < 40:

                        p.type = 'warning'

                    elif p.timer < 60:

                        p.type = 'bone' 

                        p.vx = 5 if side == 'left' else -5

        elif self.current_pattern == 12:

            spawn_index = self.pattern_timer // 5

            if self.pattern_timer % 5 == 0 and spawn_index % 4 != 0:

                center_x = self.box_x + self.box_w / 2

                center_y = self.box_y + self.box_h / 2

                angle = (self.pattern_timer * 0.1) 

                speed = 3.0

                vx = math.cos(angle) * speed

                vy = math.sin(angle) * speed

                self.projectiles.append(Projectile(center_x, center_y, vx, vy, 'bone', 20))

                self.projectiles.append(Projectile(center_x, center_y, -vx, -vy, 'bone', 20))

        elif self.current_pattern == 13:

            if self.pattern_timer % 40 == 0:

                edge = random.randint(0, 3)

                if edge == 0: 

                    x = self.box_x + random.random() * self.box_w

                    y = self.box_y

                elif edge == 1: 

                    x = self.box_x + self.box_w

                    y = self.box_y + random.random() * self.box_h

                elif edge == 2: 

                    x = self.box_x + random.random() * self.box_w

                    y = self.box_y + self.box_h

                else: 

                    x = self.box_x

                    y = self.box_y + random.random() * self.box_h

                def homing_update(p, bx, by, bw, bh):

                    p.timer += 1

                    pass

                dx = self.soul.x - x

                dy = self.soul.y - y

                mag = (dx**2 + dy**2)**0.5

                speed = 3

                vx = (dx/mag) * speed

                vy = (dy/mag) * speed

                self.projectiles.append(Projectile(x, y, vx, vy, 'bubble', 25))

        elif self.current_pattern == 14:

            if self.pattern_timer % 50 == 0:

                gap_x = self.box_x + 20 + random.random() * (self.box_w - 40)

                gap_width = 60

                tooth_size = 25

                num_teeth = int(self.box_w / tooth_size)

                for i in range(num_teeth):

                    x = self.box_x + i * tooth_size + tooth_size/2

                    if not (gap_x - gap_width/2 < x < gap_x + gap_width/2):

                        self.projectiles.append(Projectile(x, self.box_y, 0, 5, 'tooth', 25))

        elif self.current_pattern == 15:

            if self.pattern_timer == 0:

                for i in range(4):

                    x = self.box_x + self.box_w/2

                    y = self.box_y + self.box_h/2

                    angle = (i / 4) * math.pi * 2 + math.pi/4

                    speed = 4

                    vx = math.cos(angle) * speed

                    vy = math.sin(angle) * speed

                    def bounce_accel_update(p, bx, by, bw, bh):

                        p.x += p.vx

                        p.y += p.vy

                        if p.x <= bx or p.x + p.size >= bx + bw: p.vx *= -1

                        if p.y <= by or p.y + p.size >= by + bh: p.vy *= -1

                        p.rotation += 10

                        p.vx *= 1.001

                        p.vy *= 1.001

                    self.projectiles.append(Projectile(x, y, vx, vy, 'wave', 30, update_func=bounce_accel_update))

            if self.pattern_timer % 60 == 0:

                 x = self.box_x + random.random() * self.box_w

                 y = self.box_y + random.random() * self.box_h

                 vx = 3 if random.random() > 0.5 else -3

                 vy = 3 if random.random() > 0.5 else -3

                 def bounce_update(p, bx, by, bw, bh):

                    p.x += p.vx

                    p.y += p.vy

                    if p.x <= bx or p.x + p.size >= bx + bw: p.vx *= -1

                    if p.y <= by or p.y + p.size >= by + bh: p.vy *= -1

                    p.rotation += 5

                 self.projectiles.append(Projectile(x, y, vx, vy, 'wave', 30, update_func=bounce_update))

        elif self.current_pattern == 16:

            if self.pattern_timer % 5 == 0:

                edge = random.randint(0, 3)

                if edge == 0: 

                    x = self.box_x + random.random() * self.box_w

                    y = self.box_y

                elif edge == 1: 

                    x = self.box_x + self.box_w

                    y = self.box_y + random.random() * self.box_h

                elif edge == 2: 

                    x = self.box_x + random.random() * self.box_w

                    y = self.box_y + self.box_h

                else: 

                    x = self.box_x

                    y = self.box_y + random.random() * self.box_h

                center_x = self.box_x + self.box_w / 2

                center_y = self.box_y + self.box_h / 2

                dx = center_x - x

                dy = center_y - y

                mag = (dx**2 + dy**2)**0.5

                speed = 3 + (self.pattern_timer / 100) 

                vx = (dx/mag) * speed

                vy = (dy/mag) * speed

                self.projectiles.append(Projectile(x, y, vx, vy, 'tooth', 20))

    def update(self):

        """Update the boss battle state"""

        import math

        if self.char_index < len(self.full_message):

            self.type_timer += 1

            if self.type_timer >= 2:  

                self.type_timer = 0

                self.display_message += self.full_message[self.char_index]

                self.char_index += 1

        if self.soul.invincible_frames > 0:

            self.soul.invincible_frames -= 1

        if self.orca.hurt_frames > 0:

            self.orca.hurt_frames -= 1

        self.orca.update()

        if self.message_timer > 0:

            self.message_timer -= 1

        dx = 0

        dy = 0

        if self.keys_held['a'] or self.keys_held['left']:

            dx -= 1

        if self.keys_held['d'] or self.keys_held['right']:

            dx += 1

        if self.keys_held['w'] or self.keys_held['up']:

            dy -= 1

        if self.keys_held['s'] or self.keys_held['down']:

            dy += 1

        if dx != 0 or dy != 0:

            if dx != 0 and dy != 0:

                dx *= 0.707

                dy *= 0.707

            self.soul.move(dx, dy)

        if self.phase == 'fight_minigame':

            self.fight_bar_pos += self.fight_bar_speed * self.fight_bar_dir

            if self.fight_bar_pos > self.box_w / 2 or self.fight_bar_pos < -self.box_w / 2:

                self.fight_bar_dir *= -1

        elif self.phase == 'dodging':

            self.turn_timer -= 1

            self.pattern_timer += 1

            self.spawn_attack_pattern()

            for proj in self.projectiles:

                proj.update(self.box_x, self.box_y, self.box_w, self.box_h)

                if proj.collides_with(self.soul) and self.soul.invincible_frames == 0:

                    self.player_hp -= 1

                    self.soul.invincible_frames = 60

                    self.set_message('Ouch!', 30)

                    proj.active = False

            self.projectiles = [p for p in self.projectiles 

                               if p.active and (p.update_func or p.is_in_bounds(self.box_x, self.box_y, self.box_w, self.box_h))]

            if self.turn_timer <= 0:

                self.phase = 'player_turn'

                self.set_box_shape('rectangle')

                self.projectiles = []

                self.set_message('Your turn!', 60)

            if self.player_hp <= 0:

                self.phase = 'defeat'

                self.set_message('You were caught...', 180)

        elif self.phase == 'attacking':

            self.turn_timer -= 1

            if self.turn_timer <= 0:

                if self.orca.is_defeated():

                    self.phase = 'victory'

                    self.set_message('You scared off the orca!' if not self.orca.spared else 'The orca left peacefully.', 180)

                else:

                    pattern = random.randint(0, 16)

                    self.start_attack_phase(pattern)

    def handle_key_press(self, key):

        """Handle a key being pressed"""

        key_lower = key.lower() if isinstance(key, str) else key

        if key_lower in self.keys_held:

            self.keys_held[key_lower] = True

        if self.phase == 'player_turn':

            if key_lower in ['a', 'left']:

                self.menu_selection = (self.menu_selection - 1) % 4

            elif key_lower in ['d', 'right']:

                self.menu_selection = (self.menu_selection + 1) % 4

            elif key_lower in ['z', 'enter', 'space']:

                self.select_menu_option()

        elif self.phase in ['act_menu', 'item_menu', 'mercy_menu', 'enemy_select_menu']:

            if self.phase == 'item_menu':

                limit = len(self.inventory) - 1

                if key_lower in ['w', 'up']:

                    if self.submenu_selection >= 2:

                        self.submenu_selection -= 2

                elif key_lower in ['s', 'down']:

                    if self.submenu_selection + 2 <= limit:

                        self.submenu_selection += 2

                elif key_lower in ['a', 'left']:

                    if self.submenu_selection > 0:

                        self.submenu_selection -= 1

                elif key_lower in ['d', 'right']:

                    if self.submenu_selection < limit:

                        self.submenu_selection += 1

            else:

                if key_lower in ['w', 'up']:

                    self.submenu_selection = max(0, self.submenu_selection - 1)

                elif key_lower in ['s', 'down']:

                    limit = 0

                    if self.phase == 'act_menu': limit = 2

                    elif self.phase == 'mercy_menu': limit = 1

                    elif self.phase == 'enemy_select_menu': limit = 0

                    self.submenu_selection = min(limit, self.submenu_selection + 1)

            if key_lower in ['z', 'enter', 'space']:

                self.execute_submenu_action()

            elif key_lower in ['x', 'backspace', 'escape']:

                self.phase = 'player_turn'

                self.set_box_shape('rectangle')

        elif self.phase == 'fight_minigame':

            if key_lower in ['z', 'enter', 'space']:

                self.execute_attack()

    def handle_key_release(self, key):

        """Handle a key being released"""

        key_lower = key.lower() if isinstance(key, str) else key

        if key_lower in self.keys_held:

            self.keys_held[key_lower] = False

    def select_menu_option(self):

        """Select the current menu option"""

        self.submenu_selection = 0

        self.set_box_shape('rectangle')

        if self.menu_selection == 0:  

            self.phase = 'enemy_select_menu'

        elif self.menu_selection == 1:  

            self.phase = 'enemy_select_menu'

        elif self.menu_selection == 2:  

            if not self.inventory:

                self.set_message('Inventory empty!', 60)

            else:

                self.phase = 'item_menu'

                self.set_message('Choose an item.', 60)

        elif self.menu_selection == 3:  

            self.phase = 'enemy_select_menu'

    def execute_attack(self):

        """Calculate damage based on timing"""

        dist = abs(self.fight_bar_pos)

        max_dist = self.box_w / 2

        accuracy = max(0, 1 - (dist / max_dist))

        base_damage = 10 + accuracy * 15

        lv_multiplier = 1 + (self.player_lv - 1) * 0.5

        damage = int(base_damage * lv_multiplier)

        if accuracy > 0.8: 

            damage += 5

            self.set_message('CRITICAL HIT!', 60)

        else:

            self.set_message(f'Hit for {damage}!', 60)

        self.orca.take_damage(damage)

        self.phase = 'attacking'

        self.turn_timer = 60

    def execute_submenu_action(self):

        """Execute action from submenu"""

        if self.phase == 'enemy_select_menu':

            if self.menu_selection == 0: 

                self.phase = 'fight_minigame'

                self.fight_bar_pos = -self.box_w / 2

                self.fight_bar_dir = 1

                self.set_message('Press Z when center!', 60)

            elif self.menu_selection == 1: 

                self.phase = 'act_menu'

                self.submenu_selection = 0

                self.set_message('What to do?', 60)

            elif self.menu_selection == 3: 

                self.phase = 'mercy_menu'

                self.submenu_selection = 0

                self.set_message('Spare or Flee?', 60)

        elif self.phase == 'act_menu':

            actions = ['Check', 'Plead', 'Play Dead']

            action = actions[self.submenu_selection]

            if action == 'Check':

                self.set_message(f'ORCA - ATK 10 DEF 5. Looks hungry.', 90)

                self.phase = 'attacking' 

                self.turn_timer = 90 

            elif action == 'Plead':

                self.set_message('You pleaded for your life...', 60)

                self.orca.mercy_meter += 25

                self.phase = 'attacking'

                self.turn_timer = 60

            elif action == 'Play Dead':

                self.set_message('You played dead. Orca is confused.', 60)

                self.orca.mercy_meter += 10

                self.phase = 'attacking'

                self.turn_timer = 60

        elif self.phase == 'item_menu':

            if self.submenu_selection < len(self.inventory):

                item = self.inventory.pop(self.submenu_selection)

                heal = item['heal']

                self.player_hp = min(self.player_max_hp, self.player_hp + heal)

                self.set_message(f"Used {item['name']}. Healed {heal} HP.", 60)

                self.phase = 'attacking'

                self.turn_timer = 60

        elif self.phase == 'mercy_menu':

            options = ['Spare', 'Flee']

            option = options[self.submenu_selection]

            if option == 'Spare':

                if self.orca.mercy_meter >= 100 or self.orca.health < 20:

                    self.orca.spared = True

                    self.phase = 'victory'

                    self.set_message('You spared the orca.', 180)

                else:

                    self.set_message("The orca won't listen yet.", 60)

                    self.phase = 'attacking'

                    self.turn_timer = 60

            elif option == 'Flee':

                if random.random() < 0.5:

                    self.phase = 'victory' 

                    self.set_message('You fled safely!', 180)

                else:

                    self.set_message("Couldn't escape!", 60)

                    self.phase = 'attacking'

                    self.turn_timer = 60

            else:

                self.set_message('No heals left!', 60)

    def handle_mouse_press(self, mx, my):

        """Handle mouse clicks on menu buttons"""

        if self.phase == 'player_turn':

            for i, x in enumerate(self.btn_positions):

                if (x - self.btn_w/2 < mx < x + self.btn_w/2 and

                    self.menu_y - self.btn_h/2 < my < self.menu_y + self.btn_h/2):

                    self.menu_selection = i

                    self.select_menu_option()

                    break

    def draw(self, app):

        """Draw the entire boss battle screen"""

        import math

        w, h = self.w, self.h

        if hasattr(app, 'battle_bg_image') and app.battle_bg_image:

            drawImage(app.battle_bg_image, 0, 0, width=w, height=h)

        else:

            drawRect(0, 0, w, h, fill='black')

        orca_x = w / 2

        orca_y = h * 0.3

        orca_size = min(w, h) * 0.6

        shake_x = 0

        if self.orca.hurt_frames > 0:

            shake_x = math.sin(self.orca.hurt_frames * 2) * 10

        if hasattr(app, 'orca_battle_image') and app.orca_battle_image:

            drawImage(app.orca_battle_image, orca_x + shake_x, orca_y, 

                     width=orca_size, height=orca_size * 0.7, align='center')

        else:

            drawOval(orca_x + shake_x, orca_y, orca_size, orca_size * 0.5, 

                    fill=rgb(30, 30, 40), border='white', borderWidth=2)

            drawOval(orca_x + shake_x - orca_size * 0.15, orca_y - orca_size * 0.05, 

                    orca_size * 0.3, orca_size * 0.2, fill='white')

            drawCircle(orca_x + shake_x + orca_size * 0.2, orca_y - orca_size * 0.08, 

                      orca_size * 0.05, fill='red' if self.orca.hurt_frames > 0 else 'white')

            drawPolygon(orca_x + shake_x, orca_y - orca_size * 0.25,

                       orca_x + shake_x - orca_size * 0.08, orca_y - orca_size * 0.05,

                       orca_x + shake_x + orca_size * 0.08, orca_y - orca_size * 0.05,

                       fill=rgb(30, 30, 40))

            if self.orca.mercy_meter >= 100 or self.orca.health < 20:

                drawLabel('SPAREABLE', orca_x, orca_y - orca_size * 0.4, size=16, fill='yellow', bold=True, font='Determination Sans')

        if self.orca.hurt_frames > 0 or self.orca.display_health > self.orca.health:

            bar_w = w * 0.4

            bar_h = h * 0.025

            bar_x = (w - bar_w) / 2

            bar_y = h * 0.15

            drawRect(bar_x, bar_y, bar_w, bar_h, fill=rgb(50, 50, 50), border='white', borderWidth=2)

            display_ratio = self.orca.display_health / self.orca.max_health

            if display_ratio > 0:

                drawRect(bar_x + 2, bar_y + 2, (bar_w - 4) * display_ratio, bar_h - 4, fill='red')

            hp_ratio = self.orca.health / self.orca.max_health

            if hp_ratio > 0:

                hp_color = rgb(50, 200, 50) if hp_ratio > 0.5 else rgb(200, 200, 50) if hp_ratio > 0.25 else rgb(200, 50, 50)

                drawRect(bar_x + 2, bar_y + 2, (bar_w - 4) * hp_ratio, bar_h - 4, fill=hp_color)

            damage_taken = int(self.orca.display_health - self.orca.health)

            if damage_taken > 0:

                drawLabel(str(int(damage_taken)), bar_x + bar_w/2, bar_y - 20, size=20, fill='red', bold=True, font='Determination Sans')

        if self.phase != 'dodging':

            if hasattr(app, 'battle_box_image') and app.battle_box_image:

                drawImage(app.battle_box_image, self.menu_x, self.menu_y_pos, width=self.menu_w, height=self.menu_h)

            else:

                drawRect(self.menu_x, self.menu_y_pos, self.menu_w, self.menu_h, 

                        fill='black', border='white', borderWidth=5)

        if self.phase == 'dodging':

            if hasattr(app, 'battle_box_image') and app.battle_box_image:

                drawImage(app.battle_box_image, self.attack_x, self.attack_y, width=self.attack_w, height=self.attack_h)

            else:

                drawRect(self.attack_x, self.attack_y, self.attack_w, self.attack_h, 

                        fill='black', border='white', borderWidth=5)

        if self.phase == 'fight_minigame':

            center_x = self.box_x + self.box_w / 2

            if hasattr(app, 'fight_target_image') and app.fight_target_image:

                target_w = self.box_w * 0.9

                target_h = self.box_h * 0.8

                drawImage(app.fight_target_image, center_x, self.box_y + self.box_h/2, 

                         width=target_w, height=target_h, align='center')

            else:

                drawOval(center_x, self.box_y + self.box_h/2, self.box_w * 0.8, self.box_h * 0.6, 

                        fill=None, border='gray', borderWidth=3)

                drawRect(center_x - 5, self.box_y + 10, 10, self.box_h - 20, fill='red', opacity=50)

                drawRect(center_x - 30, self.box_y + 10, 60, self.box_h - 20, fill='orange', opacity=30)

            bar_x = center_x + self.fight_bar_pos

            if hasattr(app, 'fight_bar_image') and app.fight_bar_image:

                drawImage(app.fight_bar_image, bar_x, self.box_y + self.box_h/2, 

                         width=16, height=self.box_h * 0.9, align='center')

            else:

                drawRect(bar_x - 4, self.box_y + 10, 8, self.box_h - 20, fill='white', border='black', borderWidth=1)

        elif self.phase in ['act_menu', 'item_menu', 'mercy_menu', 'enemy_select_menu']:

            text_x = self.box_x + 60

            text_y = self.box_y + 40

            line_h = 45

            if self.phase == 'item_menu':

                if not self.inventory:

                    drawLabel('* (Empty)', text_x, text_y, size=32, fill='white', align='left', font='Determination Sans')

                    self.soul.x = text_x - 25

                    self.soul.y = text_y

                    self.soul.draw(app.soul_image if hasattr(app, 'soul_image') else None)

                else:

                    page_size = 8

                    current_page = self.submenu_selection // page_size

                    start_index = current_page * page_size

                    end_index = min(start_index + page_size, len(self.inventory))

                    for i in range(start_index, end_index):

                        item = self.inventory[i]

                        option = f'* {item["name"]}'

                        page_rel_index = i - start_index

                        row = page_rel_index // 2

                        col = page_rel_index % 2

                        x = text_x + col * 240

                        y = text_y + row * line_h

                        color = 'yellow' if i == self.submenu_selection else 'white'

                        drawLabel(option, x, y, size=32, fill=color, align='left', font='Determination Sans')

                        if i == self.submenu_selection:

                            self.soul.x = x - 25

                            self.soul.y = y

                            self.soul.draw(app.soul_image if hasattr(app, 'soul_image') else None)

                    page_text = f"PAGE {current_page + 1}"

                    drawLabel(page_text, self.box_x + self.box_w - 120, self.box_y + self.box_h - 30, size=24, fill='white', align='center', font='Determination Sans')

            else:

                options = []

                if self.phase == 'enemy_select_menu':

                    options = ['* Orca']

                elif self.phase == 'act_menu':

                    options = ['* Check', '* Plead', '* Play Dead']

                elif self.phase == 'mercy_menu':

                    options = ['* Spare', '* Flee']

                for i, option in enumerate(options):

                    color = 'yellow' if i == self.submenu_selection else 'white'

                    drawLabel(option, text_x, text_y + i * line_h, size=32, fill=color, align='left', font='Determination Sans')

                    if i == self.submenu_selection:

                        self.soul.x = text_x - 25

                        self.soul.y = text_y + i * line_h

                        self.soul.draw(app.soul_image if hasattr(app, 'soul_image') else None)

                    if self.phase == 'enemy_select_menu' and self.menu_selection == 0:

                        bar_x = text_x + 140

                        bar_y = text_y + i * line_h

                        bar_w = 100

                        bar_h = 15

                        drawRect(bar_x, bar_y - bar_h/2, bar_w, bar_h, fill='red')

                        hp_ratio = self.orca.health / self.orca.max_health

                        if hp_ratio > 0:

                            drawRect(bar_x, bar_y - bar_h/2, bar_w * hp_ratio, bar_h, fill='lightGreen')

        elif self.phase in ['player_turn', 'attacking']:

            text_x = self.box_x + 30

            text_y = self.box_y + 30

            msg = self.display_message

            if msg and not msg.startswith('*') and msg.strip() != '':

                msg = '* ' + msg

            drawLabel(msg, text_x, text_y, size=24, fill='white', align='left', font='Determination Mono')

        elif self.phase == 'dodging':

            proj_images = {}

            if hasattr(app, 'proj_bone_image'):

                proj_images['bone'] = app.proj_bone_image

            if hasattr(app, 'proj_bubble_image'):

                proj_images['bubble'] = app.proj_bubble_image

            if hasattr(app, 'proj_tooth_image'):

                proj_images['tooth'] = app.proj_tooth_image

            if hasattr(app, 'proj_wave_image'):

                proj_images['wave'] = app.proj_wave_image

            if hasattr(app, 'blaster_warning_image'):

                proj_images['warning'] = app.blaster_warning_image

            for proj in self.projectiles:

                proj.draw(proj_images)

            soul_image = app.soul_image if hasattr(app, 'soul_image') else None

            self.soul.draw(soul_image)

        hp_display_y = h * 0.87

        hp_text_size = int(min(w, h) * 0.022)

        name_w = 80

        lv_w = 60

        hp_label_w = 30 

        bar_w = w * 0.15

        text_w = 60 

        total_w = name_w + lv_w + hp_label_w + bar_w + text_w + 40 

        start_x = (w - total_w) / 2

        drawLabel('SEAL', start_x, hp_display_y, size=hp_text_size, fill='white', bold=True, font='Determination Sans', align='left')

        drawLabel(f'LV {self.player_lv}', start_x + name_w, hp_display_y, size=hp_text_size, fill='white', bold=True, font='Determination Sans', align='left')

        drawLabel(f'HP', start_x + name_w + lv_w, hp_display_y, size=hp_text_size, fill='white', bold=True, font='Determination Sans', align='left')

        player_bar_x = start_x + name_w + lv_w + hp_label_w + 10

        drawRect(player_bar_x, hp_display_y - h * 0.01, bar_w, h * 0.02, 

                fill=rgb(80, 0, 0), border='white', borderWidth=1)

        player_hp_ratio = self.player_hp / self.player_max_hp

        if player_hp_ratio > 0:

            drawRect(player_bar_x + 1, hp_display_y - h * 0.01 + 1, 

                    (bar_w - 2) * player_hp_ratio, h * 0.02 - 2, fill='yellow')

        drawLabel(f'{self.player_hp}/{self.player_max_hp}', player_bar_x + bar_w + 10, hp_display_y, 

                 size=hp_text_size, fill='white', font='Determination Sans', align='left')

        labels = ['FIGHT', 'ACT', 'ITEM', 'MERCY']

        btn_keys = ['fight', 'act', 'item', 'mercy']

        for i, label in enumerate(labels):

            x = self.btn_positions[i]

            selected = (self.phase == 'player_turn' and self.menu_selection == i)

            btn_key = btn_keys[i]

            custom_btn = None

            if selected and hasattr(app, 'battle_buttons_selected') and btn_key in app.battle_buttons_selected and app.battle_buttons_selected[btn_key]:

                custom_btn = app.battle_buttons_selected[btn_key]

            elif hasattr(app, 'battle_buttons') and btn_key in app.battle_buttons and app.battle_buttons[btn_key]:

                custom_btn = app.battle_buttons[btn_key]

            if custom_btn:

                drawImage(custom_btn, x, self.menu_y, width=self.btn_w, height=self.btn_h, align='center')

            else:

                if selected:

                    btn_color = 'black'

                    btn_border = 'yellow'

                    text_color = 'yellow'

                else:

                    btn_color = 'black'

                    btn_border = 'orange'

                    text_color = 'orange'

                drawRect(x, self.menu_y, self.btn_w, self.btn_h, 

                        fill=btn_color, border=btn_border, borderWidth=3, align='center')

                btn_text_size = int(min(w, h) * 0.025)

                drawLabel(label, x, self.menu_y, size=btn_text_size, 

                        fill=text_color, bold=True, font='Determination Sans')

            if selected:

                original_size = self.soul.size

                self.soul.size = 24

                self.soul.x = x - self.btn_w/2 + 25

                self.soul.y = self.menu_y

                self.soul.draw(app.soul_image if hasattr(app, 'soul_image') else None)

                self.soul.size = original_size 

        if self.phase == 'victory':

            text_x = self.menu_x + 30

            text_y = self.menu_y_pos + 50

            msg = '* YOU WON!'

            sub_msg = 'Press Z or Enter to continue.'

            if self.orca.spared:

                msg = '* You spared the orca.'

            else:

                msg = '* You defeated the orca! +50 EXP.'

            drawLabel(msg, text_x, text_y, size=20, fill='white', align='left', font='Determination Mono')

            drawLabel(sub_msg, text_x, text_y + 30, size=16, fill='yellow', align='left', font='Determination Mono')

        elif self.phase == 'defeat':

            drawRect(0, 0, w, h, fill='black', opacity=50)

            result_size = int(min(w, h) * 0.05)

            drawLabel('GAME OVER', w/2, h * 0.4, size=result_size, fill='red', bold=True, font='Determination Sans')

            hint_size = int(min(w, h) * 0.02)

            drawLabel('Press R to restart...', w/2, h * 0.5, size=hint_size, fill='white', font='Determination Sans')

def spawn_background_fish(app):

    app.floating_fish = []

    for _ in range(20):

        fish = FloatingFish(app.width, app.height)

        if app.fish_assets:

            weights = [20] * len(app.fish_assets)

            if len(app.fish_assets) >= 5:

                weights[4] = 5 

            fish.fish_type_index = random.choices(range(len(app.fish_assets)), weights=weights, k=1)[0]

        app.floating_fish.append(fish)

def unload_background_assets(app):

    """Clear background elements to improve performance during boss battle"""

    app.floating_fish = []

    app.bubbles = []

    app.light_particles = []

def reload_background_assets(app):

    """Restore background elements after boss battle"""

    spawn_background_fish(app)

    app.bubbles = [Bubble() for _ in range(12)]

    app.light_particles = [LightParticle() for _ in range(15)]

def onAppStart(app):

    app.stats = GameStats()

    app.actions = get_available_actions()

    app.buttons = []

    app.gameOver = False

    app.gameWon = False

    app.caught_by_orca = False

    app.event_message = ''

    app.event_timer = 0

    app.selected_action = None

    app.time = 0

    app.inventory = []

    app.inBossBattle = False

    app.orca_encounters_enabled = True 

    app.winning_enabled = True 

    app.bossBattle = None

    print("Loading custom images...")

    app.seal_image = try_load_image('seal.png')

    app.background_image = try_load_image('background.png')

    app.ice_image = try_load_image('ice.png')

    app.fish_assets = []

    fish_files = ['fish.png', 'fish2.png', 'fish3.png', 'fish4.png', 'miku_fish.png']

    for f in fish_files:

        name, ext = os.path.splitext(f)

        flipped_name = f"{name}_flipped{ext}"

        img = try_load_image(f)

        flipped_img = try_load_image(flipped_name)

        if img:

            app.fish_assets.append({

                'normal': img,

                'flipped': flipped_img if flipped_img else img 

            })

    if not app.fish_assets:

        app.fish_assets.append({'normal': None, 'flipped': None})

    app.button_image = try_load_image('button.png')

    app.button_hover_image = try_load_image('button_hover.png')

    app.victory_bg_image = try_load_image('victory_bg.png')

    app.gameover_bg_image = try_load_image('gameover_bg.png')

    app.orca_battle_image = try_load_image('orca_battle.png')

    app.soul_image = try_load_image('soul.png')

    app.proj_bone_image = try_load_image('proj_bone.png')

    app.proj_bubble_image = try_load_image('proj_bubble.png')

    app.proj_tooth_image = try_load_image('proj_tooth.png')

    app.proj_wave_image = try_load_image('proj_wave.png')

    app.blaster_warning_image = try_load_image('blaster_warning.png')

    app.battle_bg_image = try_load_image('battle_bg.png')

    app.battle_box_image = try_load_image('battle_box.png')

    app.fight_target_image = try_load_image('fight_target.png')

    app.fight_bar_image = try_load_image('fight_bar.png')

    app.battle_buttons = {}

    app.battle_buttons_selected = {}

    for btn_name in ['fight', 'act', 'item', 'mercy']:

        app.battle_buttons[btn_name] = try_load_image(f'ui_{btn_name}.png')

        app.battle_buttons_selected[btn_name] = try_load_image(f'ui_{btn_name}_selected.png')

    app.bubble_image = try_load_image('bubble.png')

    app.kelp_image = try_load_image('kelp.png')

    app.wave_image = try_load_image('wave.png')

    app.sparkle_image = try_load_image('sparkle.png')

    app.sleep_image = try_load_image('sleep.png')

    app.title_panel_image = try_load_image('title_panel.png')

    app.stats_panel_image = try_load_image('stats_panel.png')

    app.action_panel_image = try_load_image('action_panel.png')

    app.action_button_images = {}

    app.action_button_hover_images = {}

    action_names = ['hide', 'rest', 'forage', 'hunt', 'play', 'explore_nearby', 'explore_far', 'search']

    for action_name in action_names:

        btn_img = try_load_image(f'button_{action_name}.png')

        btn_hover_img = try_load_image(f'button_{action_name}_hover.png')

        if btn_img:

            app.action_button_images[action_name] = btn_img

            print(f"✓ button_{action_name}.png loaded")

        if btn_hover_img:

            app.action_button_hover_images[action_name] = btn_hover_img

            print(f"✓ button_{action_name}_hover.png loaded")

    app.stat_images = {

        'hunger': {},

        'health': {},

        'energy': {},

        'happiness': {}

    }

    for stat in ['hunger', 'health', 'energy', 'happiness']:

        for level in [0, 25, 50, 75, 100]:

            img = try_load_image(f'stat_{stat}_{level}.png')

            if img:

                app.stat_images[stat][level] = img

                print(f"✓ stat_{stat}_{level}.png loaded")

    app.inFishingMinigame = False

    app.fishingMinigame = None

    app.mode = 'survival' 

    app.tycoon = TycoonManager()

    app.tycoon_icons = {}

    app.tycoon_icons['bucket'] = try_load_image('tycoon_icon_bucket.png')

    app.tycoon_icons['penguin'] = try_load_image('tycoon_icon_penguin.png')

    app.tycoon_icons['platform'] = try_load_image('ice.png') 

    app.tycoon_icons['boat'] = try_load_image('tycoon_icon_boat.png')

    app.tycoon_icons['research'] = try_load_image('tycoon_icon_research.png')

    app.tycoon_icons['aquarium'] = try_load_image('tycoon_icon_aquarium.png')

    app.tycoon_icons['satellite'] = try_load_image('tycoon_icon_satellite.png')

    app.tycoon_icons['drone'] = try_load_image('tycoon_icon_drone.png')

    app.tycoon_icons['underwater_base'] = try_load_image('tycoon_icon_base.png')

    app.tycoon_icons['moon_colony'] = try_load_image('tycoon_icon_moon.png')

    app.upgrade_icon = try_load_image('tycoon_icon_upgrade.png')

    app.skill_icon = try_load_image('tycoon_icon_skill.png')

    app.pearl_icon = try_load_image('tycoon_icon_pearl.png')

    app.fishing_bg_image = try_load_image('fishing_bg.png')

    app.fishing_target_image = try_load_image('fishing_target.png')

    if app.seal_image:

        print("✓ seal.png loaded")

    else:

        print("✗ seal.png not found - using default graphics")

    if app.background_image:

        print("✓ background.png loaded")

    else:

        print("✗ background.png not found - using default gradient")

    if app.ice_image:

        print("✓ ice.png loaded")

    else:

        print("✗ ice.png not found - using default graphics")

    if app.fish_assets and app.fish_assets[0]['normal']:

        print(f"✓ {len(app.fish_assets)} fish variants loaded")

    else:

        print("✗ fish images not found - using default graphics")

    if app.button_image:

        print("✓ button.png loaded")

    else:

        print("✗ button.png not found - using default graphics")

    if app.victory_bg_image:

        print("✓ victory_bg.png loaded")

    else:

        print("✗ victory_bg.png not found - using default graphics")

    if app.gameover_bg_image:

        print("✓ gameover_bg.png loaded")

    else:

        print("✗ gameover_bg.png not found - using default graphics")

    if app.bubble_image:

        print("✓ bubble.png loaded")

    if app.kelp_image:

        print("✓ kelp.png loaded")

    if app.wave_image:

        print("✓ wave.png loaded")

    if app.sparkle_image:

        print("✓ sparkle.png loaded")

    if app.sleep_image:

        print("✓ sleep.png loaded")

    if app.title_panel_image:

        print("✓ title_panel.png loaded")

    if app.stats_panel_image:

        print("✓ stats_panel.png loaded")

    if app.action_panel_image:

        print("✓ action_panel.png loaded")

    spawn_background_fish(app)

    app.bubbles = [Bubble() for _ in range(12)]

    app.light_particles = [LightParticle() for _ in range(15)]

    app.particles = []

    setup_buttons(app)

def setup_buttons(app):

    """Setup action buttons with responsive layout"""

    app.buttons = []

    button_area_top_pct = 0.65

    button_width_pct = 0.22

    button_height_pct = 0.065

    cols = 4

    rows = (len(app.actions) + cols - 1) // cols

    spacing_x_pct = 0.04

    spacing_y_pct = 0.02

    total_width_pct = cols * button_width_pct + (cols - 1) * spacing_x_pct

    start_x_pct = (1 - total_width_pct) / 2 + button_width_pct / 2

    for i, action in enumerate(app.actions):

        col = i % cols

        row = i // cols

        x_pct = start_x_pct + col * (button_width_pct + spacing_x_pct)

        y_pct = button_area_top_pct + row * (button_height_pct + spacing_y_pct)

        action_image_map = {

            'HIDE': 'hide',

            'REST': 'rest',

            'FORAGE': 'forage',

            'HUNT': 'hunt',

            'PLAY': 'play',

            'EXPLORE': 'explore_nearby',

            'VENTURE': 'explore_far',

            'SEARCH': 'search'

        }

        action_key = action_image_map.get(action.name, None)

        custom_img = app.action_button_images.get(action_key) if action_key else None

        custom_hover_img = app.action_button_hover_images.get(action_key) if action_key else None

        button = Button(x_pct, y_pct, button_width_pct, button_height_pct, action.name, action, 

                       custom_img, custom_hover_img)

        app.buttons.append(button)

def process_action(app, action):

    """Process the selected action for the day"""

    if action.name in ['HUNT', 'FORAGE'] and random.random() < 0.15: 

        app.inFishingMinigame = True

        app.fishingMinigame = FishingMinigame(app.width, app.height, app.fish_assets)

        app.pending_action = action 

        return

    for stat, change in action.effects.items():

        current = getattr(app.stats, stat)

        limit = app.stats.max_health if stat == 'health' else 100

        setattr(app.stats, stat, max(0, min(limit, current + change)))

    app.stats.visibility = max(0, min(100, app.stats.visibility + action.visibility_change))

    if app.winning_enabled and check_mother_found(app.stats, action):

        app.gameWon = True

        app.event_message = '[VICTORY] You found your mother! You are safe!'

        app.event_timer = 300

        return

    if app.orca_encounters_enabled and check_orca_encounter(app.stats, action):

        app.inBossBattle = True

        unload_background_assets(app) 

        app.bossBattle = BossBattle(app.width, app.height)

        hp = 20 + (app.stats.lv - 1) * 5

        app.bossBattle.player_hp = hp

        app.bossBattle.player_max_hp = hp

        app.bossBattle.player_lv = app.stats.lv

        app.bossBattle.inventory.extend(app.inventory)

        app.event_message = '[DANGER] An orca spotted you! Prepare to fight!'

        app.event_timer = 120

        return

    if action.name in ['FORAGE', 'HUNT', 'EXPLORE', 'VENTURE', 'SEARCH']:

        if random.random() < 0.35: 

            item_pool = [

                {'name': 'Fatty Fish', 'heal': 10, 'desc': 'Heals 10 HP'},

                {'name': 'Kelp', 'heal': 5, 'desc': 'Heals 5 HP'},

                {'name': 'Ice Chunk', 'heal': 2, 'desc': 'Heals 2 HP'}

            ]

            new_item = random.choice(item_pool)

            app.inventory.append(new_item)

            msg = f"Found {new_item['name']}!"

            if app.event_message and not app.event_message.startswith('Day'):

                app.event_message += f" + {msg}"

            else:

                app.event_message = msg

                app.event_timer = 100

    event = get_random_event()

    if event:

        msg, effects = event

        app.event_message = msg

        app.event_timer = 100

        for stat, change in effects.items():

            current = getattr(app.stats, stat)

            setattr(app.stats, stat, max(0, min(100, current + change)))

    else:

        app.event_message = f'Day {app.stats.day}: {action.description}'

        app.event_timer = 60

    app.stats.daily_decay()

    app.stats.increase_threats()

    if not app.stats.is_alive():

        app.gameOver = True

        return

    app.stats.day += 1

    app.stats.age_days += 1

def onStep(app):

    app.time += 1

    if hasattr(app, 'tycoon'):

        app.tycoon.update()

    if hasattr(app, 'mode') and app.mode == 'tycoon':

        return

    if app.inBossBattle and app.bossBattle:

        app.bossBattle.update()

        app.bossBattle.update_dimensions(app.width, app.height)

        app.bossBattle.soul.update_box(

            app.bossBattle.box_x, app.bossBattle.box_y,

            app.bossBattle.box_w, app.bossBattle.box_h

        )

        if app.bossBattle.phase == 'victory':

            pass 

        elif app.bossBattle.phase == 'defeat':

            if app.bossBattle.message_timer <= 0:

                app.inBossBattle = False

                reload_background_assets(app) 

                app.bossBattle = None

                app.gameOver = True

                app.caught_by_orca = True

        return

    if app.event_timer > 0:

        app.event_timer -= 1

    if app.inFishingMinigame and app.fishingMinigame:

        app.fishingMinigame.update()

        if not app.fishingMinigame.active and app.fishingMinigame.message_timer <= 0:

            if app.fishingMinigame.result == 'caught':

                reward_food = app.fishingMinigame.food_reward

                reward_exp = app.fishingMinigame.exp_reward

                app.stats.hunger = min(100, app.stats.hunger + reward_food)

                app.stats.gain_exp(reward_exp)

                app.event_message = f"Caught {app.fishingMinigame.fish_name}! +{reward_food} Food +{reward_exp} EXP"

            else:

                app.event_message = "The fish got away..."

            if hasattr(app, 'pending_action'):

                for stat, change in app.pending_action.effects.items():

                    current = getattr(app.stats, stat)

                    limit = app.stats.max_health if stat == 'health' else 100

                    setattr(app.stats, stat, max(0, min(limit, current + change)))

                app.stats.visibility = max(0, min(100, app.stats.visibility + app.pending_action.visibility_change))

                app.stats.daily_decay()

                app.stats.increase_threats()

                app.stats.day += 1

                app.stats.age_days += 1

                del app.pending_action

            app.event_timer = 60

            app.inFishingMinigame = False

            app.fishingMinigame = None

        return

    for button in app.buttons:

        button.x = button.x_pct * app.width

        button.y = button.y_pct * app.height

        button.width = button.width_pct * app.width

        button.height = button.height_pct * app.height

    for fish in app.floating_fish:

        fish.move(app.time)

    for bubble in app.bubbles:

        bubble.move()

    for particle in app.light_particles:

        particle.move()

def onMouseMove(app, mouseX, mouseY):

    if app.inBossBattle:

        return  

    for button in app.buttons:

        button.hovered = button.is_clicked(mouseX, mouseY)

def onMousePress(app, mouseX, mouseY):

    if hasattr(app, 'mode') and app.mode == 'tycoon':

        if mouseX > app.width - 40:

            panel_y = app.height * 0.55

            tab_h = 50

            content_y = panel_y + tab_h

            content_h = app.height - content_y

            if mouseY > content_y:

                relative_y = mouseY - content_y

                pct = relative_y / content_h

                target_scroll = pct * app.tycoon.max_scroll

                app.tycoon.scroll_y = max(0, min(app.tycoon.max_scroll, target_scroll))

                return

        if mouseX > app.width - 160 and mouseX < app.width - 10 and mouseY > 10 and mouseY < 50:

            app.mode = 'survival'

            return

        ice_x, ice_y = app.width/2, app.height * 0.35

        dist = ((mouseX - ice_x)**2 + (mouseY - (ice_y - 50))**2)**0.5

        if dist < 120: 

            amount = app.tycoon.click()

            app.tycoon.add_particle(mouseX, mouseY, amount)

            return

        panel_y = app.height * 0.55

        tab_h = 50

        if panel_y < mouseY < panel_y + tab_h:

            tabs = ['BUILD', 'UPGRADE', 'SKILLS', 'REBIRTH']

            tab_w = app.width / len(tabs)

            idx = int(mouseX // tab_w)

            if 0 <= idx < len(tabs):

                app.tycoon.current_tab = tabs[idx]

                app.tycoon.scroll_y = 0 

            return

        content_y = panel_y + tab_h

        if mouseY > content_y:

            if app.tycoon.current_tab == 'REBIRTH':

                center_y = content_y + (app.height - content_y) / 2

                btn_y = center_y + 100

                btn_w = 200

                btn_h = 60

                if (app.width/2 - btn_w/2 < mouseX < app.width/2 + btn_w/2 and

                    btn_y - btn_h/2 < mouseY < btn_y + btn_h/2):

                    gained = app.tycoon.rebirth()

                    if gained:

                        app.tycoon.add_particle(mouseX, mouseY, f"REBIRTH! +{gained} PEARLS")

                return

            start_y = content_y + 10 - app.tycoon.scroll_y

            item_h = 80

            keys = []

            if app.tycoon.current_tab == 'BUILD':

                keys = list(app.tycoon.buildings.keys())

            elif app.tycoon.current_tab == 'UPGRADE':

                keys = list(app.tycoon.upgrades.keys())

            elif app.tycoon.current_tab == 'SKILLS':

                keys = list(app.tycoon.skills.keys())

            for i, key in enumerate(keys):

                y_pos = start_y + i * (item_h + 10)

                if y_pos < content_y: continue 

                if y_pos > app.height: break 

                if y_pos < mouseY < y_pos + item_h:

                    if mouseX > app.width - 180:

                        success = False

                        if app.tycoon.current_tab == 'BUILD':

                            success = app.tycoon.buy_building(key)

                        elif app.tycoon.current_tab == 'UPGRADE':

                            success = app.tycoon.buy_upgrade(key)

                        elif app.tycoon.current_tab == 'SKILLS':

                            success = app.tycoon.buy_skill(key)

                        if success:

                            app.tycoon.add_particle(mouseX, mouseY, "BOUGHT!")

                        else:

                            app.tycoon.add_particle(mouseX, mouseY, "NO FUNDS")

            return

        return

    if app.inFishingMinigame and app.fishingMinigame:

        app.fishingMinigame.handle_mouse_press(mouseX, mouseY)

        return

    if app.inBossBattle and app.bossBattle:

        app.bossBattle.handle_mouse_press(mouseX, mouseY)

        return

    if app.gameOver or app.gameWon:

        btn_w = app.width * 0.25

        btn_h = app.height * 0.055

        btn_y = app.height * 0.7

        btn_x = app.width / 2

        if (btn_x - btn_w/2 < mouseX < btn_x + btn_w/2 and 

            btn_y - btn_h/2 < mouseY < btn_y + btn_h/2):

            onAppStart(app)

        return

    title_y = app.height * 0.033

    dlc_btn_x = app.width * 0.9

    dlc_btn_y = title_y

    dlc_btn_w = app.width * 0.15

    dlc_btn_h = app.height * 0.055 * 0.8

    if (dlc_btn_x - dlc_btn_w/2 < mouseX < dlc_btn_x + dlc_btn_w/2 and

        dlc_btn_y - dlc_btn_h/2 < mouseY < dlc_btn_y + dlc_btn_h/2):

        app.mode = 'tycoon'

        return

    for button in app.buttons:

        if button.is_clicked(mouseX, mouseY):

            process_action(app, button.action)

            break

def onKeyHold(app, keys):

    if hasattr(app, 'mode') and app.mode == 'tycoon':

        if 'up' in keys:

            app.tycoon.scroll_y = max(0, app.tycoon.scroll_y - 15)

        if 'down' in keys:

            app.tycoon.scroll_y = min(app.tycoon.max_scroll, app.tycoon.scroll_y + 15)

def onMouseDrag(app, mouseX, mouseY):

    if hasattr(app, 'mode') and app.mode == 'tycoon':

        if mouseX > app.width - 40:

            panel_y = app.height * 0.55

            tab_h = 50

            content_y = panel_y + tab_h

            content_h = app.height - content_y

            if mouseY > content_y:

                relative_y = mouseY - content_y

                pct = relative_y / content_h

                target_scroll = pct * app.tycoon.max_scroll

                app.tycoon.scroll_y = max(0, min(app.tycoon.max_scroll, target_scroll))

def onMouseScroll(app, mouseX, mouseY, scrollAmount):

    if hasattr(app, 'mode') and app.mode == 'tycoon':

        scroll_speed = 30

        app.tycoon.scroll_y -= scrollAmount * scroll_speed

        app.tycoon.scroll_y = max(0, min(app.tycoon.max_scroll, app.tycoon.scroll_y))

def onKeyPress(app, key):

    if hasattr(app, 'mode') and app.mode == 'tycoon':

        if key == 'up':

            app.tycoon.scroll_y = max(0, app.tycoon.scroll_y - 40)

        elif key == 'down':

            app.tycoon.scroll_y = min(app.tycoon.max_scroll, app.tycoon.scroll_y + 40)

        return

    if app.inFishingMinigame and app.fishingMinigame:

        app.fishingMinigame.handle_key_press(key)

        return

    if app.inBossBattle and app.bossBattle:

        key_lower = key.lower() if isinstance(key, str) else key

        if app.bossBattle.phase == 'victory':

            if key_lower in ['z', 'enter', 'x']:

                msg = ""

                if not app.bossBattle.orca.spared:

                    leveled_up = app.stats.gain_exp(50)

                    msg = "Defeated Orca! +50 EXP."

                    if leveled_up:

                        msg += " Level Up!"

                else:

                    msg = "You spared the orca."

                app.inBossBattle = False

                reload_background_assets(app) 

                app.bossBattle = None

                app.event_message = msg

                app.event_timer = 120

                app.stats.orca_threat = max(10, app.stats.orca_threat - 20)

            return

        elif app.bossBattle.phase == 'defeat':

             if key_lower in ['z', 'enter', 'x', 'r']:

                 app.inBossBattle = False

                 reload_background_assets(app) 

                 app.bossBattle = None

                 app.gameOver = True

                 app.caught_by_orca = True

             return

        else:

            app.bossBattle.handle_key_press(key)

        return

    if key == 'r' and (app.gameOver or app.gameWon):

        onAppStart(app)

    if key == 'f':

        spawn_background_fish(app)

        app.event_message = "Fish respawned!"

        app.event_timer = 30

    if key == 'o':

        app.orca_encounters_enabled = not app.orca_encounters_enabled

        status = "ENABLED" if app.orca_encounters_enabled else "DISABLED"

        app.event_message = f"Orca encounters {status}"

        app.event_timer = 60

    if key == 'm':

        app.winning_enabled = not app.winning_enabled

        status = "ENABLED" if app.winning_enabled else "DISABLED"

        app.event_message = f"Winning (Mother) {status}"

        app.event_timer = 60

    if key == 'b' and not app.inBossBattle and not app.gameOver and not app.gameWon:

        app.inBossBattle = True

        unload_background_assets(app) 

        app.bossBattle = BossBattle(app.width, app.height)

        hp = 20 + (app.stats.lv - 1) * 5

        app.bossBattle.player_hp = hp

        app.bossBattle.player_max_hp = hp

        app.bossBattle.player_lv = app.stats.lv

        app.bossBattle.inventory.extend(app.inventory)

        app.event_message = '[DEBUG] Boss fight triggered!'

        app.event_timer = 120

    if key == 'g' and not app.inBossBattle and not app.inFishingMinigame and not app.gameOver and not app.gameWon:

        app.inFishingMinigame = True

        app.fishingMinigame = FishingMinigame(app.width, app.height, app.fish_assets)

        app.event_message = '[DEBUG] Fishing Minigame triggered!'

        app.event_timer = 60

def onKeyRelease(app, key):

    """Handle key release for boss battle movement"""

    if app.inBossBattle and app.bossBattle:

        app.bossBattle.handle_key_release(key)

def draw_stat_bar(x, y, width, height, value, max_value, label, color_good, color_bad, app_w, app_h, stat_image=None):

    """Draw a stat bar - fully custom image if available, otherwise default graphics"""

    if stat_image:

        drawImage(stat_image, x, y, width=width, height=height, align='left-top')

        label_size = int(min(app_w, app_h) * 0.016)

        drawLabel(f'{label}: {int(value)}', x + width/2 + 1, y + height/2 + 1, 

                 size=label_size, bold=True, fill='black', font='BoldPixels')

        drawLabel(f'{label}: {int(value)}', x + width/2, y + height/2, 

                 size=label_size, bold=True, fill='white', font='BoldPixels')

    else:

        shadow_offset = min(app_w, app_h) * 0.003

        drawRect(x + shadow_offset, y + shadow_offset, width, height, fill='black', opacity=30)

        border_w = int(min(app_w, app_h) * 0.003)

        drawRect(x, y, width, height, fill=rgb(40, 40, 40), border='white', borderWidth=border_w)

        bar_width = (value / max_value) * (width - border_w * 2)

        if bar_width > 0:

            ratio = value / max_value

            r = int(color_bad[0] * (1-ratio) + color_good[0] * ratio)

            g = int(color_bad[1] * (1-ratio) + color_good[1] * ratio)

            b = int(color_bad[2] * (1-ratio) + color_good[2] * ratio)

            drawRect(x + border_w, y, bar_width, height - border_w * 2, fill=rgb(r, g, b))

            drawRect(x + border_w, y - height * 0.25, bar_width * 0.9, height * 0.3,

                    fill='white', opacity=25)

        import math

        if value < 25:

            pulse = abs(math.sin(app_w / 50)) * 30

            drawRect(x, y, width, height, fill='red', opacity=pulse, border='red', borderWidth=border_w)

        if value > 75:

            indicator = '+++'

            ind_color = 'lightGreen'

        elif value > 50:

            indicator = '++'

            ind_color = 'yellow'

        elif value > 25:

            indicator = '+'

            ind_color = 'orange'

        else:

            indicator = '!'

            ind_color = 'red'

        ind_size = int(min(app_w, app_h) * 0.014)

        drawLabel(indicator, x + width - min(app_w, app_h) * 0.025, y + height/2, size=ind_size, bold=True, fill=ind_color, font='BoldPixels')

        label_size = int(min(app_w, app_h) * 0.016)

        drawLabel(f'{label}: {int(value)}', x + width/2 + 1, y + height/2 + 1, 

                 size=label_size, bold=True, fill='black', font='BoldPixels')

        drawLabel(f'{label}: {int(value)}', x + width/2, y + height/2, 

                 size=label_size, bold=True, fill='white', font='BoldPixels')

def draw_tycoon_mode(app):

    w, h = app.width, app.height

    if app.background_image:

        drawImage(app.background_image, 0, 0, width=w, height=h)

    else:

        drawRect(0, 0, w, h, fill=rgb(80, 160, 220))

    drawRect(0, 0, w, h * 0.12, fill='black', opacity=60)

    coin_icon = app.fish_assets[0]['normal'] if app.fish_assets else None

    if coin_icon:

        drawImage(coin_icon, 20, 20, width=50, height=30)

    else:

        drawOval(45, 35, 50, 30, fill='orange')

    drawLabel(f"{int(app.tycoon.fish_coins):,} Fish Coins", 80, 35, size=30, fill='gold', align='left', bold=True, font='Determination Mono')

    drawLabel(f"Income: {app.tycoon.auto_income:.1f} / sec", 80, 70, size=20, fill='lightGreen', align='left', font='Determination Sans')

    if app.pearl_icon:

        drawImage(app.pearl_icon, w - 180, 60, width=30, height=30)

    else:

        drawCircle(w - 165, 75, 15, fill='pink', border='white')

    drawLabel(f"{app.tycoon.pearls} Pearls", w - 140, 75, size=20, fill='pink', align='left', bold=True, font='Determination Sans')

    ice_x, ice_y = w/2, h * 0.35

    ice_w, ice_h = w * 0.6, h * 0.15

    if app.ice_image:

        drawImage(app.ice_image, ice_x, ice_y, width=ice_w, height=ice_h, align='center')

    else:

        drawOval(ice_x, ice_y, ice_w, ice_h, fill='white', opacity=80)

    seal_size = 200

    import math

    bounce = math.sin(app.time / 10) * 10

    if app.seal_image:

        drawImage(app.seal_image, ice_x, ice_y - 50 + bounce, width=seal_size, height=seal_size, align='center')

    else:

        drawCircle(ice_x, ice_y - 50 + bounce, 80, fill='gray')

    drawLabel("CLICK ME!", ice_x, ice_y + 80, size=20, fill='white', opacity=50 + math.sin(app.time/5)*30, font='Determination Mono')

    for p in app.tycoon.click_particles:

        drawLabel(p['text'], p['x'], p['y'], size=24, fill=p['color'], bold=True, font='Determination Sans')

    panel_y = h * 0.55

    drawRect(0, panel_y, w, h - panel_y, fill='black', opacity=85)

    tabs = ['BUILD', 'UPGRADE', 'SKILLS', 'REBIRTH']

    tab_w = w / len(tabs)

    tab_h = 50

    for i, tab in enumerate(tabs):

        x = i * tab_w

        is_active = (app.tycoon.current_tab == tab)

        color = rgb(60, 60, 80) if is_active else rgb(30, 30, 40)

        drawRect(x, panel_y, tab_w, tab_h, fill=color, border='white', borderWidth=1)

        drawLabel(tab, x + tab_w/2, panel_y + tab_h/2, size=20, fill='white' if is_active else 'gray', bold=True, font='Determination Mono')

    content_y = panel_y + tab_h

    content_h = h - content_y

    if app.tycoon.max_scroll > 0:

        bar_h = content_h * (content_h / (app.tycoon.max_scroll + content_h))

        bar_y = content_y + (app.tycoon.scroll_y / app.tycoon.max_scroll) * (content_h - bar_h)

        drawRect(w - 10, bar_y, 10, bar_h, fill='gray', opacity=50)

    start_y = content_y + 10 - app.tycoon.scroll_y

    item_h = 80

    if app.tycoon.current_tab == 'BUILD':

        keys = list(app.tycoon.buildings.keys())

        total_h = len(keys) * (item_h + 10)

        app.tycoon.max_scroll = max(0, total_h - content_h + 20)

        for i, key in enumerate(keys):

            b = app.tycoon.buildings[key]

            y_pos = start_y + i * (item_h + 10)

            if y_pos + item_h < content_y or y_pos > h: continue

            cost = int(b['cost'] * (1.15 ** b['count']))

            can_afford = app.tycoon.fish_coins >= cost

            bg_color = rgb(40, 40, 60) if i % 2 == 0 else rgb(50, 50, 70)

            drawRect(20, y_pos, w - 40, item_h, fill=bg_color, border='white' if can_afford else 'gray', borderWidth=2)

            icon = app.tycoon_icons.get(key)

            if icon:

                drawImage(icon, 60, y_pos + item_h/2, width=50, height=50, align='center')

            else:

                drawRect(35, y_pos + 15, 50, 50, fill='gray')

                drawLabel(key[0].upper(), 60, y_pos + item_h/2, size=30, fill='white')

            name_color = 'white' if can_afford else 'gray'

            drawLabel(f"{b['name']} (Owned: {b['count']})", 100, y_pos + 25, size=20, fill=name_color, align='left', bold=True, font='Determination Sans')

            drawLabel(f"Cost: {cost:,} | +{b['income']} CPS", 100, y_pos + 55, size=18, fill='yellow' if can_afford else 'red', align='left', font='Determination Sans')

            btn_x = w - 100

            btn_w = 120

            btn_h = 50

            drawRect(btn_x - btn_w/2, y_pos + item_h/2 - btn_h/2, btn_w, btn_h, fill='green' if can_afford else 'gray')

            drawLabel("BUY", btn_x, y_pos + item_h/2, size=20, fill='white', bold=True, font='Determination Mono')

    elif app.tycoon.current_tab == 'UPGRADE':

        keys = list(app.tycoon.upgrades.keys())

        total_h = len(keys) * (item_h + 10)

        app.tycoon.max_scroll = max(0, total_h - content_h + 20)

        for i, key in enumerate(keys):

            u = app.tycoon.upgrades[key]

            y_pos = start_y + i * (item_h + 10)

            if y_pos + item_h < content_y or y_pos > h: continue

            can_afford = app.tycoon.fish_coins >= u['cost']

            is_owned = u['owned']

            bg_color = rgb(40, 60, 40) if is_owned else (rgb(40, 40, 60) if i % 2 == 0 else rgb(50, 50, 70))

            drawRect(20, y_pos, w - 40, item_h, fill=bg_color, border='gold' if is_owned else ('white' if can_afford else 'gray'), borderWidth=2)

            if app.upgrade_icon:

                drawImage(app.upgrade_icon, 60, y_pos + item_h/2, width=50, height=50, align='center')

            else:

                drawCircle(60, y_pos + item_h/2, 25, fill='cyan')

                drawLabel('UP', 60, y_pos + item_h/2, fill='black', bold=True)

            drawLabel(f"{u['name']}", 100, y_pos + 25, size=20, fill='gold' if is_owned else 'white', align='left', bold=True, font='Determination Sans')

            drawLabel(f"{u['desc']}", 100, y_pos + 55, size=16, fill='lightGray', align='left', font='Determination Sans')

            btn_x = w - 100

            btn_w = 120

            btn_h = 50

            if is_owned:

                drawLabel("OWNED", btn_x, y_pos + item_h/2, size=20, fill='gold', bold=True, font='Determination Mono')

            else:

                drawRect(btn_x - btn_w/2, y_pos + item_h/2 - btn_h/2, btn_w, btn_h, fill='green' if can_afford else 'gray')

                drawLabel(f"{u['cost']:,}", btn_x, y_pos + item_h/2, size=20, fill='white', bold=True, font='Determination Mono')

    elif app.tycoon.current_tab == 'SKILLS':

        keys = list(app.tycoon.skills.keys())

        total_h = len(keys) * (item_h + 10)

        app.tycoon.max_scroll = max(0, total_h - content_h + 20)

        for i, key in enumerate(keys):

            s = app.tycoon.skills[key]

            y_pos = start_y + i * (item_h + 10)

            if y_pos + item_h < content_y or y_pos > h: continue

            can_afford = app.tycoon.pearls >= s['cost']

            is_maxed = s['level'] >= s['max']

            bg_color = rgb(60, 40, 60)

            drawRect(20, y_pos, w - 40, item_h, fill=bg_color, border='pink', borderWidth=2)

            if app.skill_icon:

                drawImage(app.skill_icon, 60, y_pos + item_h/2, width=50, height=50, align='center')

            else:

                drawStar(60, y_pos + item_h/2, 25, 5, fill='pink')

            drawLabel(f"{s['name']} (Lvl {s['level']}/{s['max']})", 100, y_pos + 25, size=20, fill='pink', align='left', bold=True, font='Determination Sans')

            drawLabel(f"{s['desc']}", 100, y_pos + 55, size=16, fill='white', align='left', font='Determination Sans')

            btn_x = w - 100

            btn_w = 120

            btn_h = 50

            if is_maxed:

                drawLabel("MAXED", btn_x, y_pos + item_h/2, size=20, fill='white', bold=True, font='Determination Mono')

            else:

                drawRect(btn_x - btn_w/2, y_pos + item_h/2 - btn_h/2, btn_w, btn_h, fill='purple' if can_afford else 'gray')

                drawLabel(f"{s['cost']} Pearl", btn_x, y_pos + item_h/2, size=18, fill='white', bold=True, font='Determination Mono')

    elif app.tycoon.current_tab == 'REBIRTH':

        app.tycoon.max_scroll = 0

        center_y = content_y + content_h / 2

        drawLabel("PRESTIGE / REBIRTH", w/2, content_y + 40, size=30, fill='pink', bold=True, font='Determination Mono')

        drawLabel("Reset your progress to gain PEARLS.", w/2, content_y + 80, size=20, fill='white', font='Determination Sans')

        drawLabel("Pearls boost income by 10% each!", w/2, content_y + 110, size=20, fill='yellow', font='Determination Sans')

        import math

        potential = int(math.sqrt(app.tycoon.fish_coins / 5000))

        drawLabel(f"Current Run Coins: {int(app.tycoon.fish_coins):,}", w/2, center_y - 20, size=24, fill='gold', font='Determination Sans')

        drawLabel(f"Potential Pearls: +{potential}", w/2, center_y + 20, size=30, fill='pink', bold=True, font='Determination Mono')

        btn_y = center_y + 100

        btn_w = 200

        btn_h = 60

        can_rebirth = potential >= 1

        drawRect(w/2 - btn_w/2, btn_y - btn_h/2, btn_w, btn_h, fill='purple' if can_rebirth else 'gray', border='white', borderWidth=3)

        drawLabel("REBIRTH NOW", w/2, btn_y, size=24, fill='white', bold=True, font='Determination Mono')

        if not can_rebirth:

            drawLabel("(Need more coins)", w/2, btn_y + 50, size=16, fill='gray', font='Determination Sans')

    drawRect(w - 160, 10, 150, 40, fill='red', border='white', borderWidth=2)

    drawLabel("EXIT DLC", w - 85, 30, size=20, fill='white', bold=True, font='Determination Mono')

def redrawAll(app):

    w, h = app.width, app.height

    if hasattr(app, 'mode') and app.mode == 'tycoon':

        draw_tycoon_mode(app)

        return

    import math

    if app.inBossBattle and app.bossBattle:

        app.bossBattle.draw(app)

        return

    if app.background_image:

        drawImage(app.background_image, 0, 0, width=w, height=h)

    else:

        drawRect(0, 0, w, h, fill=rgb(80, 160, 220))

        drawRect(0, h * 0.15, w, h * 0.85, fill=rgb(70, 145, 205))

        drawRect(0, h * 0.30, w, h * 0.70, fill=rgb(60, 130, 185))

        drawRect(0, h * 0.45, w, h * 0.55, fill=rgb(50, 115, 165))

        drawRect(0, h * 0.60, w, h * 0.40, fill=rgb(40, 100, 145))

        drawRect(0, h * 0.75, w, h * 0.25, fill=rgb(30, 85, 125))

        for i in range(6):

            radius = w * (0.9 - i * 0.14)

            opacity = 4 - i * 0.6

            drawCircle(w/2, h * 0.05, radius, fill='white', opacity=opacity)

    wave_time = app.time

    wave_spacing = w * 0.05

    if app.wave_image:

        for i in range(int(-w * 0.15), int(w * 1.15), int(wave_spacing)):

            x_pos = i + (wave_time % 100) / 2

            drawImage(app.wave_image, x_pos, h * 0.033, width=w * 0.175, height=h * 0.055, opacity=25)

            drawImage(app.wave_image, x_pos - w * 0.0625, h * 0.1, width=w * 0.175, height=h * 0.055, opacity=20)

            drawImage(app.wave_image, x_pos + w * 0.025, h * 0.178, width=w * 0.15, height=h * 0.044, opacity=15)

    else:

        for i in range(int(-w * 0.15), int(w * 1.15), int(wave_spacing)):

            x_pos = i + (wave_time % 100) / 2

            drawOval(x_pos, h * 0.033, w * 0.175, h * 0.055, fill=rgb(120, 200, 240), opacity=25)

            drawOval(x_pos - w * 0.0625, h * 0.1, w * 0.175, h * 0.055, fill=rgb(100, 180, 220), opacity=20)

            drawOval(x_pos + w * 0.025, h * 0.178, w * 0.15, h * 0.044, fill=rgb(90, 170, 210), opacity=15)

    ray_spacing = w * 0.2

    for i in range(0, int(w), int(ray_spacing)):

        ray_opacity = 5 + (math.sin((wave_time + i) / 30) * 3)

        drawPolygon(i, 0, i + w * 0.05, 0, i + w * 0.1, h * 0.33, i + w * 0.05, h * 0.33, 

                   fill='white', opacity=ray_opacity)

    for fish in app.floating_fish:

        assets = app.fish_assets[fish.fish_type_index]

        fish.draw(app.time, w, h, assets['normal'], assets['flipped'])

    for bubble in app.bubbles:

        bubble.draw(w, h, app.bubble_image)

    for particle in app.light_particles:

        particle.draw(w, h, app.time)

    kelp_spacing = w * 0.025

    if app.kelp_image:

        for i in range(int(-w * 0.1), int(w * 1.1), int(kelp_spacing)):

            kelp_x = i

            kelp_sway = math.sin((wave_time + i) / 20) * (w * 0.0125)

            kelp_width = w * 0.06

            kelp_height = h * 0.15

            drawImage(app.kelp_image, kelp_x + kelp_sway, h - kelp_height/2, 

                     width=kelp_width, height=kelp_height, opacity=40, align='center')

    else:

        for i in range(int(-w * 0.1), int(w * 1.1), int(kelp_spacing)):

            kelp_x = i

            kelp_sway = math.sin((wave_time + i) / 20) * (w * 0.0125)

            kelp_width = w * 0.02

            drawPolygon(kelp_x, h, 

                       kelp_x + kelp_sway, h * 0.89,

                       kelp_x + kelp_sway + kelp_width, h * 0.89,

                       kelp_x + kelp_width, h,

                       fill=rgb(20, 80, 60), opacity=40)

            drawPolygon(kelp_x + kelp_width * 1.8, h,

                       kelp_x + kelp_width * 1.8 - kelp_sway, h * 0.93,

                       kelp_x + kelp_width * 2.5 - kelp_sway, h * 0.93,

                       kelp_x + kelp_width * 2.5, h,

                       fill=rgb(30, 90, 70), opacity=35)

    title_y = h * 0.033

    title_h = h * 0.055

    if app.title_panel_image:

        drawImage(app.title_panel_image, w/2, title_y, width=w * 0.9, height=title_h, align='center')

    else:

        drawRect(w/2, title_y, w * 0.9, title_h, fill='white', opacity=90, 

                border='black', borderWidth=int(w * 0.005), align='center')

        corner_size = min(w, h) * 0.012

        drawCircle(w * 0.075, title_y - title_h * 0.4, corner_size, fill='black', opacity=50)

        drawCircle(w * 0.925, title_y - title_h * 0.4, corner_size, fill='black', opacity=50)

        drawCircle(w * 0.075, title_y + title_h * 0.4, corner_size, fill='black', opacity=50)

        drawCircle(w * 0.925, title_y + title_h * 0.4, corner_size, fill='black', opacity=50)

    dlc_btn_x = w * 0.9

    dlc_btn_y = title_y

    dlc_btn_w = w * 0.15

    dlc_btn_h = title_h * 0.8

    drawRect(dlc_btn_x, dlc_btn_y, dlc_btn_w, dlc_btn_h, fill='gold', border='white', borderWidth=2, align='center')

    drawLabel("DLC", dlc_btn_x, dlc_btn_y, size=16, fill='black', bold=True, font='ArcadeClassic')

    title_size = int(min(w, h) * 0.028)

    subtitle_size = int(min(w, h) * 0.018)

    drawLabel('wahhh wahhh where\'s my mom! ahh seal simulator', w/2, title_y - title_h * 0.2, size=title_size, bold=True, fill='black', font='Determination Sans')

    drawLabel(f'Day {app.stats.day} | Age: {app.stats.age_days} days old', 

             w/2, title_y + title_h * 0.2, size=subtitle_size, bold=True, fill='black', font='BoldPixels')

    avg_stat = (app.stats.hunger + app.stats.health + app.stats.happiness + app.stats.energy) / 4

    if avg_stat > 70:

        emotion = 'happy'

    elif avg_stat > 40:

        emotion = 'neutral'

    elif app.stats.energy < 30:

        emotion = 'tired'

    else:

        emotion = 'sad'

    seal_x = w / 2

    seal_y = h * 0.16

    ice_w = w * 0.22

    ice_h = h * 0.044

    if app.ice_image:

        drawImage(app.ice_image, seal_x, seal_y + h * 0.01, width=ice_w, height=ice_h, align='center')

    else:

        drawOval(seal_x, seal_y + h * 0.018, ice_w * 1.08, ice_h * 0.95, fill='black', opacity=25)

        drawOval(seal_x, seal_y + h * 0.01, ice_w, ice_h, fill=rgb(195, 225, 240), opacity=90)

        drawOval(seal_x, seal_y + h * 0.006, ice_w * 0.88, ice_h * 0.85, fill=rgb(225, 240, 250), opacity=65)

        drawOval(seal_x - ice_w * 0.18, seal_y + h * 0.004, ice_w * 0.35, ice_h * 0.65, fill='white', opacity=45)

        drawOval(seal_x + ice_w * 0.12, seal_y + h * 0.005, ice_w * 0.25, ice_h * 0.5, fill='white', opacity=35)

        drawOval(seal_x, seal_y + h * 0.01, ice_w * 1.03, ice_h * 1.08, fill=None, 

                border=rgb(170, 210, 230), borderWidth=int(w * 0.0025), opacity=60)

    seal_size = min(w, h) * 0.09

    seal_bounce = math.sin(app.time / 30) * (h * 0.004)

    if app.seal_image:

        drawImage(app.seal_image, seal_x, seal_y + seal_bounce - h * 0.025, width=seal_size*1.2, height=seal_size, align='center')

    else:

        draw_seal_default(seal_x, seal_y + seal_bounce, seal_size, emotion)

    if emotion == 'happy':

        for i in range(5):

            sparkle_x = seal_x + math.cos(app.time / 15 + i * 1.2) * (w * 0.08)

            sparkle_y = seal_y - h * 0.03 + math.sin(app.time / 15 + i * 1.2) * (h * 0.04)

            star_size = min(w, h) * 0.008 + math.sin(app.time / 10 + i) * (min(w, h) * 0.002)

            if app.sparkle_image:

                drawImage(app.sparkle_image, sparkle_x, sparkle_y, width=star_size*3, height=star_size*3, align='center', opacity=60)

            else:

                drawStar(sparkle_x, sparkle_y, star_size, 5, fill='yellow', opacity=60)

    if emotion == 'tired':

        z_offset = (app.time % 60) / 10

        z_x = seal_x + w * 0.075

        if app.sleep_image:

            z_size = min(w, h) * 0.04

            drawImage(app.sleep_image, z_x, seal_y - h * 0.06 - z_offset * h * 0.003, 

                     width=z_size, height=z_size*1.5, opacity=70 - z_offset * 7)

        else:

            z_size_lg = int(min(w, h) * 0.018)

            z_size_md = int(min(w, h) * 0.015)

            z_size_sm = int(min(w, h) * 0.012)

            drawLabel('Z', z_x, seal_y - h * 0.06 - z_offset * h * 0.003, size=z_size_lg, fill='white', opacity=70 - z_offset * 7, font='ArcadeClassic')

            drawLabel('z', z_x + w * 0.0125, seal_y - h * 0.05 - z_offset * 0.7 * h * 0.003, size=z_size_md, fill='white', opacity=60 - z_offset * 6, font='ArcadeClassic')

            drawLabel('z', z_x + w * 0.025, seal_y - h * 0.045 - z_offset * 0.4 * h * 0.003, size=z_size_sm, fill='white', opacity=50 - z_offset * 5, font='ArcadeClassic')

    stats_y = h * 0.28

    stats_h = h * 0.16

    if app.stats_panel_image:

        drawImage(app.stats_panel_image, w/2, stats_y, width=w * 0.95, height=stats_h, align='center')

    else:

        drawRect(w/2, stats_y, w * 0.96, stats_h * 1.05, fill='cyan', opacity=15, align='center')

        drawRect(w/2 + w * 0.005, stats_y + h * 0.003, w * 0.95, stats_h, fill='black', opacity=50, align='center')

        drawRect(w/2, stats_y, w * 0.95, stats_h, fill='black', opacity=70, align='center')

        drawRect(w/2, stats_y, w * 0.95, stats_h, fill=rgb(25, 35, 50), opacity=90, 

                border='cyan', borderWidth=int(w * 0.004), align='center')

        drawRect(w/2, stats_y, w * 0.94, stats_h * 0.96, fill=None, 

                border='white', borderWidth=int(w * 0.002), opacity=30, align='center')

    bar_w = w * 0.4

    bar_h = h * 0.03

    bar_y1 = h * 0.23

    bar_y2 = h * 0.275

    hunger_img = get_stat_image(app.stat_images, 'hunger', app.stats.hunger)

    health_img = get_stat_image(app.stat_images, 'health', app.stats.health)

    energy_img = get_stat_image(app.stat_images, 'energy', app.stats.energy)

    happiness_img = get_stat_image(app.stat_images, 'happiness', app.stats.happiness)

    draw_stat_bar(w * 0.05, bar_y1, bar_w, bar_h, app.stats.hunger, 100, 'HUNGER', 

                 (50, 200, 50), (255, 50, 50), w, h, hunger_img)

    draw_stat_bar(w * 0.525, bar_y1, bar_w, bar_h, app.stats.health, 100, 'HEALTH', 

                 (255, 100, 100), (150, 0, 0), w, h, health_img)

    draw_stat_bar(w * 0.05, bar_y2, bar_w, bar_h, app.stats.energy, 100, 'ENERGY', 

                 (255, 200, 0), (150, 100, 0), w, h, energy_img)

    draw_stat_bar(w * 0.525, bar_y2, bar_w, bar_h, app.stats.happiness, 100, 'HAPPY', 

                 (100, 150, 255), (100, 100, 150), w, h, happiness_img)

    threat_y = h * 0.32

    threat_size = int(min(w, h) * 0.015)

    drawLabel(f'Orca Threat: {int(app.stats.orca_threat)}%', w * 0.25, threat_y, 

             size=threat_size, bold=True, fill='black', font='BoldPixels')

    drawLabel(f'Find Mother: {int(app.stats.mother_chance)}%', w * 0.75, threat_y, 

             size=threat_size, bold=True, fill='black', font='BoldPixels')

    drawLabel(f'Visibility: {int(app.stats.visibility)}%', w * 0.5, threat_y, 

             size=threat_size, bold=True, fill='black', font='BoldPixels')

    action_y = h * 0.58

    action_h = h * 0.042

    if app.action_panel_image:

        drawImage(app.action_panel_image, w/2, action_y, width=w * 0.95, height=action_h, align='center')

    else:

        drawRect(w/2, action_y, w * 0.95, action_h, fill='black', opacity=50, align='center')

        drawRect(w/2, action_y, w * 0.95, action_h, fill=rgb(40, 60, 90), opacity=85, 

                border='white', borderWidth=int(w * 0.0025), align='center')

    action_size = int(min(w, h) * 0.02)

    if app.event_timer > 0:

        drawLabel(app.event_message, w/2, action_y, size=action_size, bold=True, fill='black', font='BoldPixels')

    else:

        drawLabel('Choose Your Action:', w/2, action_y, size=action_size, bold=True, fill='black', font='BoldPixels')

    for button in app.buttons:

        button.draw(app.button_image, app.button_hover_image, w, h)

    if app.inFishingMinigame and app.fishingMinigame:

        app.fishingMinigame.draw(app)

    if app.gameWon:

        if app.victory_bg_image:

            drawImage(app.victory_bg_image, 0, 0, width=w, height=h)

        else:

            drawRect(0, 0, w, h, fill='black', opacity=80)

        panel_w = w * 0.9

        panel_h = h * 0.48

        panel_y = h * 0.5

        if not app.victory_bg_image:

            drawRect(w/2, panel_y, panel_w, panel_h, fill='black', opacity=90, align='center')

            drawRect(w/2, panel_y, panel_w, panel_h, fill=rgb(20, 40, 20), 

                    border='lightGreen', borderWidth=int(w * 0.006), align='center')

        pulse = abs(math.sin(app.time / 20)) * 10

        for i in range(3):

            drawStar(w * (0.3 + i * 0.2), h * 0.2 + pulse, min(w, h) * 0.02, 5, fill='yellow', opacity=80)

        title_size = int(min(w, h) * 0.065)

        drawLabel('VICTORY!', w/2 + 2, h * 0.28 + 2, size=title_size, fill='black', bold=True, font='ArcadeClassic')

        drawLabel('VICTORY!', w/2, h * 0.28, size=title_size, fill='lightGreen', bold=True, font='ArcadeClassic')

        msg_size = int(min(w, h) * 0.022)

        drawLabel('You found your mother!', w/2, h * 0.365, size=msg_size, fill='cyan', bold=True, font='ArcadeClassic')

        drawLabel('You are safe now!', w/2, h * 0.405, size=int(msg_size * 0.85), fill='white', bold=True, font='ArcadeClassic')

        stat1_size = int(min(w, h) * 0.024)

        stat2_size = int(min(w, h) * 0.02)

        drawLabel(f'Survived {app.stats.day - 1} days alone', w/2, h * 0.46, size=stat1_size, fill='yellow', bold=True, font='ArcadeClassic')

        drawLabel(f'Final Orca Threat: {int(app.stats.orca_threat)}%', w/2, h * 0.50, size=stat2_size, fill='orange', font='BoldPixels')

        drawLabel(f'Final Visibility: {int(app.stats.visibility)}%', w/2, h * 0.535, size=stat2_size, fill='white', font='BoldPixels')

        summary_size = int(min(w, h) * 0.019)

        detail_size = int(min(w, h) * 0.016)

        drawLabel(f'Final Stats:', w/2, h * 0.58, size=summary_size, fill='yellow', bold=True, font='BoldPixels')

        drawLabel(f'Hunger: {int(app.stats.hunger)} | Health: {int(app.stats.health)}', 

                 w/2, h * 0.615, size=detail_size, fill='white', font='BoldPixels')

        btn_w = w * 0.25

        btn_h = h * 0.055

        btn_y = h * 0.7

        drawRect(w/2, btn_y, btn_w, btn_h, fill=rgb(50, 150, 50), 

                border='white', borderWidth=int(w * 0.003), align='center')

        btn_size = int(min(w, h) * 0.021)

        hint_size = int(min(w, h) * 0.015)

        drawLabel('Play Again', w/2, btn_y, size=btn_size, bold=True, fill='white', font='ArcadeClassic')

        drawLabel('(Click or press R)', w/2, btn_y + btn_h * 0.8, size=hint_size, fill='lightGray', font='ArcadeClassic')

    elif app.gameOver:

        if app.gameover_bg_image:

            drawImage(app.gameover_bg_image, 0, 0, width=w, height=h)

        else:

            drawRect(0, 0, w, h, fill='black', opacity=80)

        panel_w = w * 0.9

        panel_h = h * 0.48

        panel_y = h * 0.5

        if not app.gameover_bg_image:

            drawRect(w/2, panel_y, panel_w, panel_h, fill='black', opacity=90, align='center')

            drawRect(w/2, panel_y, panel_w, panel_h, fill=rgb(20, 20, 20), 

                    border='red', borderWidth=int(w * 0.006), align='center')

        title_size = int(min(w, h) * 0.065)

        drawLabel('GAME OVER', w/2 + 2, h * 0.28 + 2, size=title_size, fill='black', bold=True, font='ArcadeClassic')

        drawLabel('GAME OVER', w/2, h * 0.28, size=title_size, fill='red', bold=True, font='ArcadeClassic')

        if hasattr(app, 'caught_by_orca') and app.caught_by_orca:

            message = '[X] CAUGHT BY ORCA'

        elif app.stats.hunger <= 0:

            message = '[X] DIED OF STARVATION'

        elif app.stats.health <= 0:

            message = '[X] HEALTH REACHED ZERO'

        else:

            message = '[X] COULD NOT SURVIVE'

        msg_size = int(min(w, h) * 0.022)

        drawLabel(message, w/2, h * 0.365, size=msg_size, fill='orange', bold=True, font='ArcadeClassic')

        stat1_size = int(min(w, h) * 0.024)

        stat2_size = int(min(w, h) * 0.02)

        drawLabel(f'Survived {app.stats.day - 1} days', w/2, h * 0.43, size=stat1_size, fill='cyan', bold=True, font='ArcadeClassic')

        drawLabel(f'Final Orca Threat: {int(app.stats.orca_threat)}%', w/2, h * 0.47, size=stat2_size, fill='red', font='BoldPixels')

        summary_size = int(min(w, h) * 0.019)

        detail_size = int(min(w, h) * 0.016)

        drawLabel(f'Final Stats:', w/2, h * 0.52, size=summary_size, fill='yellow', bold=True, font='BoldPixels')

        drawLabel(f'Hunger: {int(app.stats.hunger)} | Health: {int(app.stats.health)}', 

                 w/2, h * 0.555, size=detail_size, fill='white', font='BoldPixels')

        drawLabel(f'Energy: {int(app.stats.energy)} | Happiness: {int(app.stats.happiness)}', 

                 w/2, h * 0.59, size=detail_size, fill='white', font='BoldPixels')

        btn_w = w * 0.25

        btn_h = h * 0.055

        btn_y = h * 0.7

        drawRect(w/2, btn_y, btn_w, btn_h, fill=rgb(50, 150, 50), 

                border='white', borderWidth=int(w * 0.003), align='center')

        btn_size = int(min(w, h) * 0.021)

        hint_size = int(min(w, h) * 0.015)

        drawLabel('Restart', w/2, btn_y, size=btn_size, bold=True, fill='white', font='ArcadeClassic')

        drawLabel('(Click or press R)', w/2, btn_y + btn_h * 0.8, size=hint_size, fill='lightGray', font='ArcadeClassic')

if __name__ == '__main__':

    runApp(width=800, height=900)
