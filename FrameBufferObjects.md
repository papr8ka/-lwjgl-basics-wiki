A common feature in 2D and 3D graphics programming is the ability to render to a texture. For example, say we have a slider GUI component made up of multiple sprites (the track, and the thumb button), and we are trying to fade it in/out. When we render each sprite at 50% opacity, we get some ugly blending where the sprites meet. The solution is to render the entire component at 100% opacity to an "offscreen texture", **then** render the offscreen texture to the screen at 50%.

![Opacity](http://i.imgur.com/RsM5G.png)

(Slider PSD can be downloaded [here](http://files.pixelsdaily.com/download/id/2950))

Another use for render-to-texture is for post-processing effects; i.e. rendering your sprites to an offscreen texture as large as the game window, and then render that texture to the screen 

## Frame Buffer Objects

In OpenGL, in order to render to texture, we need to set up a Frame Buffer Object (FBO). We will use the Framebuffer utility to make things a bit easier. You can loosely think of FBOs as a means of "switching screens" in GL. Generally you render to the default "screen" of the Display (or **back buffer**), but with an FBO you can define other screens to render to. 

First, we create a new frame buffer object:
```java
fbo = new Framebuffer(512, 512);
```

For maximum compatibility and efficiency, you should stick to power-of-two sizes. The frame buffer is backed by a texture, so it has the same hardware limitations discussed in the [Textures tutorial](Textures#HardwareLimitations).

## Under the Hood

A frame