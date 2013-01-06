# Intro to Normals

There is lots of information on the web regarding 3D normal mapping, but this article will put more emphasis on applying the technique to 2D games. A "surface normal" is a vector perpendicular to the tangent plane. In simpler terms, it's a vector that is perpendicular to the mesh at a given vertex. It's easier to explain with a picture:  
![Mesh1](http://i.imgur.com/QnfZ4.png)

Each vector points outward, following the curvature of the mesh. Here is another example, this time a 2D side view:
![Light](http://i.imgur.com/5EH9m.png)

We use this information to calculate lighting on a 3D shape. Many 3D games use normal mapping to give high quailty shading to a low poly mesh. The artist needs to create two models: low and high poly (the high poly is often called a "sculpt"). The normal information of the high poly mesh is encoded into a texture. Then, in game, you render the low poly mesh, but light each fragment using the high poly surface normals. The result:  
![RealTime](http://i.imgur.com/17dVa.png)

## Encoding Normals

Our surface normals are typically in the range -1.0 to 1.0. We can store the normal vector `(x, y, z)` in a RGB texture by converting the normal to the range 0.0 to 1.0. Here is some pseudo-code:
```glsl
Color.rgb = Normal.xyz / 2.0 + 0.5;
```

For example, a normal of `(-1, 0, 1)` would be encoded as RGB `(0, 0.5, 1)`. The x-axis (left/right) is stored in the red channel, the y-axis (up/down) stored in the green channel, and the z-axis (forward/backward) is stored in the blue channel. The resulting "normal map" looks ilke this:  
![NormalMap](http://i.imgur.com/pgfKp.png)

It's clearer to look at each channel individually:  
![Channels](http://i.imgur.com/ppXbS.png)

Looking at the green channel, we see the brighter parts (values closer to `1.0`) define areas where the normal would point upward, whereas darker areas (values closer to `0.0`) define areas where the normal would point downward. Most normal maps will have a bluish tint because the Z axis (blue channel) is generally pointing toward us (i.e. value of `1.0`). 

In our game's fragment shader, we can "decode" the normals in our fragment shader by doing the reverse of what we did earlier, expanding the color value to the range -1.0 to 1.0:
```glsl
//sample the normal map
NormalMap = texture2D(NormalMapTex, TexCoord);

//convert to range -1.0 to 1.0
Normal.xyz = NormalMap.rgb * 2.0 - 1.0;
```

# Lambert Shading

There are a number of 

http://www.upvector.com/?section=Tutorials&subsection=Intro%20to%20Shaders
http://acko.net/blog/making-worlds-3-thats-no-moon/