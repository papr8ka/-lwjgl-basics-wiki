In this lesson we'll learn how to sample from a texture and invert its colours, similar to Photoshop's Invert Color function.

## Set Up

Follow along with the full source code [here](https://github.com/mattdesl/lwjgl-basics/blob/master/test/mdesl/test/shadertut/ShaderLesson2.java). Our set up looks exactly the same as in [Lesson1](ShaderLesson1), except that we are loading `lesson2.vert` and `lesson2.frag`. 

We can leave our rendering method the same, and now we'll see a different outcome:

![Invert](http://i.imgur.com/Bb0MA.png)

(The original grass texture can be seen [here](https://github.com/mattdesl/lwjgl-basics/blob/master/test/res/grass.png).)


## The Shaders

Here is the [vertex shader](https://github.com/mattdesl/lwjgl-basics/blob/master/test/res/shadertut/lesson2.vert):
```glsl
//combined projection and view matrix
uniform mat4 u_projView;

//"in" attributes from our SpriteBatch
attribute vec2 Position;
attribute vec2 TexCoord;
attribute vec4 Color;

//"out" varyings to our fragment shader
varying vec4 vColor;
varying vec2 vTexCoord;
 
void main() {
	vColor = Color;
	vTexCoord = TexCoord;
	gl_Position = u_projView * vec4(Position, 0.0, 1.0);
}
```

The above is a simple "pass through" vertex shader. It does two things:

1. Pass the `Color` and `TexCoord` attributes along to our fragment shader.
2. Transform the given screen space position -- e.g. `(10, 10)` -- into 3D world-space coordinates that OpenGL understands.

And the [fragment shader](https://github.com/mattdesl/lwjgl-basics/blob/master/test/res/shadertut/lesson1.frag):
```glsl
//SpriteBatch will use texture unit 0
uniform sampler2D u_texture;

//"in" varyings from our vertex shader
varying vec4 vColor;
varying vec2 vTexCoord;

void main() {
	//sample the texture
	vec4 texColor = texture2D(u_texture, vTexCoord);
	
	//invert the red, green and blue channels
	texColor.rgb = 1.0 - texColor.rgb;
	
	//final color
	gl_FragColor = vColor * texColor;
}
```

Our fragment shader is also pretty simple:

1. Sample the color at the current texture coordinate. 
2. Invert the RGB components of the texture color.
3. Multiply this color by our vertex color and "output" the result.

# Dissecting the Vertex Shader

## Attributes

Here's the first thing you'll notice, found in our vertex shader:
```glsl
//"in" attributes from our SpriteBatch
attribute vec2 Position;
attribute vec2 TexCoord;
attribute vec4 Color;
```

Think back to our brick sprite in the [Textures](https://github.com/mattdesl/lwjgl-basics/wiki/Textures) tutorial:  
![Brick](http://i.imgur.com/IGn1g.png)

As we explained in the Textures tutorial, we need to give OpenGL four **vertices** to make up our quad. Each **vertex** contains a number of **attributes**, such as `Position` and `TexCoord`:  
![Quad](http://i.imgur.com/fkzfb.png)

Another attribute that is not shown in the above image is `Color`. Generally, we'll use opaque white `(R=1, G=1, B=1, A=1)` for each vertex, in order to render the sprite with full opacity. So our SpriteBatch is passing three **attributes** for each **vertex**: `Position`, `TexCoord`, and `Color`.

`Position` is defined with two components: `(x, y)`. In GLSL, we use a `vec2` (2-component float vector) to define this attribute. 

`TexCoord` is also defined with two components: `(s, t)`. Again, we use a `vec2` to define it.

`Color` is defined with four components: `(r, g, b, a)`. We will use a `vec4` (4-component float vector) to define it.

SpriteBatch expects these three attributes to exist in the vertex shader, and the names should match exactly. This is why we created our ShaderProgram with `SpriteBatch.ATTRIBUTES` as a parameter.

_Attributes can only be declared in vertex shaders_. Also, attributes are **read-only** since they are passed from SpriteBatch. So we cannot assign them a value in GLSL.

In order for the fragment shader to utilize these attributes, we need to "pass them along." This is done by declaring **varyings** in the vertex and fragment shaders. In the vertex shader, we pass them along like so:
```glsl
...

varying vec2 vTexCoord;
varying vec4 vColor;

void main() {
    vTexCoord = TexCoord;
    vColor = Color;
    ...
}
```

Our varying names can be anything, as long as they are consistent between fragment and vertex shaders.

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