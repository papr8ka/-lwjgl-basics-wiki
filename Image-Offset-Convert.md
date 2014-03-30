java
```java
//offset to (x, y)
int y = i / width;
int x = i - width*y;

//(x, y) to offset
int i = x + (y * w);
```

js:
```js
var x = i % width,
    y = ~~( i / width );
```

```
int value = pixmap.getPixel(x, y);
int R = ((value & 0xff000000) >>> 24);
int G = ((value & 0x00ff0000) >>> 16);
int B = ((value & 0x0000ff00) >>> 8);
int A = ((value & 0x000000ff));
```