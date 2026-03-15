GlowScript 3.2 VPython
floor = box(pos=vector(0,0,0), size=vector(10,0.2,10), color=color.green)
ball = sphere(pos=vector(0,5,0), radius=0.5, color=color.red)
velocity = vector(0,-2,0)

while True:
    rate(100)
    ball.pos = ball.pos + velocity*0.05
    if ball.pos.y <= 0.5:
        velocity.y = -velocity.y