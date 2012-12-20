An important feature of any 2D rendering system is a "batcher" -- this will allow us to render many sprites in a single draw call. Using the batcher correctly will allow us to render tens of thousands of sprites per frame at 60+ FPS.

As discussed in the [Textures](Textures) tutorial, a sprite is nothing more than a set of vertices that make up a rectangular shape. Each vertex has the attributes `Position(x, y)` (where the vertex lies), `TexCoord(s, t)` (what region of our Texture we want to render) and `Color(r, g, b, a)` (to specify tinting or transparency). From the outside, most sprite batchers look fairly simple to use:

```java
//prepare the batch for rendering
spriteBatch.begin();

//draw all of our sprites
spriteBatch.draw(mySprite1, x, y);
spriteBatch.draw(mySprite2, x, y);
...

//end the batch, flushing the data to GPU
spriteBatch.end();
```

When we call `spriteBatch.draw(...)`, this simply pushes the sprite's vertex information (position, texcoord, color) onto a very large stack. The vertices aren't passed to the GPU until one of the following occurs:

- The batch is forced to render with `end()` or another call that flushes the batch (like `flush()`)
- The user tries drawing a sprite that uses a different Texture than the last one.
- We have reached the capacity of our stack, so we need to flush to start over again

This is the basic idea behind a sprite batcher. As you can see, using many textures will lead to many draw calls (as the batch will need to flush for each new texture). This is why a texture atlas (AKA sprite sheet) is always recommended; it allows us to render many sprites (sub-regions of our texture atlas) in a single draw call.

## Vertex Color

We can change the tinting and transparency of our sprites by setting the batch color, AKA "vertex color." The RGB will be multiplied by the texture color; so if our texture was white `(1, 1, 1, 1)` and we specified a vertex color of `(1, 0, 0, 1)`, the result would be red. The Alpha component allows us to adjust the opacity of sprites rendered to screen.

```java
spriteBatch.begin();

//draw calls will now use 50% opacity
spriteBatch.setColor(1f, 1f, 1f, 0.5f);
spriteBatch.draw(...);
spriteBatch.draw(...);

//draw calls will now use 100% opacity (default)
spriteBatch.setColor(1f, 1f, 1f, 1f);
spriteBatch.draw(...);

spriteBatch.end();
```

## Triangles, not Quads

In the earlier series, we have been thinking of textures as quads, but in reality most sprite batchers will use two adjacent triangles to represent a rectangular sprite. So each sprite has 6 vertices (two triangles), and each vertex has 8 attributes (`X, Y, S, T, R, G, B, A`)



We call this "vertex coloring" because the color is an attribute specified with each vertex, along with `Position` and `TexCoord`. We could actually have a sprite fade out from left to right by using `(1, 1, 1, 1)` for the upper left and lower left vertex colors, and `(1, 1, 1, 0)` for the upper right and lower right colors. Since this is not a common task, you would need to specify your sprite's vertices manually in order to do that:
```java
    /* Renders a sprite with custom vertex data.
    @param tex - the texture to use
    @param vertices - an array of 6 vertices, each holding 8 attributes (total = 48 elements)
    @param offset - starting offset to read from vertices array */
SpriteBatch.draw(Texture tex, float[] vertices, int offset)
```