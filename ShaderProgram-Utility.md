This page will cover the steps required to create your own re-usable ShaderProgram utility class. Alternatively, you can skip this step and use the more advanced ShaderProgram utility already included in lwjgl-basics: [see here](https://github.com/mattdesl/lwjgl-basics/blob/master/src/mdesl/graphics/glutils/ShaderProgram.java).

## Set-Up

For our purposes, we will only use one vertex and one fragment shader to create our shader programs. Since we plan on targeting GL 2.1, we will also need to specify the attribute locations manually. If we were targeting newer versions of OpenGL (i.e. GLSL 330+), then we could specify the attribute locations with [type qualifiers](http://www.opengl.org/wiki/Type_Qualifier_%28GLSL%29%23Vertex_shader_attribute_index) instead. The basic steps to creating a shader program look like this:

1. Compile the vertex shader source into a shader object.
2. Compile the fragment shader source into a shader object.
3. Create a program ID with `glCreateProgram`.
4. Attach the vertex and shader objects to our program with `glAttachShader`. 
5. If we are targeting 2.1, here is where we would bind any attribute locations manually. For example, we would bind the Position attribute to index 0. For this we use `glBindAttribLocation`. If we are targeting newer versions of GLSL, we can skip this step.
6. We then link the program with `glLinkProgram`.
7. If the program succeeded in compiling, we can now detach and delete the vertex and fragment shader objects as they are no longer needed -- using `glDetachShader` and `glDeleteShader`, respectively.

You can see the entire process for that here:
```java
public ShaderProgram(String vertexShader, String fragmentShader, List<VertexAttrib> attributes) throws LWJGLException {
	//compile the String source
	vertex = compileShader(vertexShader, GL_VERTEX_SHADER);
	fragment = compileShader(fragmentShader, GL_FRAGMENT_SHADER);
	
	//create the program
	program = glCreateProgram();
	
	//attach the shaders
	glAttachShader(program, vertex);
	glAttachShader(program, fragment);

	//bind the attrib locations for GLSL 120
	if (attributes != null)
		for (VertexAttrib a : attributes)
			glBindAttribLocation(program, a.location, a.name);

	//link our program
	glLinkProgram(program);

	//grab our info log
	String infoLog = glGetProgramInfoLog(program, glGetProgrami(program, GL_INFO_LOG_LENGTH));
	
	//if some log exists, append it 
	if (infoLog!=null && infoLog.trim().length()!=0)
		log += infoLog;
	
	//if the link failed, throw some sort of exception
	if (glGetProgrami(program, GL_LINK_STATUS) == GL_FALSE)
		throw new LWJGLException(
				"Failure in linking program. Error log:\n" + infoLog);
	
	//detach and delete the shaders which are no longer needed
	glDetachShader(program, vertex);
	glDetachShader(program, fragment);
	glDeleteShader(vertex);
	glDeleteShader(fragment);
}

protected int compileShader(String source, int type) throws LWJGLException {
	//create a shader object
	int shader = glCreateShader(type);
	//pass the source string
	glShaderSource(shader, source);
	//compile the source
	glCompileShader(shader);

	//if info/warnings are found, append it to our shader log
	String infoLog = glGetShaderInfoLog(shader,
			glGetShaderi(shader, GL_INFO_LOG_LENGTH));
	if (infoLog!=null && infoLog.trim().length()!=0)
		log += getName(type) +": "+infoLog + "\n";
	
	//if the compiling was unsuccessful, throw an exception
	if (glGetShaderi(shader, GL_COMPILE_STATUS) == GL_FALSE)
		throw new LWJGLException("Failure in compiling " + getName(type)
				+ ". Error log:\n" + infoLog);

	return shader;
}
```


## Using the Program

In OpenGL, we can only have a single shader program in use at a time. We use `glUseProgram(program)` to specify the active program. In the days of "old school GL", we would specify `glUseProgram(0)` to use the default (fixed-function) shader, but since we are trying to avoid fixed-function, we should never need to call that. In 3.1+ core profile, specifying `0` will give you an error.

```java

```