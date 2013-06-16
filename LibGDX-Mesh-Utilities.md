This tutorial will cover Mesh and ImmediateModeRenderer utilities in LibGDX, and using custom shaders to create highly performant and specialized effects. Before starting, you should get familiar with the following:

- [Texture Handling](https://github.com/mattdesl/lwjgl-basics/wiki/LibGDX-Textures)
- [Shaders](https://github.com/mattdesl/lwjgl-basics/wiki/Shaders) - you should at least up to Lesson 2
- [Sprite Batch Basics](https://github.com/mattdesl/lwjgl-basics/wiki/Sprite-Batching)

[TOC]

## Intro to Vertices & Meshes

As discussed in the earlier tutorials; a single vertex can hold information about Position, Color, Texture Coordinates, or whatever else we would like to pass to the shaders. If we wanted to make a 2D white triangle, we would use three vertices, each one holding a `Position` attribute with `(x, y)` components.

OpenGL doesn't know the concept of a Mesh; this is a LibGDX utility. In LibGDX, a Mesh is really just a big array of vertices. It's important to understand that a Mesh doesn't need to represent a _single_ primitive object; in fact, you should generally try to pack as much data into one Mesh as you can. For example; if we wanted to render two triangles to create a rectangular quad, we would put all of their data into the same array, and thus the same Mesh, and call render once. Likewise; if we planned to develop our own sprite batcher, we would want to store potentially hundreds of triangles in the same Mesh, so that we can render them all in a single call. 

## Mesh Example: Quads

### Vert & Frag Shaders

Let's say we want to render some quads (i.e. two triangles) of different colours. The best way to do this is to use a `Position` attribute which holds the `(x, y)` components, and a `Color` attribute which holds the `(r, g, b, a)` components. First, we need to construct a shader for our mesh.

Vertex shader:
```glsl
//our attributes
attribute vec2 a_position;
attribute vec4 a_color;

//our camera matrix
uniform mat4 u_projTrans;

//send the color out to the fragment shader
varying vec4 vColor;

void main() {
	vColor = a_color;
	gl_Position = u_projTrans * vec4(a_position.xy, 0.0, 1.0);
}
```

Fragment shader:
```glsl
#ifdef GL_ES
precision mediump float;
#endif

//input from vertex shader
varying vec4 vColor;

void main() {
	gl_FragColor = vColor;
}
```