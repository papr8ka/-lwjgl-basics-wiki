```java
//offset to (x, y)
int y = i / width;
int x = i - width*y;

//(x, y) to offset
int i = x + (y * w);
```