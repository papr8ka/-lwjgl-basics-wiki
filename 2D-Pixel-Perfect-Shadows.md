![Screenshot](http://i.imgur.com/sJiUG6x.png)

## Intro

Detailed here is an approach to 2D pixel-perfect shadows using shaders and the GPU. Because of the high fill rate and multiple passes involved, this is generally less performant than geometry shadows (which are not per-pixel). My technique is implemented in LibGDX, although the concepts can be applied to any OpenGL/GLSL framework.

The basic steps involved are (1) render occluders to a FBO, (2) build a 1D shadow map, (3) render shadows and sprites.  
![Img](http://i.imgur.com/vcaWNof.png)

The following animation best demonstrates what's happening:   
![Visual](http://i.imgur.com/qcH7G.gif)

The idea is an extension of my [previous attempts](http://www.java-gaming.org/topics/starbound-lighting-techneques/26363/msg/230988/view.html#msg230988) at shader-based shadows, which combines [ideas from various sources](#further-reading). However, "nego" on LibGDX forums suggested some great ideas to reduce the process into fewer passes.

## Step 1: Render To Occlusion Map

The first step is to render an "occlusion map" to an FBO. This way, our shader can sample our scene and determine whether an object is a shadow-caster (opaque), or not a shadow-caster (transparent). Our algorithm will expect the light to be at the center of this "occlusion map." We use a square power-of-two size for simplicity's sake; this will be the size of our light falloff, as well as the size of our various FBOs. The larger the size, the greater the falloff, but also the more fill-limited our algorithm will become.

To do this in LibGDX, we first need to set up a Frame Buffer Object like so:

```java
//lightSize is 256 by default

//create a FrameBufferObject with proper format and no depth
occludersFBO = new FrameBuffer(Format.RGBA8888, lightSize, lightSize, false);
```

Later we may want to "debug" our shadow rendering by drawing the resulting occlusion map to the screen. For this we need to define a TextureRegion for our FrameBuffer, which is done like so:
```java
//get color buffer texture of FBO for region
occluders = new TextureRegion(occludersFBO.getColorBufferTexture());
//flip it on Y-axis due to OpenGL coordinate system
occluders.flip(false, true);
```

If we don't plan on rendering the occluder map to the screen, we can skip the TextureRegion.

During our rendering pass, we draw to the occlusion map like so:
```java
//bind the occluder FBO
occludersFBO.begin();

//clear the FBO
Gdx.gl.glClearColor(0f,0f,0f,0f);
Gdx.gl.glClear(GL10.GL_COLOR_BUFFER_BIT);

//set the orthographic camera to the size of our FBO
cam.setToOrtho(false, occludersFBO.getWidth(), occludersFBO.getHeight());

//translate camera so that light is in the center 
cam.translate(mx - lightSize/2f, my - lightSize/2f);

//update camera matrices
cam.update();

//set up our batch for the occluder pass
batch.setProjectionMatrix(cam.combined);

//reset to default shader
batch.setShader(null); 
batch.begin();

  ... draw any sprites that cast shadows here ....
  ... opaque pixels will be shadow-casters, transparent pixels will not ...

//end the batch before unbinding the FBO
batch.end();

//unbind the FBO
occludersFBO.end();
```

We could use a custom shader here to encode specific data into our occlusion pass (such as [normals for diffuse lighting](https://github.com/mattdesl/lwjgl-basics/wiki/ShaderLesson6)). But for now we'll just use the default SpriteBatch shader, and only rely on sampling from the alpha channel. The resulting "occlusion map" might look like this -- with the light at center -- if we were to render the alpha channel in black and white:  
![Occlusion](http://i.imgur.com/UWy7D1V.png)

## Step 2: Build a 1D Shadow Map Lookup Texture

Now we need to build a 1D lookup texture, which will be used as our shadow/light map. The texture is very small (256x1 pixels), and looks like this:  

![ShadowMap](http://i.imgur.com/ZaGDDgL.png)

Our x-axis represents the angle `theta` of a "light ray" from center; i.e. 360 degrees of a circle. An easy way to visualize it is to imagine a few rays, like in the following:  
![Shadow2D](http://i.imgur.com/tJR0QSz.png)

On the left, we see each ray being cast from the center (light position) to the first occluder (opaque pixel in our occlusion map). 

The texture on the right represents the "polar transform." The top (black) is the light center, and the bottom (white) is the light edge. We normalize the distance of each ray to `lightSize`, which we defined earlier. Each pixel in the resulting 1D shadow map describes the *minimum distance to the first occluder for that ray's angle*. So, if a ray (one of our red arrows) does not hit any occluders, the normalized distance will be 1.0 (and thus the resulting pixel will be white). If the ray hits an occluder half way from center, the normalized distance will be 0.5 (and thus the resulting pixel will be gray). We take the *minimum* distance so that we "stop casting the ray" after hitting the first occluder (so to speak).

In our case, we have `lightSize` number of rays, or 256. The more rays, the more precision in our resulting shadows, but the greater the fill-rate.



<a name="further-reading" />
## Further Reading

- [Catalin's Article, the original inspiration](http://www.catalinzima.com/2010/07/my-technique-for-the-shader-based-dynamic-2d-shadows/)
- http://rabidlion.com/?p=10
- http://www.gmlscripts.com/forums/viewtopic.php?id=1657