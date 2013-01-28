##### [start](https://github.com/mattdesl/lwjgl-basics/wiki) » LibGDX Textures
***

# THIS PAGE IS A WORK IN PROGRESS

This is a mirror of the [OpenGL Textures](Textures) tutorial, but geared toward LibGDX users, and thus a little "higher level." After reading through this, it would be good to read the [OpenGL Textures](Textures) and [NIO Buffers](Java-NIO-Buffers) tutorials to better understand how LibGDX handles textures "under the hood."

### Primer: Digital Images

An image, as you may know, is simply an array of colors, rendered in two dimensions. Let's use this very small image as an example; a heart sprite and a half-heart sprite:   
![Heart](http://i.imgur.com/libCK.png)

Now, when we zoom in on the image in Photoshop or another program, we can clearly see how the image is constructed of individual pixels:    
![HeartBig](http://i.imgur.com/NgH4n.png)

There are a number of ways an image like this would be stored on a computer, most commonly [RGBA with 8-bits per channel](http://en.wikipedia.org/wiki/RGBA_color_space). `RGB` refers to the red, green and blue channels, and `A` refers to the alpha (transparency) channel. Below are three different ways of storing the colour red:

  * **Hex aka RGB int:** `#ff0000` or `0xff0000`
  * **RGBA byte:** `(R=255, G=0, B=0, A=1)`
  * **RGBA float:** `(R=1f, G=0f, B=0f, A=1f)`


The RGBA byte array representing the above image (32x16 px) might look something like this:
```java
new byte[ imageWidth * imageHeight * 4 ] {
    0x00, 0x00, 0x00, 0x00, //Pixel index 0, position (x=0, y=0), transparent black
    0xFF, 0x00, 0x00, 0xFF, //Pixel index 1, position (x=1, y=0), opaque red
    0xFF, 0x00, 0x00, 0xFF, //Pixel index 2, position (x=2, y=0), opaque red
    ... etc ...
}
```

As you can see, a single pixel is made up of four bytes. Keep in mind it's just a single-dimensional array! 

The size of the array is `WIDTH * HEIGHT * BPP`, where `BPP` (bytes per pixel) is in this case 4 (RGBA).
We will rely on the width in order to render it as a two-dimensional image.

Since an array of bytes can get very large, we generally use compression like PNG or JPEG in order to decrease the final file-size and distribute the image for web/email/etc.

### OpenGL Textures

In OpenGL, we use *textures* to store image data. OpenGL textures do not only store image data; they are simply float arrays stored on the GPU, e.g. useful for shadow mapping and other advanced techniques.

To create an OpenGL texture, we first need to "decode" the image format (PNG, JPEG, etc) into an array of color data, like we saw above. Then, we can "upload" the pixels to OpenGL, which is another way of saying: copy the pixel data from CPU (RAM) to GPU (VRAM). Typically this is a slow operation, so we only do it when necessary at the beginning of our program.

Typically, we load a texture in LibGDX like this:
```java
tex = new Texture(Gdx.files.internal("data/libgdx.png"));
```

The above decodes the `"data/libgdx.png"` image into a pixel array, then uploads the data to OpenGL and discards the pixel array. The texture is "managed" by LibGDX, which means that it will be re-loaded if the OpenGL context is lost and regained (e.g. in an Android application, if the user hits the home button).

Here is a more explicit means of creating a texture. Note that this texture won't be "managed," so we will need to re-load it ourselves upon context loss.
```java
//decode the PNG into a pixel array, aka Pixmap
Pixmap pixels = new Pixmap("data/libgdx.png");

//if we wanted to, we could modify the pixel data before uploading it to GL
//...

//now we upload the data to GL by creating a new Texture
tex = new Texture(pixmap);

//and discard the pixels since we no longer need them
pixels.dispose();
```

As you will see, Textures are only necessary if you intend to draw the image to the screen. If you wanted to use image data for something like a terrain height map, or a simple [tiled map](Tiled-Map-Images), 

## LibGDX Formats

LibGDX will upload the data to OpenGL based on the format of the image being loaded. We can also specify formats explicitly, in which case LibGDX will perform conversions if necessary. Here is a brief explanation of the different formats in `Pixmap.Format`:

- `RGBA8888` - This is the format we described in the earlier *Primer* section. Each channel (R, G, B, A) is made up of a byte, or 8 bits. With this format, we have four bytes per pixel. We would use this for high-quality color that requires an alpha channel, for transparency. This is known as "True Color".
- `RGB888` - This is similar to the above, but discards the alpha channel (i.e. the image is opaque). This is useful for high-quality images that don't need an alpha channel.
- `RGBA4444` - This is similar to `RGBA8888`, but stores each channel in only 4 bits. This leads to lower color quality, but has performance and memory implications on low-end devices like Android and iOS. 
- `RGB565` - This stores the red channel in 5 bits, the green in 6 bits, and the blue in 5 bits. We use an extra bit in the green channel since the human eye can generally perceive more gradations of green. This is known as "High Color", and is again mainly useful for low-end or embedded devices.
- `LuminanceAlpha` - This is a grayscale image that includes an alpha channel. Grayscale colors have equal red, green and blue values, which we call "luminance." So a typical gray value of (R=127, G=127, B=127, A=255) would be represented like so with LuminanceAlpha: (L=127, A=255). Each uses 8 bits.
- `Alpha` - This is a special type of image that only stores an alpha channel in 8 bits.
- `Intensity` - This is another special type of image which only uses a single channel, but with the alpha channel equal to the luminance. For example, an Intensity color of (I=127) would be equivalent to a RGBA color of (R=127, G=127, B=127, A=127).

## Drawing with Pixmaps

We can use Pixmaps for very simple render-to-texture functionality, done in software. For example, we could create a circle texture like so:

```java
Pixmap px = new Pixmap(256, 256
```


The call to `glTexImage2D` is what sets up the actual texture in OpenGL. We can call this again later if we decide to change the width and height of our image, or if we need to change the RGBA pixel data.
If we only want to change a portion of the RGBA data (i.e. a sub-image), we can use `glTexSubImage2D`. For per-pixel modifications, however, we will generally rely on fragment shaders, which we will look into later.


*Note:* You can read about why we use GL_UNPACK_ALIGNMENT [here](http://www.opengl.org/wiki/Common_Mistakes#Texture_upload_and_pixel_reads).

### Texture Parameters

Before calling `glTexImage2D`, it's essential that we set up our texture parameters correctly. The code to do that looks like this:
```java
//Setup filtering, i.e. how OpenGL will interpolate the pixels when scaling up or down
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST);
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);

//Setup wrap mode, i.e. how OpenGL will handle pixels outside of the expected range
//Note: GL_CLAMP_TO_EDGE is part of GL12
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE);
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE);
```

#### Filtering 

The minification/magnification filters define how the image is handled upon scaling. For "pixel-art" style games, generally `GL_NEAREST`
is suitable as it leads to hard-edge scaling without blurring. Specifying `GL_LINEAR` will use bilinear scaling
for smoother results, which is generally effective for 3D games (e.g. a 1024x1024 rock or grass texture) but not
so for a 2D game:  
![Scaling](http://i.imgur.com/vAVHc.png)

#### Wrap Modes

To explain this, we need to understand a bit more about *texture coordinates* and vertices. Let's take a simple two dimensional image, like the following brick texture:  
![Brick](http://i.imgur.com/IGn1g.png)

To render the above object, we need to give OpenGL four **vertices**. As you can see, we end up with a 2D quad. Each vertex has a number of attributes, including Position (x, y) and Texture Coordinates (s, t). Texture coordinates are defined in *tangent space*, generally between 0.0 and 1.0. These tell OpenGL where to sample from our texture data. Here is an image showing the attributes of each vertex in our quad:  
![Quad](http://i.imgur.com/fkzfb.png)

*Note:* This depends on our coordinate system having an origin in the upper-left ("Y-down"). Some libraries, like LibGDX, will use lower-left origin ("Y-up"), and so the values for Position and TexCoord may be in a different order.

Sometimes programmers and modelers use `UV` and `ST` interchangeably -- "UV Mapping" is another way to describe how textures are applied to a 3D mesh.

So what happens if we use texture coordinate values less than 0.0, or greater than 1.0? This is where the *wrap mode* comes into play. We tell OpenGL how to handle values outside of the texture coordinates. The two most common modes are `GL_CLAMP_TO_EDGE`, which simply samples the edge color, and `GL_REPEAT`, which will lead to a repeating pattern. For example, using 2.0 and `GL_REPEAT` will lead to the image being repeated twice within the *width* and *height* we specified. Here is an image to demonstrate the differences between clamping and repeat wrap modes:

![WrapModes](http://i.imgur.com/lflHc.png)

### Debug Rendering

Before we get into the programmable pipeline and our sprite batching system, we can "test render" our texture. These calls (glMatrixMode, glBegin, glColor4f, glVertex2f, etc) are deprecated, and should not be used aside from simple debugging purposes. Once our sprite batcher is set up, we will no longer need to rely on deprecated code to draw a texture.

```java
public static void debugTexture(Texture tex, float x, float y, float width, float height) {
	//usually glOrtho would not be included in our game loop
	//however, since it's deprecated, let's keep it inside of this debug function which we will remove later
	glMatrixMode(GL_PROJECTION);
	glLoadIdentity();
	glOrtho(0, Display.getWidth(), Display.getHeight(), 0, 1, -1);
	glMatrixMode(GL_MODELVIEW);
	glLoadIdentity();
	
	//bind the texture before rendering it
	tex.bind();

	//setup our texture coordinates
	//(u,v) is another common way of writing (s,t)
	float u = 0f;
	float v = 0f;
	float u2 = 1f;
	float v2 = 1f;

	//immediate mode is deprecated -- we are only using it for quick debugging
	glColor4f(1f, 1f, 1f, 1f);
	glBegin(GL_QUADS);
		glTexCoord2f(u, v);
		glVertex2f(x, y);
		glTexCoord2f(u, v2);
		glVertex2f(x, y + height);
		glTexCoord2f(u2, v2);
		glVertex2f(x + width, y + height);
		glTexCoord2f(u2, v);
		glVertex2f(x + width, y);
	glEnd();
}
```

As you can see, the concept here is the same as we described in our earlier image. We are specifying a quad with texture coordinates 0.0 and 1.0. 

### Texture Atlases

One thing I haven't mentioned yet is the importance of texture atlases or "sprite sheets." Since we are only binding one texture at a time, this can be costly if we plan to draw many sprites or tiles per frame. Instead, it's almost always a better idea to place all of your tiles and sprites into a single image, so that you are only binding minimal textures per frame.

Here is one example of a texture atlas:  
![TexAtlas](http://i.imgur.com/0uz31.png)

As you might have noticed from the *Texture Wrap* section, we can tell OpenGL what part of our texture to render by specifying different texture coordinates. For example, say we want to render the grass tile at (1, 1), then texture coordinates would be set up like so:
```java
float srcX = 64;
float srcY = 64;
float srcWidth = 64;
float srcHeight = 64;

float u = srcX / tex.width;
float v = srcY / tex.height;
float u2 = (srcX + srcWidth) / tex.width;
float v2 = (srcY + srcHeight) / tex.height;
```

Here is a visual breakdown of each vertex:  
![VertexBreakdown](http://i.imgur.com/nwXUM.png)

The above would be better suited in its own method, such as `drawDebugRegion`. Later, we will examine the `TextureRegion` utility class, which will simplify the process of handling sprite sheets and sub-images.

*Note:* As we discussed earlier, using `GL_LINEAR` will lead to bilinear interpolation when scaling -- i.e. the nearest four pixels will be selected and blended together. This can lead to unwanted effects when scaling a texture atlas, where "bleeding" occurs at the edge of sprites, and so it's often wise to use `GL_NEAREST` and/or pad each sprite in your atlas with a transparent 1-2px border.


<a name="HardwareLimitations" />
## Hardware Limitations

### Max Texture Size

You can query the maximum texture width and height with the following:
```java
int maxSize = glGetInteger(GL_MAX_TEXTURE_SIZE);
```

Generally, most modern computers allow for at least 4096x4096 textures, but if you want to be really safe, you can limit yourself to 2048x2048. If you think you will be working with old or limiting drivers (or Android, iOS, WebGL), you may want to limit yourself to 1024x1024.

### Power of Two Sizes
One thing I have yet to note is the use of power-of-two (POT) dimensions. Historically, OpenGL only allowed POT texture dimensions:  
`1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096... etc`

Today, however, most drivers will support non-power-of-two (NPOT) texture sizes. You can check to see if your user supports NPOT textures with the following code:  
```java
boolean npotSupported = GLContext.getCapabilities().GL_ARB_texture_non_power_of_two;
```

It should be noted that even if the driver does support NPOT textures, it's generally still advisable to stick to POT sizes as it will often lead to better performance and storage. At a later point, this tutorial may include a segment on padding NPOT textures to a power-of-two size, for drivers that don't support NPOT textures.

## Advanced Topics

If you're ready to move onto something more advanced, check out the [shader programming series](Shaders).

## Full Source Code

Below is the full source of our simple texture wrapper. See the [repo](https://github.com/mattdesl/lwjgl-basics/blob/master/src/mdesl/graphics/Texture.java) for a more complete version, including better documentation.

```java
/**
 * Copyright (c) 2012, Matt DesLauriers All rights reserved.
 *
 *	Redistribution and use in source and binary forms, with or without
 *	modification, are permitted provided that the following conditions are met: 
 *
 *	* Redistributions of source code must retain the above copyright notice, this
 *	  list of conditions and the following disclaimer. 
 *
 *	* Redistributions in binary
 *	  form must reproduce the above copyright notice, this list of conditions and
 *	  the following disclaimer in the documentation and/or other materials provided
 *	  with the distribution. 
 *
 *	* Neither the name of the Matt DesLauriers nor the names
 *	  of his contributors may be used to endorse or promote products derived from
 *	  this software without specific prior written permission.
 *
 *	THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 *	AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 *	IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 *	ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
 *	LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 *	CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 *	SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 *	INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 *	CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 *	ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 *	POSSIBILITY OF SUCH DAMAGE.
 */
package mdesl.graphics;

import static org.lwjgl.opengl.GL11.GL_CLAMP;
import static org.lwjgl.opengl.GL11.GL_LINEAR;
import static org.lwjgl.opengl.GL11.GL_NEAREST;
import static org.lwjgl.opengl.GL11.GL_REPEAT;
import static org.lwjgl.opengl.GL11.GL_RGBA;
import static org.lwjgl.opengl.GL11.GL_TEXTURE_2D;
import static org.lwjgl.opengl.GL11.GL_TEXTURE_MAG_FILTER;
import static org.lwjgl.opengl.GL11.GL_TEXTURE_MIN_FILTER;
import static org.lwjgl.opengl.GL11.GL_TEXTURE_WRAP_S;
import static org.lwjgl.opengl.GL11.GL_TEXTURE_WRAP_T;
import static org.lwjgl.opengl.GL11.GL_UNPACK_ALIGNMENT;
import static org.lwjgl.opengl.GL11.GL_UNSIGNED_BYTE;
import static org.lwjgl.opengl.GL11.glBindTexture;
import static org.lwjgl.opengl.GL11.glEnable;
import static org.lwjgl.opengl.GL11.glGenTextures;
import static org.lwjgl.opengl.GL11.glPixelStorei;
import static org.lwjgl.opengl.GL11.glTexImage2D;
import static org.lwjgl.opengl.GL11.glTexParameteri;
import static org.lwjgl.opengl.GL12.GL_CLAMP_TO_EDGE;

import java.io.IOException;
import java.io.InputStream;
import java.net.URL;
import java.nio.ByteBuffer;

import org.lwjgl.BufferUtils;

import de.matthiasmann.twl.utils.PNGDecoder;

public class Texture {

	public final int target = GL_TEXTURE_2D;
	public final int id;
	public final int width;
	public final int height;

	public static final int LINEAR = GL_LINEAR;
	public static final int NEAREST = GL_NEAREST;

	public static final int CLAMP = GL_CLAMP;
	public static final int CLAMP_TO_EDGE = GL_CLAMP_TO_EDGE;
	public static final int REPEAT = GL_REPEAT;

	public Texture(URL pngRef) throws IOException {
		this(pngRef, GL_NEAREST);
	}

	public Texture(URL pngRef, int filter) throws IOException {
		this(pngRef, filter, GL_CLAMP_TO_EDGE);
	}

	public Texture(URL pngRef, int filter, int wrap) throws IOException {
		InputStream input = null;
		try {
			//get an InputStream from our URL
			input = pngRef.openStream();
			
			//initialize the decoder
			PNGDecoder dec = new PNGDecoder(input);

			//set up image dimensions 
			width = dec.getWidth();
			height = dec.getHeight();
			
			//we are using RGBA, i.e. 4 components or "bytes per pixel"
			final int bpp = 4;
			
			//create a new byte buffer which will hold our pixel data
			ByteBuffer buf = BufferUtils.createByteBuffer(bpp * width * height);
			
			//decode the image into the byte buffer, in RGBA format
			dec.decode(buf, width * bpp, PNGDecoder.Format.RGBA);
			
			//flip the buffer into "read mode" for OpenGL
			buf.flip();

			//enable textures and generate an ID
			glEnable(target);
			id = glGenTextures();

			//bind texture
			bind();

			//setup unpack mode
			glPixelStorei(GL_UNPACK_ALIGNMENT, 1);

			//setup parameters
			glTexParameteri(target, GL_TEXTURE_MIN_FILTER, filter);
			glTexParameteri(target, GL_TEXTURE_MAG_FILTER, filter);
			glTexParameteri(target, GL_TEXTURE_WRAP_S, wrap);
			glTexParameteri(target, GL_TEXTURE_WRAP_T, wrap);

			//pass RGBA data to OpenGL
			glTexImage2D(target, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, buf);
		} finally {
			if (input != null) {
				try { input.close(); } catch (IOException e) { }
			}
		}
	}

	public void bind() {
		glBindTexture(target, id);
	}
}
```