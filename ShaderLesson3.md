this page is a WIP

--

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

//RADIUS of our vignette, where 0.5 results in a circle fitting the screen
const float RADIUS = 0.75;

//softness of our vignette, between 0.0 and 1.0
const float SOFTNESS = 0.45;

//sepia colour, adjust to taste
const vec3 SEPIA = vec3(1.2, 1.0, 0.8); 

void main() {
	//sample our texture
	vec4 texColor = texture2D(u_texture, vTexCoord);
	
	//determine center position
	vec2 position = (gl_FragCoord.xy / resolution.xy) - vec2(0.5);
	
	//determine the vector length of the center position
	float len = length(position);
	
	//use smoothstep to create a smooth vignette
	float vignette = smoothstep(RADIUS, RADIUS-SOFTNESS, len);
	
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
![Before](http://i.imgur.com/pMm39.png)

And here is our scene with vignette and sepia applied:  
![After](http://i.imgur.com/EUL4t.png)

The steps involved:

- [Step 1: The Basic Vignette](#Step1)
- [Step 2: Circles, `step()` and `smoothstep()`](#Step2)
- [Step 3: Reducing strength with `mix()`](#Step3)
- [Step 4: Grayscale & Sepia](#Step4)

<a name="Step1" />
## Step 1: The Basic Vignette

To create the vignette effect, we first need to understand how to make a circle. A simple way of making a circle is to calculate the length of a vector from the quad center. To find the center, we need to determine how far the current fragment is along the x- and y-axis of our quad. 

We use the built-in `gl_FragCoord` value, which gives us the `(x, y)` coordinates of the current fragment in the frame buffer, divided by the resolution width and height (e.g. `800, 600`).

```glsl
gl_FragCoord.xy / resolution.xy
```

Note that `gl_FragCoord` value uses a *lower left* origin, so `(32, 10)` would mean 32 pixels to the right, 10 pixels *up from the bottom*. However, since our circle is symmetrical and located at center, we do not need to worry about this difference in our specific demo.

We subtract `(0.5, 0.5)` so that we can determine the length from **center**, rather than lower-left (the origin).

```glsl
//determine center
vec2 position = (gl_FragCoord.xy / resolution.xy) - vec2(0.5);	
```

We will use GLSL's built-in `length()` method to determine the length from the center point. Fragments at the center will have a length of zero (i.e. black), and it will increase as we move outward (i.e. into white/gray). We can test the shader so far:

```glsl
//texture 0
uniform sampler2D u_texture;

//our screen resolution, set from Java whenever the display is resized
uniform vec2 resolution;

//"in" attributes from our vertex shader
varying vec4 vColor;
varying vec2 vTexCoord;

void main() {
	//sample our texture
	vec4 texColor = texture2D(u_texture, vTexCoord);
	
	//determine origin
	vec2 position = (gl_FragCoord.xy / resolution.xy) - vec2(0.5);
		
	//determine the vector length of the center position
	float len = length(position);
	
	//show our length for debugging
	gl_FragColor = vec4( vec3(len), 1.0 );
}
```

![Vignette1](http://i.imgur.com/P93CZ.png)

In fact, this is all we need to create a basic vignette effect. Try inverting the length `(1.0 - len)` and multiplying it by our colour:
```glsl
gl_FragColor = vec4( texColor.rgb * (1.0 - len), 1.0 );
```

![Vignette2](http://i.imgur.com/5UPKf.png)

<a name="Step2" />
## Step 2: Circles, `step()` and `smoothstep()`

Another built-in we should look at is `step(edge, x)` and its variants. This function returns 0.0 if x is less than `edge`, otherwise it returns 1.0. It's useful to avoid `if` and `else` statements, which are expensive inside of fragment shaders. If we try it out, you'll notice we've created a sharp-edged circle:

```glsl
//the radius of our circle
float r = 0.5;

gl_FragColor = vec4( vec3( step(r, len) ), 1.0 );
```

![Circle1](http://i.imgur.com/QpLnu.png)

Our circle is squashed because of the aspect ratio. In order to correct for that, we need to include the following *before* we calculate the `length`:
```glsl
position.x *= resolution.x / resolution.y;
```

A variant of the `step` function is `smoothstep(low, high, x)`, which returns 0.0 if x is less than `low` or 1.0 if x is greater than `high`. If x is between the two values, it will linearly interpolate between zero and one. So we can adjust our circle to the following, to gain finer control over how smooth our vignette will look. Here is our updated code:

```glsl
//the radius of our circle
float r = 0.5;

//the softness of our circle edge, between 0.0 and 1.0
float softness = 0.05;

gl_FragColor = vec4( vec3( smoothstep(r, r-softness, len) ), 1.0 );
```

![Circle2](http://i.imgur.com/YIYFv.png)

Using a softness of 0.01 produces a nicely anti-aliased circle, whereas 0.45 produces a nice falloff for a vignette effect. 

Now we can move the radius and softness to constants, and test it out on our texture RGB. Note that we aren't correcting for the aspect ratio here:  
![NewVignette](http://i.imgur.com/8cxUU.png)

```glsl
//texture 0
uniform sampler2D u_texture;

//our screen resolution, set from Java whenever the display is resized
uniform vec2 resolution;

//"in" attributes from our vertex shader
varying vec4 vColor;
varying vec2 vTexCoord;

//RADIUS of our vignette, where 0.5 results in a circle fitting the screen
const float RADIUS = 0.75;

//softness of our vignette, between 0.0 and 1.0
const float SOFTNESS = 0.45;

void main() {
	//sample our texture
	vec4 texColor = texture2D(u_texture, vTexCoord);
	
	//determine center
	vec2 position = (gl_FragCoord.xy / resolution.xy) - vec2(0.5);
	
	//OPTIONAL: correct for aspect ratio
	//position.x *= resolution.x / resolution.y;
	
	//determine the vector length from center
	float len = length(position);
	
	//our vignette effect, using smoothstep
	float vignette = smoothstep(RADIUS, RADIUS-SOFTNESS, len);
	
	//apply our vignette
	texColor.rgb *= vignette;
	
	gl_FragColor = texColor;
}
```

<a name="Step3" />
## Step 3: Reducing strength with `mix()`

<a name="Step4" />
## Step 4: Grayscale & Sepia

<a name="Optimizations" />
##A Note on Optimization

If we specify our texture coordinates in the range `[0.0 - 1.0]`, then we can use them to determine where the fragment lies within our quad, instead of relying on `gl_FragCoord` and a `resolution` uniform. For example, if our texture coordinates were `(0.5, 0.5)` then that fragment would be at the center.

The upside to this is that we could batch many sprites using our post-processing shader, and each one might have different dimensions.

The downside is that not all drivers will support non-power-of-two texture sizes (for example, OpenGL ES 1.1). Typically, non-power-of-two textures will be padded with empty transparent pixels, and then rendered using smaller texture coordinates (i.e. `drawRegion` as we discussed earlier). Since we generally tend to render post-processing effects all using the same screen size, and since our screen size may not be power-of-two, our `resolution` solution is more flexible.