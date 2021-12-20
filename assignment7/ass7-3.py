import pyglet
from pyglet.window import key
import ratcave as rc

# Shaders
vert_shader = """
 #version 120
 attribute vec4 vertexPosition;
 uniform mat4 projection_matrix, view_matrix, model_matrix;

 void main()
 {
     gl_Position = projection_matrix * view_matrix * model_matrix * vertexPosition;
 }
 """

frag_shader = """
 #version 120
 uniform vec3 diffuse;
 void main()
 {
     gl_FragColor = vec4(diffuse, 1.);
 }
 """

shader = rc.Shader(vert=vert_shader, frag=frag_shader)

# Create Window
window = pyglet.window.Window()
keys = key.KeyStateHandler()
window.push_handlers(keys)

def update(dt):
    pass
pyglet.clock.schedule(update)

# Insert filename into WavefrontReader.
obj_filename = rc.resources.obj_primitives
obj_reader = rc.WavefrontReader(obj_filename)

# Create Mesh
monkey = obj_reader.get_mesh("Monkey")
monkey.position.xyz = 0, 0, -2

# Create Scene
scene = rc.Scene(meshes=[monkey])

def move_camera(dt):
    camera_speed = 3
    if keys[key.LEFT]:
        scene.camera.position.x -= camera_speed * dt
    if keys[key.RIGHT]:
        scene.camera.position.x += camera_speed * dt
pyglet.clock.schedule(move_camera)

@window.event
def on_draw():
    with shader:
        scene.draw()

pyglet.app.run()