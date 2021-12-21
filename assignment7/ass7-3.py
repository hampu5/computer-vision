import pyglet
from pyglet.window import key
import ratcave as rc

# Shaders
vert_shader = """
attribute vec4 vertexPosition;
attribute vec4 normalPosition;
uniform mat4 projection_matrix, view_matrix, model_matrix, normal_matrix;

varying vec3 FragPos;
varying vec3 Normal;

void main()
{
    gl_Position = projection_matrix * view_matrix * model_matrix * vertexPosition;
    FragPos = vec3(model_matrix * vertexPosition);
    Normal = normalize(normal_matrix * normalPosition).xyz;
}
"""

frag_shader = """
uniform vec3 lightColor;
uniform vec3 objectColor;

uniform vec3 lightPos;

varying vec3 FragPos;
varying vec3 Normal;

void main()
{
    // Ambient light
    float ambientStrength = 0.3;
    vec3 ambient = ambientStrength * lightColor;
    
    // Diffuse light (Lambertian)
    vec3 lightDir = normalize(lightPos - FragPos);
    float diff = max(dot(Normal, lightDir), 0.0);
    vec3 diffuse = diff * lightColor;

    vec3 result = (ambient + diffuse) * objectColor;
    gl_FragColor = vec4(result, 1.0);
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

monkey.uniforms['objectColor'] = [.2, .3, .5]
monkey.uniforms['lightColor'] = [.8, .8, .1]
monkey.uniforms['lightPos'] = [.0, .0, 3.]

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