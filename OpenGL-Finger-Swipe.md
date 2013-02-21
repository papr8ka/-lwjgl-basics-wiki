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

The first step is very simple. We need to capture the last N input points and store them in a list. For this we will shift all current elements in the list to the right, and then replace the first element with our new input point. Using LibGDX's Array utility, we can modify it like so:

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

Note that direct access to Array's `list` only works if we created the array with the `Class<T>` constructor. Other uses may demand their own collection implementation. 

Using a greater capacity will lead in longer "swipe trails," while smaller capacity will lead to a shorter effect. We reduce the input by only inserting new points when the length from the last point exceeds a certain amount.

```java
//determine squared distance between input and last point
float lenSq = tmpVec.set(inputPoint).sub(lastPoint).len2();

//the minimum distance between input points, squared
if (lenSq >= minDistanceSq) {
    ... insert new point ...
}
```

## 2. Simplify the Path
