A common feature in 2D and 3D graphics programming is the ability to render to a texture. For example, say we have a slider GUI component made up of multiple sprites (the track, and the thumb button), and we are trying to fade it in/out. When we render each sprite at 50% opacity, we get some ugly blending where the sprites meet. The solution is to render the entire component at 100% opacity to an "offscreen texture", **then** render the offscreen texture to the screen at 50%.

![Opacity](http://i.imgur.com/RsM5G.png)

(Slider PSD can be downloaded [here](http://files.pixelsdaily.com/download/id/2950))

Another use for render-to-texture is for post-processing effects; i.e. rendering your sprites to an offscreen texture as large as the game window, and then render that texture to the screen 

## Frame Buffer Objects

In OpenGL, in order to render to texture, we need to set up a Frame Buffer Object (FBO). We will use the Framebuffer utility to make things a bit easier. You can loosely think of FBOs as a means of "switching screens" in GL. Generally you render to the default "screen" of the Display (or **back buffer**), but with an FBO you can define other screens to render to. 

First, we create a new frame buffer object:
```java
try {
	fbo = new Framebuffer(width, height, Texture.NEAREST);
} catch (LWJGLException e) {
	... if the FBO could not be created ...
}
```

For maximum compatibility and efficiency, you should stick to power-of-two sizes. The frame buffer is backed by a texture, so it has the same hardware limitations discussed in the [Textures tutorial](Textures#wiki-HardwareLimitations).

You can check to see if frame buffer objects are supported in hardware with `Framebuffer.isSupported()`. If it returns `false`, then you will get an error when you try to create a frame buffer. This is generally only a problem on very old drivers, most of which will not work with shaders anyways, and so are not worth our time. To give you an idea of support, about [93% of drivers](http://feedback.wildfiregames.com/report/opengl/) support `GL_EXT_framebuffer_object`. Users that don't support this are probably not going to be able to run shaders, either, and you'd be better off telling them to update their graphics card and drivers.

Here is some pseudo-code to render-to-texture using a frame buffer object:

```
//make the FBO the current buffer
fbo.begin()

//... clear the FBO buffer ...
glClear(...)

//since the FBO may not be the same size as the display, 
//we need to give the SpriteBatch our new screen dimensions
batch.resize(fbo.getWidth(), fbo.getHeight());

//render some sprites 
batch.begin();
  ...
batch.end(); //flushes data to GL

//now we can unbind the FBO, returning rendering back to the default back buffer (the Display)
fbo.end();

//reset the batch back to the Display width/height
batch.resize(Display.getWidth(), Display.getHeight());

//now we are rendering to the back buffer (Display) again
batch.begin();

//draw our offscreen FBO texture to the screen
batch.draw(fbo, 0, 0);

batch.end();
```

## Under the Hood

A frame