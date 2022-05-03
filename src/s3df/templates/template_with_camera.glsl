#version 330

#ifdef VERTEX_SHADER

in vec3 in_position;
in vec2 in_texcoord_0;

out vec2 uv0;

void main() {
    gl_Position = vec4(in_position, 1.0);
    uv0 = in_texcoord_0;
}

#elif FRAGMENT_SHADER

out vec4 outColor;
in vec2 uv0;

uniform float iTime;
uniform vec2 iResolution;
uniform vec2 iMouse;


// Adapted from: https://inspirnathan.com/posts/60-shadertoy-tutorial-part-14/
const int MAX_MARCHING_STEPS = 255;
const float MIN_DIST = 0.0;
const float MAX_DIST = 100.0;
const float PRECISION = 0.001;
const float EPSILON = 0.0005;
const float PI = 3.14159265359;
const vec3 COLOR_BACKGROUND = vec3(.1, .4, .5);
const vec3 COLOR_AMBIENT = vec3(0.2, 0.2, 0.1);

{{ snippets }}

float scene(vec3 p) {
    return {{ main_shader }};
}

float rayMarch(vec3 ro, vec3 rd) {
    float depth = MIN_DIST;
    float d;// distance ray has travelled

    for (int i = 0; i < MAX_MARCHING_STEPS; i++) {
        vec3 p = ro + depth * rd;
        d = scene(p);
        depth += d;
        if (d < PRECISION || depth > MAX_DIST) break;
    }

    d = depth;
    return d;
}

vec3 calcNormal(in vec3 p) {
    vec2 e = vec2(1, -1) * EPSILON;
    return normalize(
    e.xyy * scene(p + e.xyy) +
    e.yyx * scene(p + e.yyx) +
    e.yxy * scene(p + e.yxy) +
    e.xxx * scene(p + e.xxx));
}

mat2 rotate2d(float theta) {
    float s = sin(theta), c = cos(theta);
    return mat2(c, -s, s, c);
}

mat3 camera(vec3 cameraPos, vec3 lookAtPoint) {
    vec3 cd = normalize(lookAtPoint - cameraPos);
    vec3 cr = normalize(cross(vec3(0, 1, 0), cd));
    vec3 cu = normalize(cross(cd, cr));

    return mat3(-cr, cu, -cd);
}

void mainImage(out vec4 fragColor, in vec2 fragCoord)
{
    vec2 uv = (fragCoord-.5*iResolution.xy)/iResolution.y;
    vec2 mouseUV = iMouse.xy/iResolution.xy;

    if (mouseUV == vec2(0.0)) mouseUV = vec2(0.5);// trick to center mouse on page load

    vec3 col = vec3(0);
    vec3 lp = vec3(0);
    vec3 ro = vec3(0, 0, 10);// ray origin that represents camera position

    float cameraRadius = 2.;
    ro.yz = ro.yz * cameraRadius * rotate2d(mix(-PI/2., PI/2., mouseUV.y));
    ro.xz = ro.xz * rotate2d(mix(-PI, PI, mouseUV.x)) + vec2(lp.x, lp.z);

    vec3 rd = camera(ro, lp) * normalize(vec3(uv, -1));// ray direction

    float d = rayMarch(ro, rd);// signed distance value to closest object

    if (d > MAX_DIST) {
        col = COLOR_BACKGROUND;// ray didn't hit anything
    } else {
        vec3 p = ro + rd * d;// point discovered from ray marching
        vec3 normal = calcNormal(p);// surface normal

        vec3 lightPosition = vec3(0, MAX_DIST, MAX_DIST);
        vec3 lightDirection = normalize(lightPosition - p) * .55;// The 0.65 is used to decrease the light intensity a bit

        float dif = clamp(dot(normal, lightDirection), 0., 1.) * 0.5 + 0.5;// diffuse reflection mapped to values between 0.5 and 1.0

        col = vec3(dif) + COLOR_AMBIENT;
    }

    fragColor = vec4(col, 1.0);
}

void main() {
    mainImage(outColor, gl_FragCoord.xy);
}
#endif
