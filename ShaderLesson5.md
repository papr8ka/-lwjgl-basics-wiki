##### [start](https://github.com/mattdesl/lwjgl-basics/wiki) » [Shaders](Shaders) » Lesson 5: Blurring & Bloom

***

This series relies on the minimal [lwjgl-basics](https://github.com/mattdesl/lwjgl-basics) API for shader and rendering utilities. The code has also been [Ported to LibGDX](#Ports). The concepts should be universal enough that they could be applied to [Love2D](https://love2d.org/), [GLSL Sandbox](http://glsl.heroku.com/), iOS, or any other platforms that support GLSL. 

***

## Setup

This lesson requires understanding the Frame Buffer Object (FBO), so [read up on them](FrameBufferObjects) if you haven't already. Also ensure you are well-versed on the basics of [sprite batching](Sprite-Batching).

The lesson will demonstrate a [gaussian blur](http://en.wikipedia.org/wiki/Gaussian_blur) technique in GLSL inspired by [this article](http://www.gamerendering.com/2008/10/11/gaussian-blur-filter-shader/). The blur is applied in two passes -- horizontally and vertically -- however, our implementation will only require a single fragment shader. 

Here is a visual overview of the two-pass blurring process:

![Overview](http://i.imgur.com/8jkTJ.png)


You can follow along with the source [here](https://github.com/mattdesl/lwjgl-basics/blob/master/test/mdesl/test/shadertut/ShaderLesson5.java). First, we load some textures, then we go on to create our frame buffers:

```java
//create our FBOs
blurTargetA = new FrameBuffer(FBO_SIZE, FBO_SIZE, Texture.NEAREST);
blurTargetB = new FrameBuffer(FBO_SIZE, FBO_SIZE, Texture.NEAREST);
```

We use a square power-of-two size for simplicity as well as maximum compatibility, and take advantage of linear filtering for a smoother blur. I am using `1024` which should encompass most display sizes, but if you plan to support larger resolutions you may need a larger buffer. Keep in mind that we are limited by the maximum texture size. 

Next, we load our shader, print any potential warnings, and setup some default uniform values:

```java
//our basic pass-through vertex shader
final String VERT = Util.readFile(Util.getResourceAsStream("res/shadertut/lesson5.vert"));

//our fragment shader, which does the blur in one direction at a time
final String FRAG = Util.readFile(Util.getResourceAsStream("res/shadertut/lesson5.frag"));

//create our shader program
blurShader = new ShaderProgram(VERT, FRAG, SpriteBatch.ATTRIBUTES);

//Good idea to log any warnings if they exist
if (blurShader.getLog().length()!=0)
	System.out.println(blurShader.getLog());

//always a good idea to set up default uniforms...
blurShader.use();
blurShader.setUniformf("dir", 0f, 0f); //direction of blur; nil for now
blurShader.setUniformf("resolution", FBO_SIZE); //size of FBO texture
blurShader.setUniformf("radius", radius); //radius of blur
```

The `dir` uniform will be a `vec2` defining which direction to blur along. `(1.0, 0.0)` represents the X-axis, and `(0.0, 1.0)` represents the Y-axis. The `resolution` will be used to determine the pixel size in the fragment shader, so we need to give it the `FBO_SIZE`. The last uniform, `radius`, determines the strength of the blur.

Lastly, we set up a sprite batcher initialized with the *default shader*, which we will use in Step 2 (rendering the game entities without any blur).

```java
batch = new SpriteBatch();
```

## Fragment Shader

Our vertex shader hasn't changed from previous lessons. So let's check out the fragment shader:

```glsl
//"in" attributes from our vertex shader
varying vec4 vColor;
varying vec2 vTexCoord;

//declare uniforms
uniform sampler2D u_texture;
uniform float resolution;
uniform float radius;
uniform vec2 dir;

void main() {
	//this will be our RGBA sum
	vec4 sum = vec4(0.0);
	
	//our original texcoord for this fragment
	vec2 tc = vTexCoord;
	
	//the amount to blur, i.e. how far off center to sample from 
	//1.0 -> blur by one pixel
	//2.0 -> blur by two pixels, etc.
	float blur = radius/resolution; 
    
	//the direction of our blur
	//(1.0, 0.0) -> x-axis blur
	//(0.0, 1.0) -> y-axis blur
	float hstep = dir.x;
	float vstep = dir.y;
    
	//apply blurring, using a 9-tap filter with predefined gaussian weights
    
	sum += texture2D(u_texture, vec2(tc.x - 4.0*blur*hstep, tc.y - 4.0*blur*vstep)) * 0.05;
	sum += texture2D(u_texture, vec2(tc.x - 3.0*blur*hstep, tc.y - 3.0*blur*vstep)) * 0.09;
	sum += texture2D(u_texture, vec2(tc.x - 2.0*blur*hstep, tc.y - 2.0*blur*vstep)) * 0.12;
	sum += texture2D(u_texture, vec2(tc.x - 1.0*blur*hstep, tc.y - 1.0*blur*vstep)) * 0.15;
	
	sum += texture2D(u_texture, vec2(tc.x, tc.y)) * 0.16;
	
	sum += texture2D(u_texture, vec2(tc.x + 1.0*blur*hstep, tc.y + 1.0*blur*vstep)) * 0.15;
	sum += texture2D(u_texture, vec2(tc.x + 2.0*blur*hstep, tc.y + 2.0*blur*vstep)) * 0.12;
	sum += texture2D(u_texture, vec2(tc.x + 3.0*blur*hstep, tc.y + 3.0*blur*vstep)) * 0.09;
	sum += texture2D(u_texture, vec2(tc.x + 4.0*blur*hstep, tc.y + 4.0*blur*vstep)) * 0.05;

	//discard alpha for our simple demo, multiply by vertex color and return
	gl_FragColor = vColor * vec4(sum.rgb, 1.0);
}
```

<a name="Ports" />

## Other APIs

work in progress