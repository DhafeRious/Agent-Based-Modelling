from cProfile import label
import matplotlib.dates as mdates
import random
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation

MEAN_SPEED = 2
SIMULATION_STEP = 30  # 1 minute
ENV_SIZE = 200 # 40000 m²
NB_WORKS = 5
NB_SCHOOLS = 5
NB_LEISURES = 5
NB_HOMES = 10
NB_PERSONS = 100

environments = []


def distance(p1, p2):
	"""
		Calculate the distance between two points p1(x1, y1) and p2(x2, y2)
	"""
	return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** (0.5)


def get_closest_env(home_env, type):
	dmax = 100000
	res = home_env
	for e in environments:
		d = distance(e.coords, home_env.coords)
		if e.type == type and d < dmax:
			dmax = d
			res = e
	return res


class person:
	def __init__(self, age, home_env):
		self.age = age
		self.home_env = home_env
		self.current_location = home_env.coords
		self.current_env = home_env
		self.moving = None

	def update_location(self, t):
		hour = t.hour
		day = t.weekday()
		if self.moving:
			self.move()
			return
		new_env = self.current_env
		if day in (5, 6):  # Saturday & sunday
			if hour == 8 and self.current_location == self.home_env.coords:
				if random.randint(0, 10) >= 1:
					new_env = get_closest_env(self.home_env, "leisure")
			if hour == 20 and self.current_location != self.home_env.coords:
				new_env = self.home_env
		else:
			if hour == 8 and self.current_location == self.home_env.coords:
				if (6 <= self.age <= 22):
					new_env = get_closest_env(self.home_env, "school")
				elif (23 <= self.age <= 60):
					new_env = get_closest_env(self.home_env, "work")
				else:
					if random.randint(0, 10) >= 5:
						new_env = get_closest_env(self.home_env, "leisure")
			if hour == 18 and self.current_location != self.home_env.coords:
				new_env = self.home_env
		if new_env.coords != self.current_location:
			self.moving = (self.current_env, new_env)
			self.current_env = None

	def move(self):
		from_point = self.moving[0].coords
		to_point = self.moving[1].coords
		d = distance(self.current_location, to_point)
		new_x = MEAN_SPEED / d * SIMULATION_STEP * (to_point[0] - self.current_location[0]) + self.current_location[0]
		new_y = MEAN_SPEED / d * SIMULATION_STEP * (to_point[1] - self.current_location[1]) + self.current_location[1]
		# Si le point (person) dépasse la destination ou est confondu avec la destination on arrête le movement
		if ((to_point[0] - new_x) * (to_point[0] - from_point[0])) + ((to_point[1] - new_y) * (to_point[1] - from_point[1])) <= 0:
			self.current_location = to_point
			self.current_env = self.moving[1]
			self.moving = None
			return
		self.current_location = (new_x, new_y)


class environment:
	def __init__(self, coords, type):
		self.coords = coords
		self.type = type


colors = []
# HOMES
for i in range(NB_HOMES):
	environments.append(
		environment((random.randint(0, ENV_SIZE),
		            random.randint(0, ENV_SIZE)), 'home')
	)
colors.extend(['purple'] * NB_HOMES)

# LEISURE
for i in range(NB_LEISURES):
	environments.append(
		environment((random.randint(0, ENV_SIZE),
		            random.randint(0, ENV_SIZE)), 'leisure')
	)
colors.extend(['green'] * NB_LEISURES) 

# WORKS
for i in range(NB_WORKS):
	environments.append(
		environment((random.randint(0, ENV_SIZE),
		            random.randint(0, ENV_SIZE)), 'work')
	)
colors.extend(['black'] * NB_WORKS) 

# SCHOOLS
for i in range(NB_SCHOOLS):
	environments.append(
		environment((random.randint(0, ENV_SIZE),
		            random.randint(0, ENV_SIZE)), 'school')
	)
colors.extend(['aqua'] * NB_SCHOOLS)

persons = []
for i in range(NB_PERSONS):
	persons.append(person(random.randint(0, 90), environments[random.randint(0, NB_HOMES-1)]))

colors.extend(['red'] * NB_PERSONS)
linewidths = [6] * len(environments) + [0.5] * NB_PERSONS

data = {} # person => [(x1, y1, type_environnement), ....]
for p in persons:
	data[p] = [(*p.current_location, p.current_env.type if p.current_env else None)]

t = datetime(2022, 1, 1, 0, 0, 0)
tmax = datetime(2022, 1, 31, 0, 0, 0)
nb_frames = 1
times = [t]
while (t <= tmax):
	t += timedelta(minutes=SIMULATION_STEP)
	times.append(t)
	nb_frames += 1
	for p in persons:
		p.update_location(t)
		data[p].append((*p.current_location, p.current_env.type if p.current_env else None))


fig, ax = plt.subplots(figsize=(ENV_SIZE, ENV_SIZE))

ims = []
env_points = []
for env in environments:
	env_points.append(env.coords)

nb_persons_at_home = []
nb_persons_at_work = []
nb_persons_at_leisure = []
nb_persons_at_school = []

for i in range(nb_frames):
	frame_points = env_points.copy()
	at_home = 0
	at_work = 0
	at_leisure = 0
	at_school = 0
	for p in data:
		x, y, type_env = data[p][i]
		frame_points.append((x, y))
		if type_env == "home":
			at_home += 1
		elif type_env == "work":
			at_work += 1
		elif type_env == "school":
			at_school += 1
		elif type_env == "leisure":
			at_leisure += 1
	nb_persons_at_home.append(at_home)
	nb_persons_at_work.append(at_work)
	nb_persons_at_leisure.append(at_leisure)
	nb_persons_at_school.append(at_school)	

	frame_points = np.array(frame_points)
	ims.append([
	 	ax.scatter(frame_points[:, 0], frame_points[:, 1], c=colors, linewidths=linewidths), 
	 	ax.text(0, ENV_SIZE + 10, str(times[i]))])

# Histogramme multibar Nbr personnes / environnement à chaque instant
#ax.xaxis.set_major_formatter(mdates.DateFormatter("%d-%b %Hh"))
#ax.xaxis.set_minor_formatter(mdates.DateFormatter("%d-%b %Hh"))
#plt.xticks(rotation=90)
#ax.bar(times, nb_persons_at_home, 0.01, label="At Home")
#ax.bar(times, nb_persons_at_school, 0.01, bottom=nb_persons_at_home, label="At school")
#ax.bar(times, nb_persons_at_work, 0.01, bottom=nb_persons_at_school, label="At work")
#ax.bar(times, nb_persons_at_leisure, 0.01, bottom=nb_persons_at_work, label="At leisure")
#ax.set_ylabel('Nbr persons')
#ax.legend()

#create the animation
ani = animation.ArtistAnimation(
 	fig, ims, interval=1, blit=False)
plt.show()
