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
