This page is a work in progress.

## Intro to GLSL

GLSL stands for OpenGL Shading Language. Shaders are like small scripts that let us interact with the graphics processor more closely. They are an essential aspect of graphics programming, and can be used for a variety of effects and visuals in your 2D and 3D games. For now, there are two types of shaders you should familiarize yourself with:

### Vertex Shaders

As discussed in the [Textures](https://github.com/mattdesl/lwjgl-basics/wiki/Textures) article, a **vertex** is a point in space with some attributes attached to it, like position (xyz), colour (rgba), texture coordinates (st). A “vertex shader” allows you to interact with this vertex information before sending it along the graphics pipeline to be rendered.

Vertex shaders are often more applicable in 3D graphics programming -- e.g. applying a noise displacement to the vertices of a 3D mesh -- but they are still essential to understand even for 2D games.

### Fragment Shaders

Often called “pixel shaders,” these allow us to modify individual pixels before they are sent along the graphics pipeline. These shaders “output” a RGBA colour. Think of it like a return statement: if we rendered a sprite with a fragment shader that only returned the colour red `(R=1, G=0, B=0, A=1)` – the result would be a red box! 

## How it Works

Let's go back to the brick sprite we were using in the [Textures](https://github.com/mattdesl/lwjgl-basics/wiki/Textures) tutorial:  
![Brick](http://i.imgur.com/IGn1g.png)

As we explained in the Textures tutorial, we need to give OpenGL four **vertices** to make up our quad. Each **vertex** contains a number of **attributes**, such as `Position` and `TexCoord`. Refer to this image again:  
![Quad](http://i.imgur.com/fkzfb.png)

Another attribute that is not shown in the above image is `Color`. Generally, we'll use opaque white `(R=1, G=1, B=1, A=1)` for each vertex, in order to render the sprite with full opacity.

## Where to start?

Before jumping straight into your shader-based sprite renderer, it would be smart to experiment with GLSL in order to become a little more comfortable with concepts like uniforms and attributes. For this I recommend using a library or tool that will set up shaders for you, allowing you to jump right into GLSL code. For this tutorial series, we will follow the tests in [lwjgl-basics](https://github.com/mattdesl/lwjgl-basics/tree/master/test/mdesl/test/shadertut). There are also online GLSL editors, if you have a WebGL-enabled browser, which are extremely useful for learning various concepts:
- http://glsl.heroku.com/
- http://www.iquilezles.org/apps/shadertoy/

Once you feel more comfortable with the basics of GLSL, you can start looking "under the hood" to see how it all comes together in a custom renderer.

## Hello World

Continue to Lesson 1 to get started.