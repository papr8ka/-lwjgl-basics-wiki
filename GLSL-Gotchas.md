There are some gotchas to be aware of when working with GLSL on various platforms.

## Mac OSX

- Array declaration is broken on Snow Leopard [(1)](http://openradar.appspot.com/6121615)

## ES (Android, iOS, WebGL)

- Be mindful of `step()` as it may create branching (although it really shouldn't). Benchmark with `smoothstep()` to see if performance improves.
- Ternary operator may not be supported on certain Android devices [(1)](http://badlogicgames.com/forum/viewtopic.php?f=15&t=7893)
- 'For' loops may cause problems on certain Android devices [(1)](http://badlogicgames.com/forum/viewtopic.php?f=15&t=7801&p=35649&hilit=tegra#p35649)