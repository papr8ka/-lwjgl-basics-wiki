Surely most of you are familiar with the Fruit Ninja type of games. This series will cover replicating the Swipe effect in OpenGL ES using LibGDX.

![Swipe](http://i.imgur.com/6nFRZDi.png)  
<sup>Screenshot from Fruit Ninja, a popular touch-based game</sup>


The result of our project will look something like this:  
![Proj](http://i.imgur.com/m61ar9v.gif)

Below is a break-down of the steps involved:

1. Capture Input
2. Simplify
3. Smooth
4. Extrude To Triangle Strip
5. Fast Anti-Aliasing and Stroke Effects

## 1. Capture Touch Input

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

## 2. Simplify

The first problem you might notice is that merely touching the screen is registered as a swipe. We don't want a swipe to be registered unless the user actually performs a swipe gesture. A quick fix is to only insert new points if they exceed a *minimum distance* from our last point. This forces the user to put a little more effort into their swipes, and discards very small swipes. It will also help us simplify the lines a little, reducing the point count, which will prove useful in our next step.

```java
//determine squared distance between input and last point
float lenSq = tmpVec.set(inputPoint).sub(lastPoint).len2();

//the minimum distance between input points, squared
if (lenSq >= minDistanceSq) {
    ... insert new point ...
}
```

Another issue becomes apparent when we try swiping on an actual Android device. The touch screen input is not always accurate -- leading to "zig-zag" or stepped paths whenever the user tries to swipe diagonally. The effect is demonstrated [here](http://obamapacman.com/2010/01/iphone-wins-smartphone-touchscreen-performance-test-better-than-nexus-one-droid/) and leads to ugly diagonal swipes like this:  
![Diag](http://i.imgur.com/04saiAf.png)

To fix this, we need to simplify our input line. I chose to use a [radial distance](http://psimpl.sourceforge.net/radial-distance.html) algorithm because it's very fast and leads to pretty decent results. You may choose to use another algorithm.

The following code was adapted from [simplify.js](http://mourner.github.com/simplify-js/). An `out` parameter is used to avoid allocating new objects in the game loop.

```java
public static void simplify(Array<Vector2> points, float sqTolerance, Array<Vector2> out) {
	int len = points.size;

	Vector2 point = new Vector2();
	Vector2 prevPoint = points.get(0);
	
	out.clear();
	out.add(prevPoint);
	
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


## Smooth

The next thing you'll notice is "jagged" corners on fast swipes. As you can see, this is even more apparent now that we've simplified our path:  
![Corners](http://i.imgur.com/XmJDF0L.png)

One solution to this is to use [natural cubic splines](http://en.nicoptere.net/?p=210) or even Bezier curves to produce a smooth contour. However, [Chaikin's smoothing algorithm](http://www.idav.ucdavis.edu/education/CAGDNotes/Chaikins-Algorithm/Chaikins-Algorithm.html) is easy to implement, leads to a predictable contour, and efficient enough for our purposes. The following is a single iteration of our Chaikin smooth:

```java
public static void smooth(Array<Vector2> input, Array<Vector2> output) {
	//expected size
	output.clear();
	output.ensureCapacity(input.size*2);
	
	//first element
	output.add(input.get(0));
	//average elements
	for (int i=0; i<input.size-1; i++) {
		Vector2 p0 = input.get(i);
		Vector2 p1 = input.get(i+1);

		Vector2 Q = new Vector2(0.75f * p0.x + 0.25f * p1.x, 0.75f * p0.y + 0.25f * p1.y);
		Vector2 R = new Vector2(0.25f * p0.x + 0.75f * p1.x, 0.25f * p0.y + 0.75f * p1.y);
        	output.add(Q);
	        output.add(R);
	}
	
	//last element
	output.add(input.get(input.size-1));
}
```

So now our method to "resolve" an input path (simplify and smooth) looks something like this:

```java
private Array<Vector2> tmp = new Array<Vector2>(Vector2.class);

public static int iterations = 2;
public static float simplifyTolerance = 35f;

//Simplify and smooth input, storing the result in output
public void resolve(Array<Vector2> input, Array<Vector2> output) {
	output.clear();
	if (input.size<=2) { //simple copy
		output.addAll(input);
		return;
	}

	//simplify with squared tolerance
	if (simplifyTolerance>0 && input.size>3) {
		simplify(input, simplifyTolerance * simplifyTolerance, tmp);
		input = tmp;
	}
	
	//perform smooth operations
	if (iterations<=0) { //no smooth, just copy input to output
		output.addAll(input);
	} else if (iterations==1) { //1 iteration, smooth to output
		smooth(input, output);
	} else { //multiple iterations.. ping-pong between arrays
		int iters = iterations;
		//subsequent iterations
		do {
			smooth(input, output);
			tmp.clear();
			tmp.addAll(output);
			Array<Vector2> old = output;
			input = tmp;
			output = old;
		} while (--iters > 0);
	}
}
```

Using 2 iterations, we get quite a nice curve when the user quickly swipes a corner:  
![Curve](http://i.imgur.com/WXFnDLv.png)


## Extrude to Triangle Strip

The next step delves a little into some basic vector math. To create our geometry, we will use the perpendicular vector of each point on our path. We skip the first and last points, since we want the swipe to taper into a sharp tip. Here is an image that demonstrates the process:  

![Vectors](http://i.imgur.com/lQlRjIR.png)

The steps are as follows, with LibGDX vectors. We use a shared instance `tmp` to avoid unnecessary allocations.

1. Find the direction and normalize it: `tmp.set(p2).sub(p1).nor()`
2. Get the perpendicular of the normalized direction: `tmp.set(-tmp.y, tmp.x)`
3. Extrude outward by half thickness: `tmp.mul(thickness/2f)`

Then we can determine point A with `p1.add(tmp)` or B with `p1.sub(tmp)`. For a variable thickness, resulting a taper at the far end of the trail, we simply reduce the thickness based on how far we are from the initial point (i.e. the user's finger).

When we plug the points into a triangle strip, we get a pretty good result:  
![Trail1](http://i.imgur.com/5QhTQAJ.png)

It looks a bit better if we extend the head and tail points outward by a certain amount. To extend the head, you might use `tmp.set(p1).sub(p2).mul(endcapScale)`, and similar code to extend the tail.

![Extended](http://i.imgur.com/vF5IDPC.png)

## Anti-Aliasing and Stroke Effects

TODO