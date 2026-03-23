GlowScript 3.2 VPython

# -----------------------------
# SCENE
# -----------------------------

scene.title = "Skydiver Simulation – Terminal Velocity & Drag"
scene.width = 1000
scene.height = 600
scene.background = color.black
scene.range = 70
scene.center = vector(0,45,0)

scene.userspin = True
scene.userzoom = True
scene.userpan = True

# -----------------------------
# STARS (BACKGROUND BEAUTY)
# -----------------------------

for i in range(80):
    sphere(
        pos=vector(random()*400-200, random()*200+50, random()*400-200),
        radius=0.4,
        color=color.white,
        emissive=True
    )

# -----------------------------
# SUN LIGHT SOURCE
# -----------------------------

sun = sphere(
    pos=vector(-150,150,-150),
    radius=20,
    color=color.yellow,
    emissive=True
)

local_light(pos=sun.pos, color=color.white)

# -----------------------------
# GROUND
# -----------------------------

ground = box(
    pos=vector(0,0,0),
    size=vector(120,1,120),
    color=vector(0.2,0.6,0.2)
)

# -----------------------------
# SKYDIVER (PERSON)
# -----------------------------

pos = vector(0,100,0)

head = sphere(pos=pos+vector(0,7,0), radius=2.2, color=vector(1,0.8,0.6))

body = cylinder(pos=pos, axis=vector(0,7,0), radius=1.3, color=color.red)

armL = cylinder(pos=pos+vector(0,6,0), axis=vector(-5,0,0), radius=0.6)
armR = cylinder(pos=pos+vector(0,6,0), axis=vector(5,0,0), radius=0.6)

legL = cylinder(pos=pos, axis=vector(-1.2,-6,0), radius=0.7, color=color.blue)
legR = cylinder(pos=pos, axis=vector(1.2,-6,0), radius=0.7, color=color.blue)

# -----------------------------
# PARACHUTE
# -----------------------------

parachute = cone(
    pos=pos + vector(0,16,0),
    axis=vector(0,7,0),
    radius=18,
    color=color.orange,
    visible=False
)

# -----------------------------
# PHYSICS
# -----------------------------

v = vector(0,0,0)

g = 9.8
dt = 0.01

k_free = 0.05
k_parachute = 1.6

deploy_time = 6
t = 0

running = True

# -----------------------------
# CLEAN DATA PANEL
# -----------------------------

info = label(
    pos=vector(-60,90,0),
    height=13,
    box=False
)

# -----------------------------
# EXPLANATION PANEL
# -----------------------------

explain = label(
    pos=vector(-60,60,0),
    height=12,
    box=False,
    line=False
)

# -----------------------------
# CONTROLS
# -----------------------------

def toggle_run(b):
    global running
    running = not running
    if running:
        b.text = "Pause"
    else:
        b.text = "Resume"

def restart():
    global pos,v,t
    pos = vector(0,100,0)
    v = vector(0,0,0)
    t = 0
    parachute.visible = False

scene.append_to_caption("\n")

button(text="Pause", bind=toggle_run)
button(text="Restart", bind=restart)

# -----------------------------
# SIMULATION LOOP
# -----------------------------

while True:

    rate(100)

    if not running:
        continue

    if pos.y <= 6:
        info.text = "Landing completed"
        explain.text = "The skydiver safely reaches the ground."
        continue

    # physics stage explanations
    if t < 3:

        k = k_free
        explanation = (
        "Stage 1: Free Fall\n"
        "Only gravity acts strongly on the skydiver.\n"
        "Velocity increases downward."
        )

    elif t < deploy_time:

        k = k_free
        explanation = (
        "Stage 2: Air Resistance\n"
        "Drag force increases as speed increases.\n"
        "Acceleration becomes smaller."
        )

    else:

        k = k_parachute
        parachute.visible = True

        explanation = (
        "Stage 3: Parachute Deployment\n"
        "Surface area increases greatly.\n"
        "Air resistance increases.\n"
        "The skydiver slows down."
        )

    # drag force
    drag = -k * mag(v) * v

    # acceleration
    a = vector(0,-g,0) + drag

    # motion update
    v = v + a*dt
    pos = pos + v*dt

    # move body
    head.pos = pos + vector(0,7,0)
    body.pos = pos

    armL.pos = pos + vector(0,6,0)
    armR.pos = pos + vector(0,6,0)

    legL.pos = pos
    legR.pos = pos

    parachute.pos = pos + vector(0,16,0)

    # data display
    info.text = (
        "Time: " + str(round(t,1)) + " s\n"
        "Velocity: " + str(round(mag(v),1)) + " m/s\n"
        "Acceleration: " + str(round(mag(a),1)) + " m/s²"
    )

    explain.text = explanation

    t = t + dt
