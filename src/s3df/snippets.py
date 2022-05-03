INDENT = "  "

#### PRIMITIVES ####

SPHERE_SNIPPET = """
float sdSphere( vec3 p, float s )
{
  return length(p)-s;
}
"""

CUBE_SNIPPET = """
float sdBox( vec3 p, vec3 b )
{
  vec3 q = abs(p) - b;
  return length(max(q,0.0)) + min(max(q.x,max(q.y,q.z)),0.0);
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
