Web VPython 3.2
from vpython import *

# Full-screen scene
scene.title = "Paratrooper Jump from Plane"
scene.fullscreen = True
scene.center = vector(0,200,0)
scene.background = vector(0.53, 0.81, 0.92)  # sky blue

# Constants
g = 9.8
mass = 80
Cd = 0.5
A = 2.5       # cross-section for large objects
rho = 1.225
dt = 0.01
t = 0

# Plane (large)
plane_body = box(pos=vector(0,700,0), size=vector(180,30,60), color=color.gray(0.7))
plane_wing = box(pos=plane_body.pos + vector(0,0,45), size=vector(180,6,90), color=color.red)
plane_wing2 = box(pos=plane_body.pos + vector(0,0,-45), size=vector(180,6,90), color=color.red)
plane_tail = box(pos=plane_body.pos + vector(-90,30,0), size=vector(45,45,15), color=color.blue)

# Ground
ground = box(pos=vector(0,0,0), size=vector(1200,4,1200), color=vector(0.55,0.27,0.07))  # brown land

# Sun
sun = sphere(pos=vector(400,800,0), radius=100, color=color.yellow, emissive=True)

# Paratrooper (large)
scale = 8
body = cylinder(pos=vector(0,700,0), axis=vector(0,5*scale,0), radius=1.5*scale, color=color.red)
head = sphere(pos=body.pos + vector(0,6*scale,0), radius=2*scale, color=color.yellow)
left_arm = cylinder(pos=body.pos + vector(-1.5*scale,4*scale,0), axis=vector(-2.5*scale,0,0), radius=0.5*scale, color=color.red)
right_arm = cylinder(pos=body.pos + vector(1.5*scale,4*scale,0), axis=vector(2.5*scale,0,0), radius=0.5*scale, color=color.red)
left_leg = cylinder(pos=body.pos, axis=vector(-1.5*scale,-5*scale,0), radius=0.5*scale, color=color.red)
right_leg = cylinder(pos=body.pos, axis=vector(1.5*scale,-5*scale,0), radius=0.5*scale, color=color.red)
person = compound([body, head, left_arm, right_arm, left_leg, right_leg])
person.velocity = vector(0,0,0)
trail = attach_trail(person, radius=0.5*scale, color=color.white)

# Parachute
parachute_deployed = False
Cd_parachute = 1.5
A_parachute = 50

# Terminal velocity
terminal_v = sqrt((2*mass*g)/(rho*Cd*A))

# Labels (small and clear)
velocity_label = label(pos=vector(-500,650,0), text='Velocity: 0 m/s', height=14, box=False, color=color.black, opacity=0)
time_label = label(pos=vector(-500,620,0), text='Time: 0 s', height=14, box=False, color=color.black, opacity=0)
terminal_label = label(pos=vector(-500,590,0), text=f'Terminal velocity: {terminal_v:.1f} m/s', height=14, box=False, color=color.black, opacity=0)

# Drag function
def drag_force(v, Cd, A):
    return 0.5 * rho * Cd * A * v**2

# Simulation loop
while person.pos.y - (5*scale) > 0:
    rate(100)
    t += dt
    
    v = mag(person.velocity)
    F_drag = -norm(person.velocity) * drag_force(v, Cd, A) if v != 0 else vector(0,0,0)
    F_gravity = vector(0,-mass*g,0)
    F_net = F_gravity + F_drag
    
    person.velocity += F_net/mass * dt
    person.pos += person.velocity * dt
    
    if not parachute_deployed and abs(person.velocity.y) >= terminal_v:
        parachute_deployed = True
        Cd = Cd_parachute
        A = A_parachute
        # Umbrella-style parachute above the person
        canopy = hemisphere(pos=person.pos + vector(0,14*scale,0), radius=12*scale, color=color.orange, opacity=0.6)
        person.color = color.green
    
    # Update labels
    velocity_label.text = f'Velocity: {v:.1f} m/s'
    time_label.text = f'Time: {t:.2f} s'
    terminal_label.text = f'Terminal velocity: {terminal_v:.1f} m/s'

print("Paratrooper landed safely!")