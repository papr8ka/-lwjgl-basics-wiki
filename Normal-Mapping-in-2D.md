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

In our game's fragment shader, we can "decode" the normals by doing the reverse of what we did earlier, expanding the color value to the range -1.0 to 1.0:
```glsl
//sample the normal map
NormalMap = texture2D(NormalMapTex, TexCoord);

//convert to range -1.0 to 1.0
Normal.xyz = NormalMap.rgb * 2.0 - 1.0;
```

*Note:* Keep in mind that different engines and programs will use different coordinate systems, and the green channel may need to be inverted.

# Lambertian Illumination Model

In computer graphics, we have a number of algorithms that can be combined to create different shading results for a 3D object. In this article we will focus on Lambert shading, without any specular (i.e. "gloss" or "shininess"). Other techniques, like Phong, Cook-Torrance, and Oren–Nayar cam be used instead of or in combination with Lambertian shading to produce different visual results (rough surfaces, shiny surfaces, etc).

The entire algorithm looks like this:

```
Normal.xyz = NormalMap.rgb * 2.0 - 1.0
N = normalize(Normal.xyz)
L = normalize(LightDir.xyz)

Diffuse = LightColor * max(dot(N, L), 0.0)
Ambient = AmbientColor * AmbientIntensity
Attenuation = 1.0 / (ConstantAtt + (LinearAtt * Distance) + (QuadraticAtt * Distance * Distance)) 
Intensity = Ambient + Diffuse * Attenuation
FinalColor = DiffuseColor.rgb * Intensity.rgb
```

Although this looks daunting, it's actually very basic. You don't need to understand why this works mathematically, but if you are interested you can read more about "N dot L" shading [here](http://www.lighthouse3d.com/tutorials/glsl-core-tutorial/directional-lights/) and [here](http://en.wikipedia.org/wiki/Lambertian_reflectance).

Let's break it down into steps...


### Step 1: Decode Normal & Convert to Unit Vectors

The first line should be familiar; here we decode the high-quality normal from our normal map, and convert it to the range `-1.0 to 1.0`. 

```
Normal.xyz = NormalMap.rgb * 2.0 - 1.0
```

Then we normalize (convert to unit vector) our vectors before continuing. 

*Note:* For a 3D application, we would need to first convert our light direction from camera space into tangent space. This is explained in further detail [here](http://www.ozone3d.net/tutorials/bump_mapping_p3.php#tangent_space). However, for the purposes of 2D, we do not need to do this calculation as our light direction is already in tangent space (0.0 to 1.0).

```
N = normalize(Normal.xyz)
L = normalize(LightDir.xyz)
```

![NDotL](http://www.lighthouse3d.com/wp-content/uploads/2012/12/lambert.jpg)

<sub>Above we have normalized L, which is the direction from the surface to the light source, and normalized N, which is the normal of our high-quality mesh, sampled from our normal map.</sub>



http://www.upvector.com/?section=Tutorials&subsection=Intro%20to%20Shaders
http://acko.net/blog/making-worlds-3-thats-no-moon/