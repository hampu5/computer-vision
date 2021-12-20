import pyglet
from pyglet.window import key
import ratcave as rc

# Shaders
vert_shader = """
#version 130
attribute vec4 vertexPosition;
uniform mat4 projection_matrix, view_matrix, model_matrix;

out vec4 FragPos;
// out vec3 Normal;
// vec3 aPos = gl_Vertex.xyz;
// vec3 aNormal = gl_Normal;

void main()
{
    gl_Position = projection_matrix * view_matrix * model_matrix * vertexPosition;
    // FragPos = vec3(model_matrix * vec4(gl_Position.xyz, 1.0));
    FragPos = gl_Position;
    // Normal = aNormal;
}
"""

frag_shader = """
#version 130
uniform vec3 lightColor;
uniform vec3 objectColor;

in vec4 FragPos;
// in vec3 Normal;

uniform vec3 lightPos;

void main()
{
    // Ambient light
    float ambientStrength = 1;
    vec3 ambient = ambientStrength * lightColor;
    
    // Diffuse light (Lambertian)
    
    vec3  ndc_pos = FragPos.xyz / FragPos.w;
    vec3  dx      = dFdx( ndc_pos );
    vec3  dy      = dFdy( ndc_pos );

    vec3 Normal = normalize(cross(dx, dy));
    Normal *= sign(Normal.z);

    vec3 norm = normalize(Normal);
    vec3 lightDir = normalize(lightPos - FragPos.xyz);
    float diff = max(dot(norm, lightDir), 0.0);
    vec3 diffuse = diff * lightColor;

    //vec3 result = (ambient + diffuse) * objectColor;
    vec3 result = (ambient) * objectColor;
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
monkey.uniforms['lightPos'] = [0, 0, 3]

# Create Scene
scene = rc.Scene(meshes=[monkey])

scene.light = rc.Light

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