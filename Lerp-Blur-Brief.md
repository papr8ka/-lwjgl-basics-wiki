The "Lerp Blur" is a name I've given to a technique for cheap blurring, suitable for Android, iOS and other fill-rate limited devices that can't rely on multiple render passes and FBOs. 

The basic idea of the "Lerp Blur" is to, in software, create a series of images of increasing blur strengths, and use some form of interpolation between two varying strengths in order to simulate a real-time adjustable blur:

![8x](http://i.imgur.com/JL3yQ.png)

We can employ mipmapping and the `bias` parameter to make this a bit more efficient.

## Mipmapping

An old-school trick for cheap blurs is to down-sample your image with high quality interpolation (such as those employed by most drivers for mip-mapping), and then up-scale the image with linear filtering. 

![Crap](http://i.imgur.com/e7zb4.png)

Downscaled to 64x64, upscaled to 256x256. Looks pretty crappy. Now, let's do the above, but after downsampling to 64x64, we'll apply a nice quality gaussian blur (in software) to the downsized image. Rendered at 256x256:

![Nice](http://i.imgur.com/ZOPd1.png)

That looks better. Now, if we applied a gaussian blur to each mipmap level, we can use this to simulate a variable blur. Since each mipmap level is smaller than the last, it will lead to a greater blur effect when scaled up. This means we need to build our mipmaps manually, in software:

```java
for each mipmap level:
    //... downsample image by half ...
    pixels = downsample(pixels, width, height);

    //... apply blur to downsampled image ...
    blurred = blur(pixels);    
    
    //... upload blurred pixels to the current mipmap level ...
    glTexImage2D(GL_TEXTURE_2D, mipmapLevel, ...)

    mipmapLevel++;
    width = width/2;
    height = height/2;
```

Our texture will use `GL_LINEAR_MIPMAP_LINEAR` as the filter, and `GL_CLAMP_TO_EDGE` for wrap mode.

Our fragment shader is only changed slightly. We specify a `bias` amount (0.0 or greater) to influence which mipmap level the driver picks from. 

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

The result is that we can "fake" a real-time blur without any extra draw passes or FBOs. The blur is by no means accurate, but on small resolutions it looks good.

![MipmapBlur](http://i.imgur.com/FAROj.gif)

<sup>(Shown in grayscale for better GIF quality)</sup>

You can see a full implementation of the above technique, as well as a solution that doesn't rely on `bias`, in the following article:  
[OpenGL ES Blurs](OpenGL-ES-Blurs)
