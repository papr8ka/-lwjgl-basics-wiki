This page is a work in progress.

## Intro to GLSL

GLSL stands for OpenGL Shading Language. Shaders are like small scripts that let us interact with the graphics processor more closely. They are an essential aspect of graphics programming, and can be used for a variety of effects and visuals in your 2D and 3D games. For now, there are two types of shaders you should familiarize yourself with:

### Vertex Shaders

As discussed in the [Textures](https://github.com/mattdesl/lwjgl-basics/wiki/Textures) article, a **vertex** is a point in space with some attributes attached to it, like position (xyz), colour (rgba), texture coordinates (st). A “vertex shader” allows you to interact with this vertex information before sending it along the graphics pipeline to be rendered.

Vertex shaders are often more applicable in 3D graphics programming -- e.g. applying a noise displacement to the vertices of a 3D mesh -- but they are still essential to understand even for 2D games.

### Fragment Shaders

Often called “pixel shaders,” these allow us to modify individual pixels before they are sent along the graphics pipeline. These shaders “output” a RGBA colour. Think of it like a return statement: if we rendered a sprite with a fragment shader that only returned the colour red `(R=1, G=0, B=0, A=1)` – the result would be a red box! 

### Basic Shaders

Vertex and fragment shaders both require a `main()` method. Vertex shaders typically pass the position of the vertex on to GL, like so:

```glsl
//the position of the vertex as specified by our renderer
attribute vec3 Position;

void main() {
    //pass along the position
    gl_Position = vec4(Position, 1.0);
}
```

Whereas fragment shaders typically pass the frag color (i.e. "pixel" color) along, like so:
```glsl
void main() {
    //pass along the color red
    gl_FragColor = vec4(1.0, 0.0, 0.0, 1.0);
}
```

## On to Lesson 1...

[Lesson 1](https://github.com/mattdesl/lwjgl-basics/wiki/ShaderLesson1) covers the basics of writing your own vertex and fragment shaders.

## Further Reading

The best way to learn GLSL is through experimentation and practice. Once you've finished the lessons, check out some online GLSL effects to see how they were achieved:

- http://glsl.heroku.com/
- http://www.iquilezles.org/apps/shadertoy/

If you're feeling comfortable with GLSL, you could also try making your own [shader-based sprite batcher](https://github.com/mattdesl/lwjgl-basics/wiki/CustomRenderer) in order to have a better grasp of how it all comes together.