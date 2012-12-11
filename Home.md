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

The best way to install the API is to use Eclipse and EGit (or another IDE with Git support) to pull the most recent source code. Included in the `lib` and `native` folder is a distribution of LWJGL 2.8.5. You can download newer versions of LWJGL from their [downloads page](http://lwjgl.org/download.php). 

You could also grab a stable JAR of the API from the [downloads page](https://github.com/mattdesl/lwjgl-basics/downloads). Then, you would set up LWJGL and your natives properly in [Eclipse](http://www.lwjgl.org/wiki/index.php?title=Setting_Up_LWJGL_with_Eclipse), [NetBeans](http://www.lwjgl.org/wiki/index.php?title=Setting_Up_LWJGL_with_NetBeans) or [IntelliJ](http://www.lwjgl.org/wiki/index.php?title=Setting_Up_LWJGL_with_IntelliJ_IDEA), and include lwjgl-basics as a class library.

### Hello World

Here is a simple example of rendering some sprites to the screen with _lwjgl-basics_.

```java
import java.io.IOException;

import mdesl.graphics.Color;
import mdesl.graphics.SpriteBatch;
import mdesl.graphics.Texture;

import org.lwjgl.LWJGLException;
import org.lwjgl.Sys;
import org.lwjgl.opengl.Display;

public class SpriteBatchExample extends SimpleGame {

	public static void main(String[] args) throws LWJGLException {
		Game game = new SpriteBatchExample();
		game.setDisplayMode(640, 480, false);
		game.start();
	}

	Texture tex, tex2;
	SpriteBatch batch;

	protected void create() throws LWJGLException {
		super.create();

		//Load some textures
		try {
			tex = new Texture(Util.getResource("res/tiles.png"), Texture.NEAREST);
			tex2 = new Texture(Util.getResource("res/font0.png"));
		} catch (IOException e) {
			// ... do something here ...
			Sys.alert("Error", "Could not decode images!");
			e.printStackTrace();
			System.exit(0);
		}
		
		//create our sprite batch
		batch = new SpriteBatch();
	}

	protected void render() throws LWJGLException {
		super.render();		
		
		//start the sprite batch
		batch.begin();

		//draw some tiles from our sprite sheet
		batch.drawRegion(tex, 64, 64, 64, 64, 	//source X,Y,WIDTH,HEIGHT
							  0, 0);			//destination X,Y (uses source size)
		batch.drawRegion(tex, 0, 0, 64, 64,		//source X,Y,WIDTH,HEIGHT
							  50, 70, 128, 128);//destination X,Y,WIDTH,HEIGHT

		//tint batch red
		batch.setColor(Color.RED); 
		batch.draw(tex2, 200, 155);
		
		//reset color
		batch.setColor(Color.WHITE);

		//finish the sprite batch and push the tiles to the GPU
		batch.end();
	}
	

	protected void resize() throws LWJGLException {
		super.resize();
		batch.resize(Display.getWidth(), Display.getHeight());
	}
}
```