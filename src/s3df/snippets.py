INDENT = "  "

#### PRIMITIVES ####

SPHERE_SNIPPET = """
float sdSphere( vec3 p, float s )
{
  return length(p)-s;
}
"""

BOX_SNIPPET = """
float sdBox( vec3 p, vec3 b )
{
  vec3 q = abs(p) - b;
  return length(max(q,0.0)) + min(max(q.x,max(q.y,q.z)),0.0);
}
"""

CUBE_SNIPPET = BOX_SNIPPET

TORUS_SNIPPET = """
float sdTorus( vec3 p, vec2 t )
{
  vec2 q = vec2(length(p.xz)-t.x,p.y);
  return length(q)-t.y;
}
"""

CAPPEDCYLINDER_SNIPPET = """
float sdCappedCylinder( vec3 p, float h, float r )
{
  vec2 d = abs(vec2(length(p.xz),p.y)) - vec2(h,r);
  return min(max(d.x,d.y),0.0) + length(max(d,0.0));
}
"""

#### OPERATIONS ####

UNION_SNIPPET = """float opUnion( float d1, float d2 ) { return min(d1,d2); }"""

SUBTRACTION_SNIPPET = (
    """float opSubtraction( float d1, float d2 ) { return max(-d1,d2); }"""
)

INTERSECTION_SNIPPET = (
    """float opIntersection( float d1, float d2 ) { return max(d1,d2); }"""
)

REPEAT_SNIPPET = """
vec3 opRep(in vec3 p, in vec3 c)
{
    return mod(p+0.5*c,c)-0.5*c;
}
"""

SMOOTHUNION_SNIPPET = """
float opSmoothUnion( float d1, float d2, float k ) {
    float h = clamp( 0.5 + 0.5*(d2-d1)/k, 0.0, 1.0 );
    return mix( d2, d1, h ) - k*h*(1.0-h); }
"""

SMOOTHSUBTRACT_SNIPPET = """
float opSmoothSubtraction( float d1, float d2, float k ) {
    float h = clamp( 0.5 - 0.5*(d2+d1)/k, 0.0, 1.0 );
    return mix( d2, -d1, h ) + k*h*(1.0-h); }
"""

SMOOTHINTERSECTION_SNIPPET = """
float opSmoothIntersection( float d1, float d2, float k ) {
    float h = clamp( 0.5 - 0.5*(d2-d1)/k, 0.0, 1.0 );
    return mix( d2, d1, h ) + k*h*(1.0-h); }
"""

TWIST_SNIPPET = """
vec3 opTwist(in vec3 p, float k)
{
    // const float k = 10.0; // or some other amount
    float c = cos(k*p.y);
    float s = sin(k*p.y);
    mat2  m = mat2(c,-s,s,c);
    vec3  q = vec3(m*p.xz,p.y);
    return q;
}
"""