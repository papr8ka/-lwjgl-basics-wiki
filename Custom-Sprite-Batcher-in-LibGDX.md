This is an advanced tutorial that will deal with shaders, meshes, camera matrices, texture handling, and various other concepts. Ensure you have read and understand the following before continuing:

- [Handling Textures in LibGDX](LibGDX-Textures)
- [Shader Tutorial Series](Shaders)
- [Intro to Sprite Batchers](Sprite-Batching)

## Objective

As we know from previous tutorials, we can send float data to a shader with *uniforms* (vec2, vec3, etc). The problem is, however, that we need to flush the SpriteBatch before changing the uniform. Imagine each of our sprites require a different uniform value; this would lead to a lot of flushing, and it defeats the benefits of a SpriteBatch in the first place. 

The solution is to use *vertex attributes* -- this allows us to send data to the shader *per-vertex* as opposed to *per-batch*. We already use vertex attributes to send RGBA colors per sprite, or texture coordinates per vertex. There are a number of situations where custom vertex data will prove useful, but for our cases let's use it for multi-texturing.

## Theoretical Puzzle Game

Let's say we're developing a simple puzzle game with many varieties of jigsaw pieces. Here are a couple of them:  
![Jigsaw](http://i.imgur.com/KBVfvqV.png)

Here is an example of a photo we'd like to slice up:  
![Photo](http://i.imgur.com/sqSPwpa.png)

We could develop this app in a number of ways, but for the purpose of the tutorial we'll implement a solution that applies the mask in real-time. This means that our "photo" source could actually be a dynamic image (like a rotating 3D cube), or a video (like webcam input). 

We can use similar techniques discussed in [Shader Lesson 4](ShaderLesson4), and probably achieve sufficient framerates. But for more optimized rendering, such as a scene with *many* jigsaw pieces, we may need a different technique. The two most important optimizations in 2D are:

- Reducing texture binds by packing all sprites into a TextureAtlas.
- Sending multiple sprites to the GPU at once; also known as "batching" your sprites in a single draw call.
