Web VPython 3.2

# Modified by: yeabsirateshomehabtemichael

# Scene setup
scene.background = color.cyan 
scene.width = 800
scene.height = 500
scene.range = 20 

# Graph setup - Moved to the bottom for better visibility
v_alt_graph = graph(title="Velocity vs Altitude", xtitle="Altitude (m)", ytitle="Velocity (m/s)", 
                    width=800, height=300, align="bottom")
v_curve = gcurve(color=color.blue, width=3)

# Constants
g = 9.8
m = 70
rho = 1.225
A = 4.0    
Cd = 1.4
v = 0
y = 700    
dt = 0.01

# --- Visual Objects ---
ground = box(pos=vec(0, -10, 0), size=vec(2000, 20, 2000), color=color.green)
sun_sphere = sphere(pos=vec(200, 500, -200), radius=40, color=color.yellow, emissive=True)

# THE SUPER VISIBLE SKYDIVER
parachute_canopy = sphere(pos=vec(0, 8, 0), radius=6, color=color.red)
line1 = cylinder(pos=vec(0, 0, 0), axis=vec(-4, 8, 0), radius=0.1, color=color.white)
line2 = cylinder(pos=vec(0, 0, 0), axis=vec(4, 8, 0), radius=0.1, color=color.white)
body = cylinder(pos=vec(0, 0, 0), axis=vec(0, -3, 0), radius=0.8, color=color.orange)
head = sphere(pos=vec(0, 0.5, 0), radius=0.9, color=color.orange)

skydiver = compound([parachute_canopy, line1, line2, body, head], make_trail=True)
skydiver.trail_color = color.yellow
skydiver.pos.y = y

# Adding Clouds
def create_cloud(x, y, z):
    for i in range(5):
        sphere(pos=vec(x + i*4, y + (random()*3), z), radius=8, color=color.white, opacity=0.8)

for i in range(15):
    create_cloud((random()*1000)-500, 100 + (random()*500), (random()*600)-300)

# BIG VISIBLE LABELS (Using 'label' which floats in 3D space)
# We place them slightly to the side of the skydiver's path
label_v = label(pos=vec(15, y, 0), text='Speed: 0 m/s', height=20, color=color.black, box=True)
label_y = label(pos=vec(15, y-5, 0), text='Altitude: 700 m', height=20, color=color.black, box=True)

# Simulation Loop
while skydiver.pos.y > 0:
    rate(100)
    
    scene.center = skydiver.pos # Follow the skydiver
    
    # Physics
    Fg = m * g
    Fd = 0.5 * rho * (v**2) * Cd * A
    ay = (Fd - Fg) / m
    
    v = v + ay * dt
    y = y + v * dt
    
    # Update position
    skydiver.pos.y = y
    
    # Update Label Positions and Text
    label_v.pos = skydiver.pos + vec(15, 0, 0)
    label_y.pos = skydiver.pos + vec(15, -5, 0)
    
    label_v.text = 'Speed: ' + str(round(abs(v), 2)) + ' m/s'
    label_y.text = 'Altitude: ' + str(round(y, 2)) + ' m'
    
    # Update Graph
    v_curve.plot(y, abs(v))

print("Landed!")