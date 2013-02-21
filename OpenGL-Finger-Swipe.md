Surely most of you are familiar with the Fruit Ninja type of games. This series will cover replicating the Swipe effect in OpenGL ES using LibGDX.

![Swipe](http://i.imgur.com/6nFRZDi.png)  
<sup>Screenshot from Fruit Ninja, a popular touch-based game</sup>


The result of our project will look something like this:  
![Proj](http://i.imgur.com/m61ar9v.gif)

Below is a break-down of the steps involved:

1. Capture Input
2. Simplify path
3. Smooth path
4. Extrude to triangle strips
5. Fast anti-aliasing and stroke effects

## 1. Capture Input

The first step is very simple. We need to capture the last N input points and store them in a list. For this we will shift all current elements in the list to the right, and then replace the first element with our new input point. Using LibGDX's Array utility, we can "insert" elements without growing the backing array like so:

```java
// direct access REQUIRES that we created the Array with the Class<T> constructor
Vector2[] items = list.items;

// increase size if we have a new point
// items.length (array size) represents our fixed-length capacity
list.size = Math.min(list.size + 1, items.length);

// shift elements right
for (int i = list.size - 1; i > 0; i--) {
	items[i] = items[i - 1];
}

// insert new item at first index
items[0] = t;
```

We insert our first point in `touchDown`, and subsequent points in `touchDragged`.

Note that direct access to Array's `list` only works if we created the array with the `Class<T>` constructor. You can see my [FixedList implementation here](https://gist.github.com/mattdesl/5002527). You may choose to modify an existing Java collection, instead.

We determine how many input points to "remember" by setting the Array's capacity. Using a greater capacity will lead in longer "swipe trails," while smaller capacity will lead to shorter trials. 

## 2. Simplify the Path

If we were to render the current input with ShapeRenderer and lines, we'd notice some issues. Firstly, if the user swipes too slowly, or simply touches the screen, they will be left with a very small trail made up of many points. Secondly, if the user swipes too quickly, it may lead to "jagged" and sharp corners:  
![Corners](http://i.imgur.com/VKyhA6s.png)

Another problem becomes visible when we test on the Android device. The touch screen input is not always accurate, and often fails with diagonal lines -- leading to "zig-zag" or stepped paths. The effect is demonstrated [here](http://obamapacman.com/2010/01/iphone-wins-smartphone-touchscreen-performance-test-better-than-nexus-one-droid/) and leads to ugly diagonal lines like this:  
![Diag](http://i.imgur.com/04saiAf.png)

To start, we can set a minimum distance between input points, only inserting new points if the length from the last exceeds the minimum distance. This forces the user to put a little more effort into their swipes, and ignores small input touches. It will also help us simplify the lines a little, which will prove useful in our next step.

```java
//determine squared distance between input and last point
float lenSq = tmpVec.set(inputPoint).sub(lastPoint).len2();

//the minimum distance between input points, squared
if (lenSq >= minDistanceSq) {
    ... insert new point ...
}
```

The next step is to simplify the lines, removing some of the "zig-zag" effect. For this we use a simple [radial distance](http://psimpl.sourceforge.net/radial-distance.html) algorithm because it's very fast and leads to pretty nice results. You may choose to use another algorithm.

The following code was adapted from [simplify.js](http://mourner.github.com/simplify-js/). You should clear the `out` array before calling. An `out` parameter is used to avoid allocating new objects in the game loop.

```java
private static Vector2 point = new Vector2(); //shared instance
...

public static void simplify(Array<Vector2> points, float sqTolerance, Array<Vector2> out) {
	int len = points.size;

	Vector2 prevPoint = points.get(0);
	
	out.clear();
	out.add(prevPoint);
	
	//shared point, reset to (0, 0)
	point.set(0, 0);
	
	for (int i = 1; i < len; i++) {
		point = points.get(i);
		if (distSq(point, prevPoint) > sqTolerance) {
			out.add(point);
			prevPoint = point;
		}
	}
	if (!prevPoint.equals(point)) {
		out.add(point);
	}
}

public static float distSq(Vector2 p1, Vector2 p2) {
	float dx = p1.x - p2.x, dy = p1.y - p2.y;
	return dx * dx + dy * dy;
}
```

We can play with the tolerance to get a more or less simplified path. Using 35<sup>2</sup> seems to work well for our purposes. The red line shows the simplified result, the gray line shows the raw input:  
![RadialDistance](http://i.imgur.com/2NfgN7m.png)
