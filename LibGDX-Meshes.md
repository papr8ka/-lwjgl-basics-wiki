##### [start](https://github.com/mattdesl/lwjgl-basics/wiki) » LibGDX Meshes

***

This tutorial will cover Mesh and ImmediateModeRenderer utilities in LibGDX, and using custom shaders to create highly performant and specialized effects. Before starting, you should get familiar with the following:

- [Texture Handling](https://github.com/mattdesl/lwjgl-basics/wiki/LibGDX-Textures)
- [Shaders](https://github.com/mattdesl/lwjgl-basics/wiki/Shaders) - you should read up to Lesson 2, at least
- [Sprite Batch Basics](https://github.com/mattdesl/lwjgl-basics/wiki/Sprite-Batching)

## Table of Contents

  * [Lesson 1](LibGDX-Meshes-Lesson-1): Rendering a batch of Triangles
  * Lesson 2: Understanding indices
  * Lesson 3: Using ImmediateModeRenderer for Prototyping
  * Lesson 4: Practical Applications 

## Intro to Vertices & Meshes

As discussed in the earlier tutorials; a single vertex can hold information about Position, Color, Texture Coordinates, or whatever else we would like to pass to the shaders. If we wanted to make a 2D white triangle, we would use three vertices, each one holding a `Position` attribute with `(x, y)` components.

OpenGL doesn't know the concept of a Mesh; this is a LibGDX utility. In LibGDX, a Mesh is really just a big array of vertices. It's important to understand that a Mesh doesn't need to represent a _single_ primitive object; in fact, you should generally try to pack as much data into one Mesh as you can. For example; if we wanted to render many rectangular sprites (made up of two triangles each), we would try to fit all of this data into a single Mesh, and push all the data to GL in a single render call.

## Get Started

Move onto [Lesson 1](LibGDX-Meshes-Lesson-1) to get started.