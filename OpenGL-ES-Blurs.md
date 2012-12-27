Our blurring technique described in [Shader Lesson 5](ShaderLesson5) is fairly efficient on desktop, but won't hold up on more limited devices such as Android and iOS. This is largely because of the fill-rate and multiple passes involved (as well as other factors such as sending uniform data) which contribute to the poor performance. 

By downsampling the frame buffer to 50%, we can achieve a frame rate of ~30 FPS on the Samsung Galaxy Tab II (7"). This is not really acceptable, though, considering we'd like to target some lower end hardware, and our current technique is not very practical for most game dev purposes.

There are a number of options, and which to choose depends on the requirements of your game/application.

# Software Blur

Modifying pixel data in software is slow since we need to transfer texture data to and from the GPU. This can lead to pipeline stalls, and generally isn't something you'd want to do every frame. However, if all we need is a fixed blur, or if our blur rarely ever changes, this may be a viable solution. We also have a bit more flexibility in our blur algorithm, i.e. we can reproduce a "true" gaussian blur or another type of blur. It should work on all devices, including those only supporting GL 1.0+.

There are a number of blur algorithms floating around the web, here are a couple links:

- Mario Klingemann has a number of blur algorithms, including the popular [StackBlur](http://www.quasimondo.com/StackBlurForCanvas/StackBlurDemo.html) (ported for [Android](http://stackoverflow.com/questions/12198045/fast-variable-blur-or-blur-library-in-android))
- [Romain Guy's box blur in Java](http://www.java2s.com/Code/Java/Advanced-Graphics/FastBlurDemo.htm)
- [Basic box blur](http://www.blackpawn.com/texts/blur/default.html)

I have implemented Romain Guy's box blur for LibGDX in the following utility class:

[BlurUtils](https://gist.github.com/4383372)

Note that this utility isn't very performant -- it requires a lot of unnecessary data copies from ByteBuffer to int[] and back. A more involved solution would be to blur a RGB or RGBA ByteBuffer directly; however, for the purpose of our small demo (since our blurs are only created during initialization) it runs fast enough. 

### BlurUtils Usage

To blur an image, you would do it in software before uploading the data to a GL texture:

```java
//load original pixmap
Pixmap orig = new Pixmap(Gdx.files.internal("data/lenna.png"));

//Blur the original pixmap with a radius of 4 px
//The blur is applied over 2 iterations for better quality
//We specify "disposePixmap=true" to destroy the original pixmap
Pixmap blurred = BlurUtils.blur(orig, 4, 2, true);

//we then create a GL texture with the blurred pixmap
blurTex = new Texture(blurred);

//dispose our blurred data now that it resides on the GPU
blurred.dispose();
```

The result:  
![Blurred](http://i.imgur.com/kA3gW.png)

Note that the resulting texture is not managed, so you will have to re-load it using the above code after GL context loss.

# Faking Real-Time Blurring

The simple software solution above only gives us a single blur strength to work with. If we wanted to use a different blur strength, we would need to blur the original image again, then re-upload the newly blurred data. This is very costly and would destroy our framerate if done frequently. 

Another solution is create multiple textures of varying blur strengths, and "linearly interpolate" between them while rendering to create a faux-realtime blurring. 

Given our original texture:  
![Orig](http://i.imgur.com/9ePyD.png)

We would create an array of increasingly blurry images, preferably using TextureRegions in the same Texture (to reduce texture binds and increase batching). Here we use a smaller size for our blurred images in order to reduce memory usage and improve rendering. When we upscale with bilinear filtering, the difference will not be very significant. 

Using 4 different blurs: (100% extra memory space)  
![4x](http://i.imgur.com/ylMdU.png)

Using 8 different blurs: (150% extra memory space)  
![8x](http://i.imgur.com/JL3yQ.png)

To fake a real-time blurring, we would use `mix()` in GLSL to linearly interpolate (lerp) between two different blur strengths. Since the different blur strengths are contained in the same texture, we end up with very fast rendering, no extra draw passes, no FBOs, no bath flushes, etc. The downsides:

- Requires more memory
- Larger distribution filesize. This can be avoided by blurring in software during creation time, i.e. using BlurUtils.
- Requires tweaking your shaders and atlases.



# Bloom
http://www.curious-creature.org/2007/02/20/fast-image-processing-with-jogl/
- [Further reading on GL bloom/blur](http://prideout.net/archive/bloom/) 