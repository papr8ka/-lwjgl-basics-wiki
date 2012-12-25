##### [start](https://github.com/mattdesl/lwjgl-basics/wiki) » [Shaders](Shaders) » Lesson 5: Blurring & Bloom

***

This series relies on the minimal [lwjgl-basics](https://github.com/mattdesl/lwjgl-basics) API for shader and rendering utilities. The code has also been [Ported to LibGDX](#Ports). The concepts should be universal enough that they could be applied to [Love2D](https://love2d.org/), [GLSL Sandbox](http://glsl.heroku.com/), iOS, or any other platforms that support GLSL. 

***

## Setup

This lesson requires understanding the Frame Buffer Object (FBO), so [read up on them](FrameBufferObjects) if you haven't already. Also ensure you are well-versed on the basics of [sprite batching](Sprite-Batching).

The lesson will demonstrate a [gaussian blur](http://en.wikipedia.org/wiki/Gaussian_blur) technique in GLSL inspired by [this article](http://www.gamerendering.com/2008/10/11/gaussian-blur-filter-shader/). The blur is applied in two passes -- horizontally and vertically -- however, our implementation will only require a single fragment shader. 

Here is a visual overview of the two-pass blurring process:

![Overview1](http://i.imgur.com/8jkTJ.png)

(click for full view)

You can follow along with the source [here](https://github.com/mattdesl/lwjgl-basics/blob/master/test/mdesl/test/shadertut/ShaderLesson5.java). We first load some textures, as usual, then we set up our frame buffers:

```java
//create our FBOs
blurTargetA = new FrameBuffer(FBO_SIZE, FBO_SIZE, Texture.NEAREST);
blurTargetB = new FrameBuffer(FBO_SIZE, FBO_SIZE, Texture.NEAREST);
```



<a name="Ports" />

## Other APIs

work in progress