Often you may want to render rectangles, lines, and squares -- be it for debugging or any other visual purpose. In the programmable pipeline there is no longer `glRect` nor can you simply "disable textures" to render a primitive shape. The solution is to find a 1x1 white opaque pixel in your UI texture atlas from which to sample from (or more pixels if you are using `GL_LINEAR`). Then, you can render boxes, lines, and other basic shapes. 

I added a small 4x4 white square in the font sheet and then grabbed that with a TextureRegion. We also could have created a 1x1 white `GL_NEAREST` Texture with a ByteBuffer, but having multiple textures would not allow us to take advantage of SpriteBatcher. 

You can see the utility methods used in RectTest to draw lines and a rectangle:

```java
void drawRect(int x, int y, int width, int height, int thickness) {
	batch.draw(rect, x, y, width, thickness);
	batch.draw(rect, x, y, thickness, height);
	batch.draw(rect, x, y+height-thickness, width, thickness);
	batch.draw(rect, x+width-thickness, y, thickness, height);
}

void drawLine(int x1, int y1, int x2, int y2, int thickness) {
	int dx = x2-x1;
	int dy = y2-y1;
	float dist = (float)Math.sqrt(dx*dx + dy*dy);
	float rad = (float)Math.atan2(dy, dx);
	batch.draw(rect, x1, y1, dist, thickness, 0, 0, rad); 
}
```

A screenshot of our application:

![Lines](http://i.imgur.com/C89nu.png)

This is a very simple means of rendering shapes. For more advanced polygons, anti-aliasing, stroke effects, and so forth, we may need to take advantage of fragment and geometry shaders. The technique here relies on the CPU to transform each vertex of the line sprite; and under the hood the sprite is a quad made up of two triangles, i.e. six vertices. That's a lot of work just to render a 1 px line segment! In certain cases `GL_LINES` would be much more effective, at the expense of not being able to include it in your sprite batch.