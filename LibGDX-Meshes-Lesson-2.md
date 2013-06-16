##### [start](https://github.com/mattdesl/lwjgl-basics/wiki) » [LibGDX Meshes](LibGDX-Meshes) » Lesson 2

***

This tutorial is part of a series. Take a look at the [Introduction](LibGDX-Meshes) before you move on.

# Prototyping with ImmediateModeRenderer

Now that you understand the concepts of how meshes and vertices come together to form geometry, we can utilize LibGDX's ImmediateModeRenderer for some faster prototyping. This is a specialized utility which is good for un-indexed geometry (something we will cover in the next lesson) that holds `Position(x, y, z)` and some other optional attributes: `Normal(x, y, z)`, `Color(r, g, b, a)`, and a variable number of `TexCoord(s, t)`. 

## Setting up the renderer

First, we need to set up the renderer. This will create a default shader for us that has the vertex attributes we specified in the constructor:

```java
    //normals=false, colors=true, numTexCoords=no texture info
    r = new ImmediateModeRenderer20(false, true, 0);
```

Normals are generally not needed for 2D rendering. Colors and texture coordinates are optional, and dependent on your needs. For our triangle renderer, we do need colors, but not texture coordinates. 

When rendering, we use it like so. Notice that it uses a `vec3` for position; we can just ignore the Z component.
```java
//passes the projection matrix to the camera
r.begin(camera.combined, GL20.GL_TRIANGLES);

//renders a single triangle...

//specify normals/colors/texcoords before vertex position
r.color(color.r, color.g, color.b, color.a);
r.vertex(x, y, 0);

r.color(color.r, color.g, color.b, color.a);
r.vertex(x, y+height, 0);

r.color(color.r, color.g, color.b, color.a);
r.vertex(x+width, y, 0);

//flush the renderer
r.end();
```

The ImmediateModeRenderer does not do any bounds checking, so you will have to do that yourself before sending new vertex data!

## Custom Shaders with ImmediateModeRenderer

If we wanted to specify a custom shader, it should be passed in the constructor. Other than `Position` being a vec3, the other thing worth noting is that it uses the constants in ShaderProgram for the attribute names:
```
POSITION_ATTRIBUTE = "a_position"
NORMAL_ATTRIBUTE = "a_normal"
COLOR_ATTRIBUTE = "a_color"
TEXCOORD_ATTRIBUTE = "a_texCoord" + N
```

The texture coordinate is appended with the index; so if we specified a single texCoord, its attribute name in the shader would be `a_texCoord0`. If we did not specify these attributes when constructing ImmediateModeRenderer, then you should not include them in your vertex shader.

The uniform for the projection matrix is named `u_projModelView` and the texture uniforms will be `u_samplerN` (again, where N is the index).