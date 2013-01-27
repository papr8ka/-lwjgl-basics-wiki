### OpenGL & GLSL Tutorials

This is a series of tutorials aimed at LWJGL and LibGDX devs looking to learn more about OpenGL, shaders and the programmable pipeline.

The tutorial series uses the lwjgl-basics API to reduce clutter and keep things readable. However, many lessons include "Under the Hood" sections, which go into more detail on the specific OpenGL calls required to set up the various wrapper objects (e.g. Texture, Game, etc).

* [Display Creation](wiki/Display) 
* [OpenGL Textures](wiki/Textures)
  * [Using Buffers with LWJGL](wiki/Java-NIO-Buffers)
* [Batching Sprites](wiki/Sprite-Batching)
  * [Batching Rectangles and Lines](wiki/Batching-Rectangles-and-Lines)
* [Frame Buffer Objects](wiki/FrameBufferObjects)
* [Intro to Shaders](wiki/Shaders)
  * [Lesson 1: Red Boxes](wiki/ShaderLesson1)
  * [Lesson 2: Inverting a Texture](wiki/ShaderLesson2)
  * [Lesson 3: Circles, vignette, sepia and grayscale effects](wiki/ShaderLesson3)
  * [Lesson 4: Multiple Texture Units](wiki/ShaderLesson4)
  * [Lesson 5: Gaussian Blurs](wiki/ShaderLesson5)
      * [Blurs for Mobile Applications in LibGDX](wiki/OpenGL-ES-Blurs)
  * Lesson 6 (WIP) will cover normal map lighting for 2D games. See [here](http://www.java-gaming.org/topics/glsl-using-normal-maps-to-illuminate-a-2d-texture-libgdx/27516/view.html) for now.
  * Lesson 7 (WIP) will cover light scattering, aka "god rays".
* 5. Creating Your own 2D Renderer
  * [ShaderProgram Utility](wiki/ShaderProgram-Utility)
  * [Sprite Batching](wiki/SpriteBatch)

### Code Snippets & Tips

* LibGDX
  * [Using Normal Maps to Light a 2D Texture (GLSL)](http://www.java-gaming.org/topics/glsl-using-normal-maps-to-illuminate-a-2d-texture-libgdx/27516/view.html)
  * [Using Java2D For Advanced Shapes & Rasterization (Desktop)](wiki/LibGDX-&-Java2D)
  * [Rendering a Textured Triangle with SpriteBatch](https://gist.github.com/4255476)
  * [Hiding the Mouse Cursor (Desktop)](https://gist.github.com/4255483)
  * [Sprite Brightness/Contrast in GL11 and GL20](wiki/LibGDX-Brightness-&-Contrast)
* GLSL Sandbox
  * [Outlined Circle](http://glsl.heroku.com/e#4635.0)
  * [Procedural Bricks](http://glsl.heroku.com/e#5215.13)
  * [Spotlight WIP](http://glsl.heroku.com/e#5700.4)
  * [Flying Lotus' Cosmogramma in Code (Album Artwork)](http://glsl.heroku.com/e#5928.5)
* Misc
  * [2D Lightning Effect](wiki/LightningEffect)
  * [Tiled Maps from Images](wiki/Tiled-Map-Images)

***

### The API

You can also use the *lwjgl-basics* source code as a minimal shader-based library for 2D LWJGL sprite games. It provides essential utilities for textures, shaders, and sprite rendering.

For a large game project, a platform like [LibGDX](http://libgdx.badlogicgames.com/) may be more suitable.

The [source code](https://github.com/mattdesl/lwjgl-basics) is hosted on GitHub.

### Installing the API

The best way to install the API is to use Eclipse and EGit (or another IDE with Git support) to pull the most recent source code. Included in the `lib` and `native` folder is a distribution of LWJGL 2.8.5, as well as an Eclipse project with class path set up for you. You can download newer versions of LWJGL from their [downloads page](http://lwjgl.org/download.php). 

Alternatively, you can download the full library as a ZIP:

![ZIP](http://i.imgur.com/Dkvp0.png)

Then, simply open the Eclipse project to start testing. Ensure your LWJGL JARs and natives have been set correctly in [Eclipse](http://www.lwjgl.org/wiki/index.php?title=Setting_Up_LWJGL_with_Eclipse), [NetBeans](http://www.lwjgl.org/wiki/index.php?title=Setting_Up_LWJGL_with_NetBeans) or [IntelliJ](http://www.lwjgl.org/wiki/index.php?title=Setting_Up_LWJGL_with_IntelliJ_IDEA), and include lwjgl-basics as a class library. lwjgl-basics also uses PNGDecoder.jar as a dependency, which can be downloaded [here](http://twl.l33tlabs.org/textureloader/).

See the [tests](https://github.com/mattdesl/lwjgl-basics/tree/master/test/mdesl/test) package to get started with some basic examples.