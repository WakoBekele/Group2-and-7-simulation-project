GlowScript 3.2 VPython

# -----------------------------
# SCENE
# -----------------------------

scene.title = "Skydiver Terminal Velocity"
scene.width = 800
scene.height = 500
scene.background = vector(0.8,0.9,1)

scene.range = 50
scene.center = vector(0,40,0)

scene.userspin = True
scene.userzoom = True

ground = box(pos=vector(0,0,0), size=vector(80,1,80), color=color.green)

# -----------------------------
# SKYDIVER (PERSON)
# -----------------------------

pos = vector(0,90,0)

head = sphere(pos=pos + vector(0,6,0), radius=2, color=vector(1,0.8,0.6))

body = cylinder(pos=pos, axis=vector(0,6,0), radius=1.2, color=color.red)

armL = cylinder(pos=pos + vector(0,5,0), axis=vector(-4,0,0), radius=0.5)
armR = cylinder(pos=pos + vector(0,5,0), axis=vector(4,0,0), radius=0.5)

legL = cylinder(pos=pos, axis=vector(-1,-5,0), radius=0.6, color=color.blue)
legR = cylinder(pos=pos, axis=vector(1,-5,0), radius=0.6, color=color.blue)

# -----------------------------
# PARACHUTE
# -----------------------------

parachute = cone(
    pos = pos + vector(0,14,0),
    axis = vector(0,6,0),
    radius = 14,
    color = color.orange,
    visible = False
)

# -----------------------------
# PHYSICS
# -----------------------------

v = vector(0,0,0)

g = 9.8
dt = 0.01

k_free = 0.05
k_parachute = 1.4

deploy_time = 5
t = 0

info = label(box=False, height=11)

# -----------------------------
# SIMULATION LOOP
# -----------------------------

while pos.y > 5:

    rate(100)

    if t < deploy_time:
        k = k_free
    else:
        k = k_parachute
        parachute.visible = True

    drag = -k * mag(v) * v

    a = vector(0,-g,0) + drag

    v = v + a*dt

    pos = pos + v*dt

    # move body parts
    head.pos = pos + vector(0,6,0)
    body.pos = pos

    armL.pos = pos + vector(0,5,0)
    armR.pos = pos + vector(0,5,0)

    legL.pos = pos
    legR.pos = pos

    parachute.pos = pos + vector(0,14,0)

    info.pos = vector(25,80,0)

    info.text = (
        "t: " + str(round(t,1)) +
        " s\nv: " + str(round(mag(v),1)) +
        " m/s\na: " + str(round(mag(a),1))
    )

    t = t + dt