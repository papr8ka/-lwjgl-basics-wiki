Our blurring technique described in [Shader Lesson 5](ShaderLesson5) is fairly efficient on desktop, but won't hold up on more limited devices such as Android and iOS. This is largely because of the fill-rate and multiple passes involved, as well as other factors such as sending uniform data, which contribute to the poor performance. 

By downsampling the frame buffer to 50%, we can achieve a frame rate of ~30 FPS on the Samsung Galaxy Tab II (7"). This is not really acceptable, though, considering we'd like to target some lower end hardware, and our current technique is not very practical for most game dev purposes.

Before we begin optimizing, it's important to consider the actual *practical usage* of our blurring. If we are developing an image processing application, then maybe we can get away with non-realtime performance. For a game, though, we may need to blur multiple objects. Below we discuss a few other tricks to achieve blurs on OpenGL ES.

# Depth-of-Field Tricks

