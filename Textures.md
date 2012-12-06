This is a short introduction to textures in OpenGL. Our end result will be a Texture class which we can use in our simple sprite engine.

### Primer: Digital Images

An image, as you may know, is simply an array of colors, rendered in two dimensions. Let's use this very small image as an example; a heart sprite and a half-heart sprite:   
![Heart](http://i.imgur.com/WQDjE.png)

Now, when we zoom in on the image in Photoshop or another program, we can clearly see how the image is constructed of individual pixels:    
![HeartBig](http://i.imgur.com/NgH4n.png)

There are a number of ways an image like this would be stored on a computer, most commonly [RGBA with 8-bits per channel](http://en.wikipedia.org/wiki/RGBA_color_space). `RGB` refers to the red, green and blue channels, and `A` refers to the alpha (transparency) channel. Below we can see how the color red would be stored digitally:
```
Hex aka RGB int: #ff0000 or 0xff0000
RGBA byte: (R=255, G=0, B=0, A=1)
RGBA float: (R=1f, G=0f, B=0f, A=1f)
```

The byte array representing the above image (22x9 px) might look something like this:
```java
new byte[ imageWidth * imageHeight * 4 ] {
    0x00, 0x00, 0x00, 0x00, //Pixel index 0, position (x=0, y=0), transparent black
    0xFF, 0x00, 0x00, 0xFF, //Pixel index 1, position (x=1, y=0), opaque red
    0xFF, 0x00, 0x00, 0xFF, //Pixel index 2, position (x=2, y=0), opaque red
    ... etc ...
}
```

As you can see, a single pixel is made up of four bytes. Keep in mind it's just a single-dimensional array! 
The size of the array is WIDTH * HEIGHT * BPP, where BPP (bytes per pixel) in this case is 4 (RGBA).
We will rely on the width in order to render it as a two-dimensional image.

Most often, we use compression like PNG, TIFF, JPEG, GIF, or what have you, in order to make the file-size smaller. 

### OpenGL Textures

In OpenGL, we use *textures* to store image data. OpenGL textures do not only store image data; they are simply float arrays stored on the GPU, e.g. useful for shadow mapping and other advanced techniques.

The basic steps of setting up a texture are as follows:

1. Decode into RGBA bytes
2. Get a new texture ID
3. Bind that texture
4. Set up any texture parameters
5. Upload the RGBA bytes to OpenGL

### Decoding PNG to RGBA bytes

OpenGL doesn't know anything about GIF, PNG, JPEG, etc; it only understands bytes and floats. So we need to decode our PNG image into a ByteBuffer. If you are unfamiliar with NIO buffers, [see this page](https://github.com/mattdesl/lwjgl-basics/wiki/Java-NIO-Buffers).

In order to do that, we will use Matthias Mann's open source pure-Java PNG decoder. He also has some decoders for BMP, JPEG and TGA which you can find [here](http://hg.l33tlabs.org/TextureLoader/file/tip/src/de/matthiasmann/textureloader). 

The code to decode an image into a ByteBuffer looks like this:
```java
//get an InputStream from our URL
input = pngURL.openStream();

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
```

### Creating the Texture

Although it's possible to bind multiple textures in OpenGL with multiple texture units, this guide
will only focus on using a single texture unit. Therefore, in order to change the parameters of a texture,
or in order to send the RGBA bytes to OpenGL, we first need to *bind* that texture, i.e. "make it the currently
active texture." We can use `glGenTextures` to retrieve a unique identifier (aka "texture name" or "texture handle")
so that GL knows which texture we are trying to bind. 

The process of creating a texture and uploading the RGBA bytes looks like this:

```java
//Generally a good idea to enable texturing first
glEnable(GL_TEXTURE_2D);

//generate a texture handle or unique ID for this texture
id = glGenTextures();

//bind the texture
glBindTexture(GL_TEXTURE_2D, id);

//use an alignment of 1 to be safe
//this tells OpenGL how to unpack the RGBA bytes we will specify
glPixelStorei(GL_UNPACK_ALIGNMENT, 1);
glPixelStorei(GL_PACK_ALIGNMENT, 1);

//set up our texture parameters
glTexParameteri(...);

//upload our ByteBuffer to GL
glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, buf);		
```

The call to `glTexImage2D` is what sets up the actual texture in OpenGL. We can call this again later if we decide to change the width and height of our image, or if we need to change the RGBA pixel data.
If we only want to change a portion of the RGBA data (i.e. a sub-image), we can use `glTexSubImage2D`. For per-pixel modifications, however, we will generally rely on fragment shaders, which we will look into later.


### Texture Parameters

Before calling `glTexImage2D`, it's essential that we set up our texture parameters correctly. 

**This section is a work in progress. For now you should be fine with the following parameters:**
```java
//Setup wrap mode, i.e. how OpenGL will handle pixels outside of the expected range
//Note: GL_CLAMP_TO_EDGE is part of GL12
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE);
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE);

//Setup filtering, i.e. how OpenGL will interpolate the pixels when scaling up or down
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST);
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
```

The minification/magnification filters define how the image is handled upon scaling. For "pixel-art" style games, generally `GL_NEAREST`
is suitable as it leads to hard-edge scaling without blurring. Specifying `GL_LINEAR` will use bilinear scaling
for smoother results, which is generally effective for 3D games (e.g. a 1024x1024 rock or grass texture) but not
so for a 2D game:  
![Scaling](http://i.imgur.com/vAVHc.png)

### Texture Atlases

**This section is a work in progress.**

### Full Source Code

Below is the full source of our texture wrapper. See the [repo](https://github.com/mattdesl/lwjgl-basics/blob/master/src/mdesl/graphics/Texture.java) for a more complete version, including better documentation.

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
import static org.lwjgl.opengl.GL11.GL_PACK_ALIGNMENT;
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
	static int bound = 0;

	public final int target = GL_TEXTURE_2D;
	public final int id;
	public final int width;
	public final int height;

	public static final int LINEAR = GL_LINEAR;
	public static final int NEAREST = GL_NEAREST;

	public static final int CLAMP = GL_CLAMP;
	public static final int CLAMP_TO_EDGE = GL_CLAMP_TO_EDGE;
	public static final int REPEAT = GL_REPEAT;

	public static void clearLastBind() {
		bound = 0;
	}

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
			glPixelStorei(GL_PACK_ALIGNMENT, 1);

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
		if (id != bound)
			glBindTexture(target, id);
	}
}
```