# Setup

You can see the source for this short demo [here](https://github.com/mattdesl/lwjgl-basics/blob/master/test/mdesl/test/shadertut/ShaderLesson4.java). The setup looks a lot like previous lessons, with a couple minor differences. First, we load the following three textures:

![Grass](https://raw.github.com/mattdesl/lwjgl-basics/master/test/res/grass.png) 
![Dirt](https://raw.github.com/mattdesl/lwjgl-basics/master/test/res/dirt.png) 
![Mask](https://raw.github.com/mattdesl/lwjgl-basics/master/test/res/mask.png)

Second, we are setting our uniforms after creating the program, like so:

```java
//create our shader program -- be sure to pass SpriteBatch's default attributes!
program = new ShaderProgram(VERTEX, FRAGMENT, SpriteBatch.ATTRIBUTES);

//Good idea to log any warnings if they exist
if (program.getLog().length()!=0)
	System.out.println(program.getLog());

//bind our program
program.use();

//set our sampler2D uniforms
program.setUniformi("u_texture1", 1);
program.setUniformi("u_mask", 2);
```

(Keep in mind that the uniforms `u_texture` and `u_projView` will be set from SpriteBatch.)

And thirdly, we are binding our textures into different texture units, like so:
```java
//make GL_TEXTURE2 the active texture unit, then bind our mask texture
glActiveTexture(GL_TEXTURE2);
mask.bind();

//do the same for our dirt texture
glActiveTexture(GL_TEXTURE1);
tex1.bind();

//don't forget to set active texture unit back to GL_TEXTURE0 !
glActiveTexture(GL_TEXTURE0);
tex0.bind();
```

`glActiveTexture` specifies the texture unit to use, and `bind()` will bind that texture to the current texture unit. The numbers will line up with the sampler2D uniforms we specified to our fragment shader: e.g. `program.setUniform("u_texture1", 1) => GL_TEXTURE1`. 

It's important to remember that OpenGL is a state-based API. So if you make `GL_TEXTURE1` the active texture, and forget to reset to `GL_TEXTURE0` before trying to render, you may run into problems.

Our [vertex shader](https://github.com/mattdesl/lwjgl-basics/blob/master/test/res/shadertut/lesson4.vert) is the same as in the previous lesson. Here is our [fragment shader](https://github.com/mattdesl/lwjgl-basics/blob/master/test/res/shadertut/lesson4.frag):

```glsl
//"in" attributes from our vertex shader
varying vec4 vColor;
varying vec2 vTexCoord;


//our different texture units
uniform sampler2D u_texture; //default GL_TEXTURE0, expected by SpriteBatch
uniform sampler2D u_texture1; 
uniform sampler2D u_mask;

void main(void) {
	//sample the colour from the first texture
	vec4 texColor0 = texture2D(u_texture, vTexCoord);

	//sample the colour from the second texture
	vec4 texColor1 = texture2D(u_texture1, vTexCoord);

	//get the mask; we will only use the alpha channel
	float mask = texture2D(u_mask, vTexCoord).a;

	//interpolate the colours based on the mask
	gl_FragColor = vColor * mix(texColor0, texColor1, mask);
}
```

![Result](http://i.imgur.com/sIOxq.png)

Note that we are limited by the maximum number of "texture image units" -- we can check with the following:
```java
int maxUnits = glGetInteger(GL_MAX_TEXTURE_IMAGE_UNITS);
```

Most drivers support [up to 16](http://feedback.wildfiregames.com/report/opengl/feature/GL_MAX_TEXTURE_IMAGE_UNITS_ARB) active units. However, if you need that many active texture units, you may need to re-think your design.

This doesn't really cover any new ground<sup>(pun!)</sup>, although it will help get us started with using multiple texture units. 