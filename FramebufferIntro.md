A common feature in 2D and 3D graphics programming is the ability to render to a texture. For example, say we have a slider GUI component made up of multiple sprites (the track, and the thumb button). Now, what if we wanted to reduce the opacity of the component? If we tried rendering each sprite at 50% opacity, we will notice an ugly looking overlap where the two sprites blend together. One solution to this is to render both sprites at 100% opacity to an "offscreen image", and then render that image to the screen at 50% opacity.

![Opacity](http://i.imgur.com/RsM5G.png)

(Slider PSD can be downloaded [here](http://files.pixelsdaily.com/download/id/2950))