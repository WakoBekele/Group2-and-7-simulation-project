Web VPython 3.2 
from vpython import *

# --- 1. Scene & Environment ---
scene = canvas(title="Physics Lab: High-Speed Jump", width=800, height=600)
scene.background = color.black  
scene.range = 150
scene.center = vector(0, 150, 0)

# --- 2. Dashboard Labels ---
label_time = label(text='Time: 0 s', align='left', box=False, height=14)
label_vel = label(text='Velocity: 0 m/s', align='left', box=False, height=14)
label_acc = label(text='Acceleration: 0 m/s^2', align='left', box=False, height=14)
label_stage = label(text='Stage 1: High Velocity Fall', align='left', box=False, color=color.cyan, height=16)
label_desc = label(text='Gravity is pulling hard.', align='left', box=False, opacity=0.8, height=12)

# --- 3. World Elements ---
# Target is now at 500m to account for the plane's forward speed
target_pos = vector(500, 0, 0)
ground = box(pos=vector(400, -2, 0), size=vector(2000, 4, 1000), color=color.green)
target = cylinder(pos=target_pos, axis=vector(0,0.5,0), radius=40, color=color.red)
plane = box(pos=vector(0, 305, 0), size=vector(80, 10, 20), color=color.gray(0.4))
plane_vel = vector(60, 0, 0) # Faster Plane

# --- 4. The Thin Paratrooper Model ---
head = sphere(radius=3.5, color=color.orange)
body = cylinder(axis=vector(0, 12, 0), radius=1.0, color=color.blue)
arm_r = cylinder(axis=vector(6, -1.5, 0), radius=0.4, color=color.blue)
arm_l = cylinder(axis=vector(-6, -1.5, 0), radius=0.4, color=color.blue)
leg_r = cylinder(axis=vector(2, -9, 0), radius=0.5, color=color.blue)
leg_l = cylinder(axis=vector(-2, -9, 0), radius=0.5, color=color.blue)
chute = sphere(size=vector(70, 20, 70), color=color.red, visible=False, opacity=0.8)

# --- 5. Physics Constants ---
m = 75             
g = vector(0, -9.8, 0)
rho = 1.225        
dt = 0.04 # DOUBLED: Math moves twice as fast
t = 0

C_body, A_body = 1.0, 0.4  # Very thin
C_chute, A_chute = 1.5, 60.0
deploy_alt = 120  # Lowered deployment for more speed

# Initial state
pos = vector(0, 300, 0) 
vel = vector(60, 0, 0) # Jumping at 60 m/s
chute_open = False

# --- 6. Simulation Loop ---
while pos.y > 0:
    rate(100) # DOUBLED: Animation runs at 100 FPS
    
    # Physics Calculation
    C = C_chute if chute_open else C_body
    A = A_chute if chute_open else A_body
    
    f_drag = -0.5 * rho * mag(vel)**2 * C * A * norm(vel)
    f_net = (m * g) + f_drag
    accel_v = f_net / m
    
    vel = vel + accel_v * dt
    pos = pos + vel * dt
    t += dt

    # UI Logic
    v_vertical = abs(vel.y)
    a_mag = mag(accel_v)

    if not chute_open:
        if v_vertical < 20:
            label_stage.text = "Stage 1: Rapid Acceleration"
            label_desc.text = "The diver is picking up speed fast."
        else:
            label_stage.text = "Stage 2: High Speed Drift"
            label_desc.text = "Air resistance is fighting back."
            
    if pos.y <= deploy_alt and not chute_open:
        chute_open = True
        chute.visible = True
        label_stage.text = "Stage 3: DEPLOYMENT"
        label_stage.color = color.red
        label_desc.text = "Brakes on! Decelerating for landing."
        body.color=arm_r.color=arm_l.color=leg_r.color=leg_l.color=color.yellow

    # Update Visuals
    body.pos = pos
    head.pos = pos + vector(0, 12, 0)
    arm_r.pos = pos + vector(0, 9, 0)
    arm_l.pos = pos + vector(0, 9, 0)
    leg_r.pos = pos
    leg_l.pos = pos
    chute.pos = pos + vector(0, 30, 0)
    plane.pos = plane.pos + plane_vel * dt
    
    scene.center = pos + vector(20, 10, 0)

    # HUD Positioning
    ui_offset = scene.center + vector(-120, 110, 0)
    label_time.pos = ui_offset
    label_vel.pos = ui_offset + vector(0, -15, 0)
    label_acc.pos = ui_offset + vector(0, -30, 0)
    label_stage.pos = ui_offset + vector(0, -55, 0)
    label_desc.pos = ui_offset + vector(0, -85, 0)

    label_time.text = "Time: " + str(round(t, 1)) + " s"
    label_vel.text = "Velocity: " + str(round(mag(vel), 1)) + " m/s"
    label_acc.text = "Acceleration: " + str(round(a_mag, 1)) + " m/s^2"

# --- 7. Final Score ---
distance_from_target = mag(pos - target_pos)
print("---------- JUMP COMPLETE ----------")
print("Distance from Target: " + str(round(distance_from_target, 1)) + " meters")
if distance_from_target < 40:
    print("BULLSEYE! Perfect Landing.")
else:
    print("Good landing, but you missed the mark!")
