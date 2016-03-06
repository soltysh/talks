
script = """
from vapory import *

scene = Scene(
    camera = Camera('location', [0, 2, -3], 'look_at', [0, 1, 2]),
    objects = [
        LightSource([2, 4, -3], 'color', [1, 1, 1]),
        Background('color', [1, 1, 1]),
        Sphere([0, 1, 2], 2, Texture(Pigment('color', ([1, 0, 1])))),
        Box([{0}, -1.5, -0.5], [{1}, 3.5, 5], Texture(Pigment('color', ([1, 0.6, 0.5]))), 'rotate', [0, 30, 0]),
    ])

scene.render('/data/{2}.png', width=400, height=400, antialiasing=0.001)
"""

for i in range(20):
    name = str(i).zfill(2)
    with open(name+".py", 'w') as f:
        f.write(script.format(-4+(0.25*i), -3.75+(0.25*i), name))
