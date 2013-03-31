## Intro

Detailed here is an approach to 2D pixel-perfect shadows using shaders and the GPU. Because of the high fill rate and multiple passes involved, this is generally less performant than geometry shadows; however, it has a number of benefits. It will be implemented in LibGDX, although the concepts can be applied to any OpenGL/GLSL framework.

The basic steps involved are (1) render occluders to a FBO, (2) build a 1D shadow map, (3) render shadows and sprites.  
![Img](http://i.imgur.com/vcaWNof.png)

The following animation demonstrates the technique:  
![Visual](http://i.imgur.com/qcH7G.gif)

The idea is an extension of my [previous attempts](http://www.java-gaming.org/topics/starbound-lighting-techneques/26363/msg/230988/view.html#msg230988) at shader-based shadows, which combines [ideas from various sources](#further-reading). However, "nego" on LibGDX forums suggested some great ideas to reduce the process into fewer passes.


<a name="further-reading" />
## Further Reading

- [Catalin's Article, the original inspiration](http://www.catalinzima.com/2010/07/my-technique-for-the-shader-based-dynamic-2d-shadows/)
- http://rabidlion.com/?p=10
- http://www.gmlscripts.com/forums/viewtopic.php?id=1657