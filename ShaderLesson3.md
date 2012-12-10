this page is a WIP

--- ignore it all for now ---


Now that you're familiar with some of the basic ideas behind GLSL, we can start getting into some more interesting effects. First, take a peek at [Lesson 3's Java source](https://github.com/mattdesl/lwjgl-basics/blob/master/test/mdesl/test/shadertut/ShaderLesson3.java). As you can see, most of the code is the same as in the other lessons, save for a few differences in resource paths and a flag to `Display.setResizable(false)` (for simplicity's sake in our demo).

The most important change on the Java side can be seen in the `resize` method:
```java
// called to resize the display
protected void resize() throws LWJGLException {
	super.resize();

	// resize our batch with the new screen size
	batch.resize(Display.getWidth(), Display.getHeight());
	
	// whenever our screen resizes, we need to update our uniform
	program.use();
	program.setUniformf("resolution", Display.getWidth(), Display.getHeight());
}
```

Here we are setting a uniform called `resolution`. We give it two float parameters, so the uniform will need to be of type `vec2`. Also note that, before sending our uniform data, we need to make our program active by calling `use()`. As you will see below, we declare our uniform in the fragment shader, although you can also use uniforms in vertex shaders.

Our [vertex shader](https://github.com/mattdesl/lwjgl-basics/blob/master/test/res/shadertut/lesson3.vert) is exactly the same as in [Lesson 2](ShaderLesson2). 

Our [fragment shader](https://github.com/mattdesl/lwjgl-basics/blob/master/test/res/shadertut/lesson3.frag) looks like this:

```glsl
//texture 0
uniform sampler2D u_texture;

//our screen resolution, set from Java whenever the display is resized
uniform vec2 resolution;

//"in" attributes from our vertex shader
varying vec4 vColor;
varying vec2 vTexCoord;

//size of our vignette, where 1.0 results in a circle fitting the screen
const float SIZE = 0.75;

//softness of our vignette, between 0.0 and 1.0
const float SOFTNESS = 0.45;

//sepia colour, adjust to taste
const vec3 SEPIA = vec3(1.2, 1.0, 0.8); 

void main() {
	//sample our texture
	vec4 texColor = texture2D(u_texture, vTexCoord);
	
	//determine center position
	vec2 position = (gl_FragCoord.xy / resolution.xy) - vec2(0.5);
	
	//correct for aspect ratio
	position.x *= resolution.x / resolution.y;
	
	//determine the vector length (magnitude) of the center position
	float len = length(position);
	
	//use smoothstep to create a smooth vignette
	float vignette = smoothstep(SIZE, SIZE-SOFTNESS, len);
	
	//apply the vignette with 50% opacity
	texColor.rgb = mix(texColor.rgb, texColor.rgb * vignette, 0.5);
	
	//convert to grayscale using NTSC conversion weights
	float gray = dot(texColor.rgb, vec3(0.299, 0.587, 0.114));
	
	//create our sepia tone from some constant value
	vec3 sepiaColor = vec3(gray) * SEPIA;
		
	//again we'll use mix so that the sepia effect is at 75%
	texColor.rgb = mix(texColor.rgb, sepiaColor, 0.75);
	
	//final colour, multiplied by vertex colour
	gl_FragColor = texColor * vColor;
}
```

What a beast! Here is the scene before any effects:

![Before]()

And here is our scene with vignette and sepia applied:

![After]()

## Step 1: Creating a Circle

To create the vignette effect, we first need to understand how to make a circle. A simple way of making a circle is to calculate the length of a vector from the quad center. To find the center, we need to determine how far the current fragment is along the x- and y-axis of our quad. 

We use the built-in `gl_FragCoord` value, which gives us the `(x, y)` coordinates of the current fragment in the frame buffer. Note that this value uses a *lower left* origin, so `(32, 10)` would mean 32 pixels to the right, 10 pixels *up from the bottom*. However, since our circle is symmetrical and located at center, we do not need to worry about this difference in our specific demo:

```glsl
gl_FragCoord.xy / resolution.xy
```



We subtract `(0.5, 0.5)` so that the length gives us the proper value. If the fragment was at `(0.5, 0.5)` (i.e. center)

***

**Alternative Solution: Texture Coordinates*

If we specify our texture coordinates in the range `[0.0 - 1.0]`, then we can use them to determine where the fragment lies within our quad, instead of relying on a `resolution` uniform. For example, if our texture coordinates were `(0.5, 0.5)` then that fragment would be at the center.

The upside to this is that we could batch many sprites using our post-processing shader, and each one might have different dimensions.

The downside is that not all drivers will support non-power-of-two texture sizes (for example, OpenGL ES 1.1). Typically, non-power-of-two textures will be padded with empty transparent pixels, and then rendered using smaller texture coordinates (i.e. `drawRegion` as we discussed earlier). Since typically we render post-processing effects at the same size (screen size), and since our screen size may not be power-of-two, using a `resolution` uniform is a more flexible solution. 

***

//determine center position
vec2 position = (gl_FragCoord.xy / resolution.xy) - vec2(0.5);

```glsl

	//the most basic solution:
	//texColor.rgb *= vec3(1.0 - length(position));
	//gl_FragColor = texColor * vColor;
```