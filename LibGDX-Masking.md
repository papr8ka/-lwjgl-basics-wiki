### Masking Rectangles

Rendering a sprite masked by a rectangle is dead simple in LibGDX and OpenGL. We simply draw a TextureRegion to our SpriteBatch, which acts as a sub-region of a texture:
```java
TextureRegion myRegion;

 ... create
    myRegion = new TextureRegion(texture, x, y, width, height);

 ... render    
    batch.draw(myRegion, x, y);
```

To mask a series of overlapping sprites, such as a GUI element that may contain some text, we can use glScissor and `SCISSOR_TEST`. It looks like this, assuming we are using the standard y-up coordinate system:

```java
Gdx.gl.glEnable(GL10.GL_SCISSOR_TEST);
Gdx.gl.glScissor(clipX, clipY, clipWidth, clipHeight);

batch.begin();
//draw sprites to be clipped
batch.draw(sprite, 0, 0, 250, 250);
batch.end();

Gdx.gl.glDisable(GL10.GL_SCISSOR_TEST);
```

Note that we need to `end()` the batch before disabling scissor testing. Another approach is to call `flush()` on the SpriteBatch, which forces the data to be sent to GL. This allows us to, say, have the following flow:

```java
batch.begin();

//draw sprites
batch.draw(...);

//flush with current GL states
batch.flush();

//now we can change the GL state for future rendering...
Gdx.gl.glXXXXXXX(...);

//continue drawing
batch.draw(...);

//end the batch once we're all finished
batch.end();
```

Sometimes it can be a bit faster to just flush a batch, rather than calling `end()` followed by `start()`.

# Masking Shapes

Masking something other than an axis-aligned rectangle becomes a little bit more difficult. Here are some common approaches.

## Masking in Software

This is the approach taken by frameworks like Java2D and other high-level 2D renderers. The idea here is to apply the mask in software, by manipulating the RGBA data of a Pixmap, and then send the new pixels to the GPU through `Texture.drawPixmap`. This is an ideal solution for a scene that does not need to be rendered or updated frequently, as it allows full control over each pixel; however, it is not suitable for real-time use, especially not on Android or iOS. We won't discuss this in much detail here, but if you are interested the [LibGDX Textures](LibGDX-Textures) tutorial would be a good place to start.

## Masking with Stencil Buffer

An old-school technique in OpenGL for masking is to use the stencil buffer. The basic idea is to render your primitives (such as those created by ShapeRenderer) to the stencil buffer, then render your scene with stencil buffer testing enabled to apply the clipping. The downside is that you lose anti-aliasing (such as a smooth edge to a circle).

If you choose this route, make sure to enable the stencil buffer with `AndroidApplicationConfiguration.stencil` (e.g. set it to 8 bits). 

## Masking with Depth Buffer

Another approach is to use the depth buffer to discard pixels in hardware. Here, we clear the depth buffer with 1.0f, then draw our shapes to the depth buffer at 0.0. We then render our scene with depth testing enabled, and `GL_GEQUAL`

## Notes

- Anti-aliasing is enabled by default in WebGL, at least in major browsers like Chrome and Firefox
- Remember to flush() or end your batch before changing GL states. This includes things like setting the blend and depth functions and enabling/disabling a GL state.