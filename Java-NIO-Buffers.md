This is a short introduction to Java NIO buffers, which are commonly used in LWJGL to handle GL data. For a more detailed look at buffers, [see here](http://tutorials.jenkov.com/java-nio/buffers.html).

### Intro
A buffer is simply a block of memory which holds some data. For our purposes, you can think of it as an array of elements. However, instead of random access (e.g. `array[i]`), Buffers read and write data relative to their current position. To demonstrate, let's say we wish to create a buffer which holds four bytes, and then read those bytes out. You would create it like so:
```java
//LWJGL includes utilities for easily creating buffers
ByteBuffer buffer = BufferUtils.createByteBuffer(4);

//"relative put" method, which places the byte and 
//then moves the position forward
buffer.put(a);
buffer.put(b);
buffer.put(c);
buffer.put(d);

//flip the position to reset the relative position to zero
buffer.flip();

//loop through all of the bytes that were written, using "relative get"
for (int i=0; i<buffer.limit(); i++) {
    System.out.println( buffer.get() );
}
```

To understand what's happening, comparing it to a Java array:
```java
//creating the fixed-size array..
byte[] array = new byte[4];

//position starts at 0
int position = 0;

//using a relative "put", position inreases each time
array[position++] = a;
array[position++] = b;
array[position++] = c;
array[position++] = d;

//"flipping" our position/limit
int limit = position;
position = 0;

//printing our values
for (int i=0; i<limit; i++) {
    //using a relative "get", position inreases each time
    System.out.println( array[position++] );
}
```

The `capacity` of a buffer is similar to the length of an array; but as we can see from the above example, the `limit` of a buffer may not be equal to its capacity if we've only written a limited number of bytes.

For convenience, you can "chain" calls with get/put/etc. like so:
```java
buffer.put(a).put(b).put(c).put(d);
```

### Practical Usage

So how does this relate to LWJGL and OpenGL? There are two common ways you'll be using buffers: writing data to GL (i.e. uploading texture data to the GPU), or reading data from GL (i.e. reading texture data from the GPU, or getting a certain value from the driver).

Let's say we are creating a 1x1 blue RGBA texture, our buffer setup would look like this:

```java
int width = 1; //1 pixel wide
int height = 1; //1 pixel high
int bpp = 4; //4 bytes per pixel (RGBA)

//create our buffer
ByteBuffer buffer = BufferUtils.createByteBuffer(width * height * bpp);

//put the Red, Green, Blue, and Alpha bytes
buffer.put((byte)0x00).put((byte)0x00).put((byte)0xFF).put((byte)0xFF);

//flip the buffer !!! this needs to be done before it can be read by GL
buffer.flip();

//here is an example of sending data to GL... we will talk 
//more about this method in the Texture section
glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, 
             width, height, 0, GL_RGBA, 
             GL_UNSIGNED_BYTE, buffer);
```

Below is an example of getting data from GL:

```java
IntBuffer buffer = BufferUtils.createIntBuffer(1);

//this will call the relative "put" on our buffer
glGetInteger(GL_MAX_TEXURE_SIZE, buffer);

//before we read back the values, we need to "flip" it
buffer.flip();

//now we can get the max size as a Java int
int maxSize = buffer.get();
```

As described [in the docs](http://www.khronos.org/opengles/documentation/opengles1_0/html/glGetInteger.html), `GL_MAX_TEXTURE_SIZE` will give us one value. Some other GL parameters may return more values, and in that case we would have to create our buffer with a large enough capacity. Where possible, you should try to re-use buffers instead of always creating new ones.

Also note that LWJGL includes convenience methods for glGetInteger, glGenTextures, and various other calls. So the above code would actually be reduced to the following:

```java
int maxSize = glGetInteger(GL_MAX_TEXTURE_SIZE);
```