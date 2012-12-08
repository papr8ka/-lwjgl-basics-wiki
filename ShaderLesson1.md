**Preface**

***

This series relies on the minimal [lwjgl-basics](https://github.com/mattdesl/lwjgl-basics) API for shader and rendering utilities. However, the concepts should be universal enough that they could be applied to LibGDX, [GLSL Sandbox](http://glsl.heroku.com/), [Love2D](https://love2d.org/), iOS, or any other platforms that support GLSL. I'd recommend starting with the [Textures](https://github.com/mattdesl/lwjgl-basics/wiki/Textures) tutorial as it covers essential concepts like filters and texture coordinates.

***

## Intro

As discussed, we need to write *vertex* and *fragment* scripts in order for our shader program to work. This first example will use standard shaders, similar to those defined in SpriteBatch. You can see the default SpriteBatch programs by printing `SpriteBatch.DEFAULT_VERT_SHADER` and `SpriteBatch.DEFAULT_FRAG_SHADER`. Our program will include one minor difference: we will invert the final colour. For example, it will look as if we applied Photoshop's *Invert Color* function.

*Note:* In this series, we will use text files (`.vert` and `.frag`) for easier editing. When you go to release and distribute your games, you may want to embed the GLSL in your Java source as a String. Eclipse includes a [feature for pasting multi-line strings](http://www.vasanth.in/2009/03/10/eclipse-tip-escape-text-when-pasting/) which will be helpful.

Follow along with the full source code [here](https://github.com/mattdesl/lwjgl-basics/blob/master/test/mdesl/test/shadertut/ShaderLesson1.java).

## Set-Up

Below is our setup code:
```java
//load our shader program and sprite batch
try {
	//read the files into strings
	final String VERTEX = Util.readFile(Util.getResourceAsStream("res/shadertut/lesson1.vert"));
	final String FRAGMENT = Util.readFile(Util.getResourceAsStream("res/shadertut/lesson1.frag"));
	
	//create our shader program -- be sure to pass SpriteBatch's default attributes!
	ShaderProgram program = new ShaderProgram(VERTEX, FRAGMENT, SpriteBatch.ATTRIBUTES);
	
	//create our sprite batch
	batch = new SpriteBatch(program);
} catch (Exception e) { 
	// ... handle the exception ... 
}
```

For convenience, we use the [Util](https://github.com/mattdesl/lwjgl-basics/blob/master/test/mdesl/test/Util.java) class to read our text files.

We then create our shader program and specify the attribute locations with the third parameter. This tells ShaderProgram how the attributes will be laid out; since SpriteBatch expects them to be in a specific order (i.e. Position is expected at index 0). 

Then, we create our SpriteBatch using our custom shader. Now we can render our sprites as per usual, and they will appear inverted:

```java
protected void render() throws LWJGLException {
	super.render();

	// start our batch
	batch.begin();

	// draw some sprites here
	batch.draw(tex, 10, 10);

	// end our batch
	batch.end();
}
```

![Invert](http://i.imgur.com/CdA4o.png)