### OpenGL & GLSL Tutorials

* 1. [Display Creation](wiki/Display)
* 2. [Textures](wiki/Textures)
  * [Using Buffers with LWJGL](wiki/Java-NIO-Buffers)
* 3. [Intro to Shaders](wiki/Shaders)
  * [Lesson 1: Red Boxes](wiki/ShaderLesson1)
  * [Lesson 2: Inverting a Texture](wiki/ShaderLesson2)
  * [Lesson 3: Circles, vignette, sepia and grayscale effects](wiki/ShaderLesson3)
* 4. Creating Your own 2D Renderer
  * [ShaderProgram Utility](wiki/ShaderProgram-Utility)
  * [Sprite Batching](wiki/SpriteBatch)

### The API

*lwjgl-basics* also acts as a minimal shader-based library for 2D sprite games. It provides essential utilities for textures, shaders, and sprite rendering.

For a large game project, a platform like [LibGDX](http://libgdx.badlogicgames.com/) may be more suitable.

The [source code](https://github.com/mattdesl/lwjgl-basics) is hosted on GitHub.

### Installing the API

The best way to install the API is to use Eclipse and EGit (or another IDE with Git support) to pull from the master branch. Included is a distribution of LWJGL 2.8.5 in `libs/` and `natives/`. You can download newer versions of LWJGL from their [downloads page](http://lwjgl.org/download.php). 

You could also grab a stable JAR of the API from the downloads page. Then, you would set up LWJGL and your natives properly in [Eclipse](http://www.lwjgl.org/wiki/index.php?title=Setting_Up_LWJGL_with_Eclipse), [NetBeans](http://www.lwjgl.org/wiki/index.php?title=Setting_Up_LWJGL_with_NetBeans) or [IntelliJ](http://www.lwjgl.org/wiki/index.php?title=Setting_Up_LWJGL_with_IntelliJ_IDEA), and include lwjgl-basics as a class library.