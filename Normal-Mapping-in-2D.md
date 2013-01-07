- preface

This article will focus on 3D lighting and normal mapping techniques and how we can apply them to 2D games.

![Pixels](http://i.imgur.com/S6ElW.gif)

# Intro to Normals

As we've discussed in past lessons, a GLSL "vector" is a float container that typically holds values such as position; `(x, y, z)`. In mathematics, vectors mean quite a bit more, and are used to denote length (i.e. magnitude) and direction. If you're new to vectors and want to learn a bit more about them, check out some of these links:

- [Basic 3D Math](http://www.matrix44.net/cms/notes/opengl-3d-graphics/basic-3d-math-vectors)
- [Vector Math for Graphics](http://programmedlessons.org/VectorLessons/index.html)
- [Mathematics of Vectors Applied to Graphics](http://3dgep.com/?p=359)

To calculate lighting, we need to use the "normal" vectors of a mesh. A surface normal is a vector perpendicular to the tangent plane. In simpler terms, it's a vector that is perpendicular to the mesh at a given vertex. Below we see a mesh with the normal for each vertex.  
![Mesh1](http://i.imgur.com/QnfZ4.png)

Each vector points outward, following the curvature of the mesh. Here is another example, this time a simplified 2D side view:  
![LightLow](http://i.imgur.com/MLTGx.png)

"Normal Mapping" is a game programming trick that allows us to render the same number of polygons (i.e. a low-res mesh), but use the normals of our high-res mesh when calculating the lighting. This gives us a much greater sense of depth, realism and smoothness:  
![Light](http://i.imgur.com/5EH9m.png)

<sub>(Images from [this great blog post](http://acko.net/blog/making-worlds-3-thats-no-moon/))</sub>

The normals of the high poly mesh or "sculpt" are encoded into a texture (AKA normal map), which we sample from in our fragment shader while rendering the low poly mesh. The results speak for themselves:  
![RealTime](http://i.imgur.com/17dVa.png)

## Encoding Normals

Our surface normals are unit vectors typically in the range -1.0 to 1.0. We can store the normal vector `(x, y, z)` in a RGB texture by converting the normal to the range 0.0 to 1.0. Here is some pseudo-code:
```glsl
Color.rgb = Normal.xyz / 2.0 + 0.5;
```

For example, a normal of `(-1, 0, 1)` would be encoded as RGB `(0, 0.5, 1)`. The x-axis (left/right) is stored in the red channel, the y-axis (up/down) stored in the green channel, and the z-axis (forward/backward) is stored in the blue channel. The resulting "normal map" looks ilke this:  
![NormalMap](http://i.imgur.com/pgfKp.png)

It's clearer to look at each channel individually:  
![Channels](http://i.imgur.com/ppXbS.png)

Looking at, say, the green channel, we see that the brighter parts (values closer to `1.0`) define areas where the normal would point upward, whereas darker areas (values closer to `0.0`) define areas where the normal would point downward. Most normal maps will have a bluish tint because the Z axis (blue channel) is generally pointing toward us (i.e. value of `1.0`). 

In our game's fragment shader, we can "decode" the normals in our fragment shader by doing the reverse of what we did earlier, expanding the color value to the range -1.0 to 1.0:
```glsl
//sample the normal map
NormalMap = texture2D(NormalMapTex, TexCoord);

//convert to range -1.0 to 1.0
Normal.xyz = NormalMap.rgb * 2.0 - 1.0;
```

*Note:* Keep in mind that different engines and programs will use different coordinate systems, and the green channel may need to be inverted.

# Lambert Shading

There are a number of 

http://www.upvector.com/?section=Tutorials&subsection=Intro%20to%20Shaders
http://acko.net/blog/making-worlds-3-thats-no-moon/