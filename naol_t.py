Web VPython 3.2
from vpython import *
import random

scene.title = "Paratrooper Jump from Plane"
scene.fullscreen = True
scene.center = vector(0,200,0)
scene.background = vector(0.05,0.05,0.05)   # almost black night sky

# Add stars in background
num_stars = 200
for i in range(num_stars):
    x = random.uniform(-600,600)
    y = random.uniform(100,800)
    z = random.uniform(-600,600)
    sphere(pos=vector(x,y,z), radius=0.5, color=color.white, emissive=True)

# constants
g = 9.8
mass = 80
Cd = 0.5
A = 2.5
rho = 1.225
dt = 0.01
t = 0

# plane
plane_body = box(pos=vector(0,700,0), size=vector(180,30,60), color=color.gray(0.7))
plane_wing = box(pos=plane_body.pos + vector(0,0,45), size=vector(180,6,90), color=color.red)
plane_wing2 = box(pos=plane_body.pos + vector(0,0,-45), size=vector(180,6,90), color=color.red)

# ground (visible grass color)
ground = box(pos=vector(0,0,0), size=vector(1200,4,1200), color=vector(0.1,0.6,0.1))  # green grass

# person
scale = 8
body = cylinder(pos=vector(0,700,0), axis=vector(0,5*scale,0), radius=1.5*scale, color=color.red)
head = sphere(pos=body.pos + vector(0,6*scale,0), radius=2*scale, color=color.yellow)
left_arm = cylinder(pos=body.pos + vector(-1.5*scale,4*scale,0), axis=vector(-2.5*scale,0,0), radius=0.5*scale, color=color.red)
right_arm = cylinder(pos=body.pos + vector(1.5*scale,4*scale,0), axis=vector(2.5*scale,0,0), radius=0.5*scale, color=color.red)
left_leg = cylinder(pos=body.pos, axis=vector(-1.5*scale,-5*scale,0), radius=0.5*scale, color=color.red)
right_leg = cylinder(pos=body.pos, axis=vector(1.5*scale,-5*scale,0), radius=0.5*scale, color=color.red)

person = compound([body, head, left_arm, right_arm, left_leg, right_leg])
person.velocity = vector(0,0,0)

# parachute settings
parachute_deployed = False
Cd_parachute = 0.9
A_parachute = 20
deploy_height = 400
parachute = None

# terminal velocity
terminal_v = sqrt((2*mass*g)/(rho*Cd*A))

# labels
velocity_label = label(pos=vector(-500,650,0), text='Velocity: 0 m/s', height=16, box=False, color=color.white)
time_label = label(pos=vector(-500,600,0), text='Time: 0 s', height=16, box=False, color=color.white)
terminal_label = label(pos=vector(-500,550,0), text=f'Terminal velocity: {terminal_v:.1f} m/s', height=16, box=False, color=color.white)

# drag function
def drag_force(v, Cd, A):
    return 0.5 * rho * Cd * A * v**2

# simulation
while person.pos.y > 0:
    rate(100)
    t += dt

    v = mag(person.velocity)

    if v != 0:
        F_drag = -norm(person.velocity) * drag_force(v, Cd, A)
    else:
        F_drag = vector(0,0,0)

    F_gravity = vector(0,-mass*g,0)
    F_net = F_gravity + F_drag

    person.velocity += (F_net/mass) * dt
    person.pos += person.velocity * dt

    # parachute opens
    if not parachute_deployed and person.pos.y < deploy_height:
        parachute_deployed = True
        Cd = Cd_parachute
        A = A_parachute

        parachute = cone(
            pos=person.pos + vector(0,15*scale,0),
            axis=vector(0,-5,0),
            radius=14*scale,
            color=color.cyan,
            opacity=0.9
        )

    # parachute follows person
    if parachute_deployed:
        parachute.pos = person.pos + vector(0,15*scale,0)

    velocity_label.text = f'Velocity: {v:.1f} m/s'
    time_label.text = f'Time: {t:.2f} s'