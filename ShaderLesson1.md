**Preface**

***

This series relies on the minimal [lwjgl-basics](https://github.com/mattdesl/lwjgl-basics) API for shader and rendering utilities. However, the concepts should be universal enough that they could be applied to LibGDX, [GLSL Sandbox](http://glsl.heroku.com/), [Love2D](https://love2d.org/), iOS, or any other platforms that support GLSL. I'd recommend starting with the [Textures](https://github.com/mattdesl/lwjgl-basics/wiki/Textures) tutorial as it covers essential concepts like filters and texture coordinates. 

***

## Intro

As discussed, we need to write *vertex* and *fragment* scripts in order for our shader program to work. Our first shaders will be very basic, and simply output the color red (ignoring the texture).

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

Then, we create our SpriteBatch using our custom shader. Now we can render our sprites as per usual, and they will appear as red boxes:

```java
protected void render() throws LWJGLException {
	super.render();

	// start our batch
	batch.begin();

	// draw some sprites... they will all be affected by our shaders
	batch.draw(tex, 10, 10);
	batch.draw(tex, 10, 320, 32, 32);

	// end our batch
	batch.end();
}
```

![RedBoxes](http://i.imgur.com/iziaV.png)


## The Shaders

Let's take a look at what is going on. Here is the [vertex shader](https://github.com/mattdesl/lwjgl-basics/blob/master/test/res/shadertut/lesson1.vert):
```glsl
//incoming Position attribute from our SpriteBatch
attribute vec2 Position;

//the transformation matrix of our SpriteBatch
uniform mat4 u_projView;
 
void main() {
	//transform our 2D screen space position into 3D world space
	gl_Position = u_projView * vec4(Position.xy, 0.0, 1.0);
}
```

We simply take the Position attribute (given to us by our sprite batcher) -- such as `(10, 10)` -- and transform it into 3D world-space coordinates that OpenGL can work with.

The [fragment shader](https://github.com/mattdesl/lwjgl-basics/blob/master/test/res/shadertut/lesson1.frag):
```glsl
void main() {
	//final color
	gl_FragColor = vec4(1.0, 0.0, 0.0, 1.0);
}
```

Our fragment shader is also pretty simple -- it simply returns opaque red as the fragment (or "pixel") color.

## Vertex Attributes

```glsl
attribute vec2 Position;
```

Seeing the above line, you may be wondering what exactly an `attribute` is in GLSL. Think back to our brick sprite in the [Textures](https://github.com/mattdesl/lwjgl-basics/wiki/Textures) tutorial:  
![Brick](http://i.imgur.com/IGn1g.png)

As we explained in the Textures tutorial, we need to give OpenGL four **vertices** to make up our quad. Each **vertex** contains a number of **attributes**, such as `Position` and `TexCoord`:  
![Quad](http://i.imgur.com/fkzfb.png)

In our case, we are ignoring the `TexCoord` attribute since we don't need it. Instead, we only define the `Position` attribute, using a `vec2` (2-component float vector) as the data type to represent `(x, y)`. SpriteBatch expects the name and data type to match accordingly.

_Attributes can only be declared in vertex shaders_. Also, attributes are **read-only** since they are passed from SpriteBatch. So we cannot assign them a value in GLSL.


## Uniform: u_projView

The next line in our vertex shader brings us to another topic, uniforms:
```glsl
uniform mat4 u_projView;
```

A uniform is like a script variable that we can set from Java. For example, if we needed to pass the mouse coordinates to a shader program, we would use a `vec2` uniform and send the new `(x, y)` values to the shader every time the mouse moves. Like attributes, uniforms are **read-only** in the shader, so we cannot assign values to them in GLSL.

In our case, the vertex shader needs to transform the screen space coordinates from our SpriteBatch -- e.g. `(10, 10)` -- into 3D world-space coordinates. We do this by multiplying our `Position` attribute by the combined [projection and view matrices](http://en.wikipedia.org/wiki/Transformation_matrix) of our SpriteBatch, which is named `u_projView` (or `SpriteBatch.U_PROJ_VIEW`). This leads to 2D orthographic projection, where origin `(0, 0)` is at the top left:
```glsl
gl_Position = u_projView * vec4(Position.xy, 0.0, 1.0);
```

SpriteBatch will update the `u_projView` uniform data as necessary; for example, when we first initialize SpriteBatch, or after calling `SpriteBatch.resize`. Notice that the uniform uses a `mat4` data type. 

# Dissecting the Fragment Shader

## Uniform: u_texture

As I briefly explained in the Texture tutorial, it's possible in OpenGL to have multiple active texture units (i.e. multiple textures "bound" at once). The `sampler2D` data type tells us which texture unit we are dealing with. However, for now, we will only concern ourselves with the default one: texture unit zero (`GL_TEXTURE0`). We can think of it as an integer, where 0 is the default texture unit. 

SpriteBatch expects a `sampler2D` uniform named `u_texture` (or `SpriteBatch.U_TEXTURE`). SpriteBatch will then set this uniform for us to `0`, during initialization, to indicate the default texture unit.

As we can see in the fragment shader, we also need to declare our varyings, i.e. our attributes passed from the vertex shader. The names should match the varyings we declared in the vertex shader.

```glsl
//texture unit, SpriteBatch will set it to zero (0)
uniform sampler2D u_texture;

//"in" attributes from vertex shader
varying vec4 vColor;
varying vec2 vTexCoord;
```

Within our `main()`