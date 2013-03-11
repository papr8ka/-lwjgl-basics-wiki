This is an advanced tutorial that will deal with shaders, meshes, camera matrices, texture handling, and various other concepts. Ensure you have read and understand the following before continuing:

- [Handling Textures in LibGDX](LibGDX-Textures)
- [Shader Tutorial Series](Shaders)
- [Intro to Sprite Batchers](Sprite-Batching)

## Objective

As we know from previous tutorials, we can send information to a shader with *uniforms*. The problem is, however, that we need to flush the SpriteBatch before changing the uniform. Imagine almost all of our sprites require a different uniform value; this would lead to a lot of flushing, defeating the benefits of a SpriteBatch in the first place. 

The solution is to use vertex attributes. This allows us to send data to the shader *per-vertex* as opposed to *per-batch*. There are a number of cases where this would prove useful, but for our purposes we are going to use it for multi-texturing. 

Let's say we have a *huge* 2D RPG with many different tilesets. We want the tiles to "splat" nicely together at edges; such as where the water meets rock, or where grass meets dirt. The typical solution is to pre-render all different possible tile combinations. However, in our theoretical situation, this would lead to an exponential growth in tilesets that we can't afford. So an alternative solution is to use "splat masks" (like we did in [Lesson 4](https://github.com/mattdesl/lwjgl-basics/wiki/ShaderLesson4)) to blend the 