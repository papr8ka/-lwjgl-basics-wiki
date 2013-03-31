Detailed here is an approach to 2D pixel-perfect shadows using shaders and the GPU. Because of the high fill rate and multiple passes involved, this is generally less performant than geometry shadows; however, it has a number of benefits. It will be implemented in LibGDX, although the concepts can be applied to any OpenGL/GLSL framework.


The basic steps involved:   
![Img](http://i.imgur.com/vcaWNof.png)

1. Render occluders (shadow casters) to a FBO; if they cast a shadow, they will be opaque, otherwise transparent.

2. Build a 1-dimensional "shadow map" from our occluders. The x-axis represents angle (theta), and the colour represents the minimum distance from light center to the nearest occluder.

3. Using the 1D shadow map, render our blurred shadows. Then render our sprites on top.

Here is a visual demonstration of the technique:  
![Visual](http://i.imgur.com/qcH7G.gif)

The idea is an extension of my [previous attempts](http://www.java-gaming.org/topics/starbound-lighting-techneques/26363/msg/230988/view.html#msg230988) at shader-based shadows, which combines [ideas from various sources](#Further-Reading). However, "nego" on LibGDX forums suggested some great ideas to reduce the process into fewer passes.



## Further Reading

- http://www.catalinzima.com/2010/07/my-technique-for-the-shader-based-dynamic-2d-shadows/
- http://rabidlion.com/?p=10
- http://www.gmlscripts.com/forums/viewtopic.php?id=1657