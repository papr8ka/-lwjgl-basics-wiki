Our blurring technique described in [Shader Lesson 5](ShaderLesson5) is fairly efficient on desktop, but won't hold up on more limited devices such as Android and iOS. This is largely because of the fill-rate and multiple passes involved, as well as other factors such as sending uniform data.

By downsampling the frame buffer object to 50% of the screen size, we can achieve a frame rate of ~30 FPS on the Samsung Galaxy Tab II (7"). This is not really acceptable, though, considering we'd like to target some lower end hardware, and our current technique is not very practical for games.

There are a number of options, and which to choose depends on the requirements of your game/application.

# Software Blur

Modifying pixel data in software is slow since we need to transfer texture data to and from the GPU. This can lead to pipeline stalls, and generally isn't something you'd want to do every frame. However, if all we need is a fixed blur, or if our blur rarely ever changes, this may be a viable solution. Blurring in software also allows for a bit more flexibility, and we can employ a "true" gaussian blur or any other type of blur. This should work on all GL 1.0+ devices.

There are a number of blur algorithms floating around the web, here are a couple links:

- Mario Klingemann has a number of blur algorithms, including the popular [StackBlur](http://www.quasimondo.com/StackBlurForCanvas/StackBlurDemo.html) (ported for [Android](http://stackoverflow.com/questions/12198045/fast-variable-blur-or-blur-library-in-android))
- [Romain Guy's box blur in Java](http://www.java2s.com/Code/Java/Advanced-Graphics/FastBlurDemo.htm)
- [Basic box blur](http://www.blackpawn.com/texts/blur/default.html)

I have implemented Romain Guy's box blur for LibGDX in the following utility class:

[BlurUtils](https://gist.github.com/4383372)

Note that this utility isn't very performant -- it requires a lot of unnecessary data copies from ByteBuffer to int[] and back. A more involved solution would be to blur a RGB or RGBA ByteBuffer directly; however, for the purpose of our small demo, it runs fast enough, and is only used at creation time.

### BlurUtils Usage

After decoding the image into a Pixmap, we can blur the pixel buffer with the BlurUtils class. Then we can upload the blurred pixels to a GL texture.

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

The result, using the notorious [Lenna](http://en.wikipedia.org/wiki/Lenna):    
![Blurred](http://i.imgur.com/kA3gW.png)

Note that the resulting texture is not managed, so you will have to re-load it using the above code after GL context loss.

# "Lerp Blur" - Faking Real-Time Blurs

The software solution above only gives us a single blur strength to work with. If we wanted to use a different blur strength, we would need to blur the original image again, then re-upload the newly blurred pixmap data. This is very costly and would destroy our framerate if done frequently. 

Below I describe a trick to achieve blurs of varying strengths without much impact on rendering performance, especially suitable for mobile devices and low-end hardware. The idea is to "lerp" (linearly interpolate) between different pre-calculated blur strengths.

We will look at two different ways of implementing this "lerp blur" in practice:

- [Using Mipmaps and `bias`](#ImplementationA)
- [Manual Lerp with `mix()`](#ImplementationB)

<a name="ImplementationA" />
## Implementation A: Using Mipmaps

_Note:_ I'll assume you understand the basics of mipmapping. If not, read [this primer]() before continuing. 

An old-school trick for cheap blurs is to down-sample your image with high quality interpolation (such as those employed by most drivers for mip-mapping), and then up-scale the image with linear filtering. 

![Crap](http://i.imgur.com/e7zb4.png)

Downscaled to 64x64, upscaled to 256x256. Looks crappy. Now, let's do the above, but after downsampling to 64x64, we'll apply a nice quality gaussian blur to the downsized image. Rendered at 256x256:

![Nice](http://i.imgur.com/ZOPd1.png)

Holy shiza, it looks like a blur. The code for that:

```java
Pixmap orig = new Pixmap(Gdx.files.internal("data/lenna2.png"));

int origWidth = orig.getWidth();
int origHeight = orig.getHeight();

//blur parameters
int blurRadius = 4;
int iterations = 3;

//blur the image at 25% of original size
//also specify disposePixmap=true to dispose the original Pixmap
Pixmap blurred = BlurUtils.blur(orig, 0, 0, origWidth, origHeight,
						0, 0, origWidth/4, origHeight/4,
						blurRadius, iterations, true);
					
//uplaod the blurred texture to GL
tex = new Texture(blurred);
tex.setFilter(TextureFilter.Linear, TextureFilter.Linear);
tex.setWrap(TextureWrap.Repeat, TextureWrap.Repeat);

//dispose blur after uploading
blurred.dispose();
```

Now, maybe you can see how mipmaps would help us here. The further we downscale, the stronger the blur will appear. Each successive downsample in our mipmap chain acts as the next level up of "blur strength." Our effect only works if we generate custom mipmaps, though, as we need to blur at each mipmap level after downsampling. Here is the set up code:

```java
//load the original image, can be in any format
Pixmap pixmap = new Pixmap(Gdx.files.internal("data/lenna.png"));

//upload the (unblurred) data, this will be put to mipmap level 0
//NOTE: we need to ensure RGBA8888 format is used, otherwise it may not render correctly
tex = new Texture(pixmap, Format.RGBA8888, false);

//bind before we generate mipmaps
tex.bind();

//generate our blurred mipmaps
BlurUtils.generateBlurredMipmaps(pixmap, pixmap.getWidth(), pixmap.getHeight(), 1, 3, true);

//clamping to edge seems to work best
tex.setWrap(TextureWrap.ClampToEdge, TextureWrap.ClampToEdge);

//any mipmap filter setting will work; but this will give us the smoothest result
tex.setFilter(TextureFilter.MipMapLinearLinear, TextureFilter.MipMapLinearLinear);
```

The generateBlurredMipmaps essentially just draws successively halved Pixmaps, then applies a software blur on them, then uploads the Pixmap data to that mipmap level with the following:
```java
//upload Pixmap to currently bound texture 
Gdx.gl.glTexImage2D(GL10.GL_TEXTURE_2D, mipmapLevel,
		pixmap.getGLInternalFormat(), pixmap.getWidth(),
		pixmap.getHeight(), 0, pixmap.getGLFormat(),
		pixmap.getGLType(), pixmap.getPixels());
```

Then, on the GLSL side, we'll use the optional `bias` parameter of `texture2D`, which allows us to influence which mipmap level is sampled from. Depending on the given bias, the driver will choose the most appropriate mipmap level. With MipMapLinearLinear, we actually end up with "trilinear" filtering, where the driver interpolates between the two nearest mipmap levels. 

```glsl
...

//bias to influence LOD picking; e.g. "blur strength"
uniform float bias;

void main() {
	//sample from the texture using bias to influence LOD
	vec4 texColor = texture2D(u_texture, vTexCoord, bias);
	gl_FragColor = texColor * vColor;
}
```

![MipmapBlur](http://i.imgur.com/FAROj.gif)

Try setting different filters on your texture. MipMapNearestLinear leads to an interesting pixelated effect. MipMapLinearNearest leads to a "stepping" effect between mipmap levels, but with smooth interpolation. MipMapNearestNearest leads to both a "stepping" and pixelated effect.

The upsides to this solution is that we only need to set it up once, then we can forget about it. It also works with SpriteBatch, so it doesn't require very much refactoring. The downside is that `bias` is not a commonly used or well tested feature, thus may not act as expected on certain drivers. It also seems rather arbitrary how much our maximum bias should be. Another obvious downside is that this solution requires 33% more texture space.

You might notice the transition from mipmap 0 (unblurred) to 1 (blurred slightly) looks a little strange. This is because the difference is rather dramatic (full size unblurred to half-size blurred), and when we interpolate between them it's rather obvious. If you need a smoother blur transition, you can try playing with the blur radius at varying mipmap levels, or you can try Implementation B, which intends to fix this problem.

<a name="ImplementationB" />

## Implementation B: Manual Lerping with `mix()`

Another solution is create multiple textures of varying blur strengths, and "linearly interpolate" between them while rendering to mimic realtime blurring. This doesn't require the `bias` parameter (which is not thoroughly tested), and allows for a slightly smoother transition from unblurred to blurred.

Given our original texture:  
![Orig](http://i.imgur.com/9ePyD.png)

We would create an array of increasingly blurry images, like so:

![8x](http://i.imgur.com/JL3yQ.png)

Notice that each is half the size of our original; this "downsampling" reduces memory usage, and the differences will be minor when we upscale with linear filtering. Since we're working on phones and small screens, we could probably get away with even further downsampling.

To fake the real-time blurring, we use `mix()` in GLSL to linearly interpolate (lerp) between two different blur strengths. It looks like this:

![AnimatedBlur](http://i.imgur.com/yU3xF.gif)

(In grayscale for the sake of GIF quality)

There are a number of ways we could implement this in practice. One would be to layout your sprites along a single column in your sprite sheet, and have the successive blur strengths placed to the right of each respective sprite. Then the shader would offset the S (i.e. x-axis) texture coordinate based on the desired blur strength.

Instead, we'll use another solution to demonstrate how to work with a custom mesh and pass our own attributes to a shader. The downside is that we won't be able to use SpriteBatch, and will need to create our own. 

Firstly, decode our image into a Pixmap. Then we need to build a larger pixmap, made up of our image at varying sizes and blur strengths. Here are two ideas for laying out your sheet:

![Layout1](http://i.imgur.com/P1mta.png)

![Layout2](http://i.imgur.com/TLXvO.png)

The first leads to a smoother and wider transition of blurs, but the second requires less texture space.



# Bloom
http://www.curious-creature.org/2007/02/20/fast-image-processing-with-jogl/
- [Further reading on GL bloom/blur](http://prideout.net/archive/bloom/) 