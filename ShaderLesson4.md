# Setup

You can see the source for this short demo [here](https://github.com/mattdesl/lwjgl-basics/blob/master/test/mdesl/test/shadertut/ShaderLesson4.java). The setup looks a lot like previous lessons, with a couple minor differences. First, we are loading three textures instead of one. Second, we are setting our uniforms after creating the program, like so:

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

(Keep in mind that the `u_texture` and `u_projView` uniforms will be set from SpriteBatch.)

And thirdly, we are binding our textures into different texture units like so:
```java
//make GL_TEXTURE2 the active texture unit, then bind our mask texture
glActiveTexture(GL_TEXTURE2);
mask.bind();

//do the same for our other two texture units
glActiveTexture(GL_TEXTURE1);
tex1.bind();

//set active texture back to GL_TEXTURE0 before rendering
glActiveTexture(GL_TEXTURE0);
tex0.bind();
```

`glActiveTexture` specifies the texture unit to use, and `bind()` will bind that texture to the current texture unit. The numbers will line up with the sampler2D uniforms we specified to our fragment shader: e.g. `GL_TEXTURE1 => program.setUniform("u_texture1", 1)`. It's important to remember that OpenGL is a state-based API. So if you make `GL_TEXTURE1` the active texture, and forget to reset to `GL_TEXTURE0` before trying to render, you may run into problems.

Our [vertex shader](https://github.com/mattdesl/lwjgl-basics/blob/master/test/res/shadertut/lesson4.vert) is the same as in the previous lesson. Here is our [fragment shader](https://github.com/mattdesl/lwjgl-basics/blob/master/test/res/shadertut/lesson4.frag):

```glsl
//the default texture 0 (grass.png), expected by SpriteBatch
uniform sampler2D u_texture;

//texture 1 (dirt.png)
uniform sampler2D u_texture1;

//texture 2 (mask.png)
uniform sampler2D u_mask;

//"in" varyings from vertex shader
varying vec4 vColor;
varying vec2 vTexCoord;

void main(void) {
	vec4 texColor0 = texture2D(u_texture, vTexCoord);
	vec4 texColor1 = texture2D(u_texture1, vTexCoord);
	float mask = texture2D(u_mask, vTexCoord).a;
	gl_FragColor = vColor * mix(texColor0, texColor1, mask);
}
```