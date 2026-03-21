GlowScript 3.2 VPython

scene.title = "Terminal Velocity & Paratrooper"
scene.background = color.black

# Ground
ground = box(pos=vector(0,-300,0), size=vector(800,10,800), color=color.red)

# Skydiver
body = cylinder(pos=vector(0,200,0), axis=vector(0,-15,0), radius=4, color=color.green)
head = sphere(pos=body.pos+vector(0,6,0), radius=4, color=color.red)

# Parachute
canopy = cone(pos=body.pos+vector(0,30,0),
axis=vector(0,20,0),
radius=35,
color=color.yellow,
visible=False)

# Physics constants
m = 80
g = 9.8
rho = 1.2
Cd = 1
A = 0.7

Cd_parachute = 1.75
A_parachute = 18

v = vector(0,0,0)
t = 0
dt = 0.05
parachute_open = False

# Graphs
g1 = graph(title="Velocity vs Time", xtitle="Time", ytitle="Velocity")
vel_curve = gcurve(color=color.blue)

g2 = graph(title="Acceleration vs Time", xtitle="Time", ytitle="Acceleration")
acc_curve = gcurve(color=color.orange)

# Display text
info = label(pos=vector(-150,180,0),
text="",
box=False,
height=16,
color=color.black)

while body.pos.y > -295:

    rate(200)

    if t > 3 and parachute_open == False:
        parachute_open = True
        Cd = Cd_parachute
        A = A_parachute
        canopy.visible = True

    # Drag force
    drag_mag = 0.5*rho*Cd*A*mag(v)**2
    drag = -drag_mag*norm(v) if mag(v) > 0 else vector(0,0,0)

    gravity = vector(0,-m*g,0)
    F = gravity + drag

    a = F/m

    v = v + a*dt
    body.pos = body.pos + v*dt
    head.pos = body.pos + vector(0,6,0)
    canopy.pos = body.pos + vector(0,30,0)

    # Graphs
    vel_curve.plot(t,v.y)
    acc_curve.plot(t,a.y)

    # Display important quantities
    info.text = "Time: {:.2f} s\nVelocity: {:.2f} m/s\nAcceleration: {:.2f} m/s²\nHeight: {:.2f} m\nParachute: {}".format(
        t, v.y, a.y, body.pos.y, parachute_open)

    t += dt
