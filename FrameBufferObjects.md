A common feature in 2D and 3D graphics programming is the ability to render to a texture. For example, say we have a slider GUI component made up of multiple sprites (the track, and the thumb button), and we are trying to fade it in/out. When we render each sprite at 50% opacity, we get some ugly blending where the sprites meet. The solution is to render the entire component at 100% opacity to an "offscreen texture", **then** render the offscreen texture to the screen at 50%.

![Opacity](http://i.imgur.com/RsM5G.png)

(Slider PSD can be downloaded [here](http://files.pixelsdaily.com/download/id/2950))
