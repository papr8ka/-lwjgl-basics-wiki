Complex polygons, strokes, dotted outlines, and various other raster effects are difficult to achieve in OpenGL. Solutions such as `GL_LINES` may lead to different visual results across platforms, while other options have been deprecated altogether (e.g. `glLineStipple`). 

If you are only targeting desktop, you may decide to use Java2D for rasterization. It's a powerful, flexible and easy to use API that leads to implementation-independent rendering. In order to use Java2D's rasterizer in LibGDX, we need to render it to a Java2D BufferedImage, then copy the pixels to a texture on the GPU.

![Img](images/xTl6Y.png)

For better performance you would minimize the number of times you upload data to GL; e.g. accumulating the data into the same glTexSubImage2D call. Also, you could modify the below code to upload to a texture atlas, rather than having a single large texture per shape.

This is not an ideal solution for dynamic shapes that need to change frequently, but for static shapes it may lead to crisper graphics than `GL_LINES` or meshes.

## Full Java Source

```java
import java.awt.BasicStroke;
import java.awt.Color;
import java.awt.Graphics2D;
import java.awt.Rectangle;
import java.awt.RenderingHints;
import java.awt.geom.GeneralPath;
import java.awt.image.BufferedImage;
import java.awt.image.DataBufferInt;
import java.nio.IntBuffer;
import java.util.ArrayList;
import java.util.List;

import org.lwjgl.opengl.GL12;

import com.badlogic.gdx.Application.ApplicationType;
import com.badlogic.gdx.ApplicationListener;
import com.badlogic.gdx.Gdx;
import com.badlogic.gdx.backends.lwjgl.LwjglApplication;
import com.badlogic.gdx.backends.lwjgl.LwjglApplicationConfiguration;
import com.badlogic.gdx.graphics.GL10;
import com.badlogic.gdx.graphics.GL11;
import com.badlogic.gdx.graphics.OrthographicCamera;
import com.badlogic.gdx.graphics.Pixmap.Format;
import com.badlogic.gdx.graphics.Texture;
import com.badlogic.gdx.graphics.g2d.SpriteBatch;
import com.badlogic.gdx.graphics.g2d.TextureRegion;
import com.badlogic.gdx.utils.BufferUtils;
import com.badlogic.gdx.utils.GdxRuntimeException;

public class Java2DTest implements ApplicationListener {
   
   public static void main(String[] args) {
      LwjglApplicationConfiguration cfg = new LwjglApplicationConfiguration();
      cfg.title = "Java2DTest";
      cfg.useGL20 = false;
      cfg.width = 480;
      cfg.height = 320;
      
      new LwjglApplication(new Java2DTest(), cfg);
   }
   
   private OrthographicCamera camera;
   private SpriteBatch batch;
   private Java2DTexture j2dTex;
   private TextureRegion sprite;
   

   private List<java.awt.Shape> shapes = new ArrayList<java.awt.Shape>();
   private int pointer = 0;
   
   @Override
   public void create() {
      if (Gdx.app.getType()!=ApplicationType.Desktop)
         throw new GdxRuntimeException("this demo only works on desktop with Java2D");
      
      float w = Gdx.graphics.getWidth();
      float h = Gdx.graphics.getHeight();
      
      camera = new OrthographicCamera(w, h);
      camera.setToOrtho(false);
      batch = new SpriteBatch();
      
      // 1. -- create our Java2D buffer; must be big enough to hold our shape!
      j2dTex = new Java2DTexture(1024, 1024);
      
      // 2. -- setup our texture region for drawing part of our buffer
      sprite = new TextureRegion(j2dTex);
      
      // 3. --- Setup a few shapes for example
      GeneralPath path = new GeneralPath();
      path.moveTo(50, 120);
      path.lineTo(70, 180);
      path.lineTo(20, 140);
      path.lineTo(80, 140);
      path.lineTo(30, 180);
      path.closePath();
      shapes.add(path);

      path = new GeneralPath();
      path.moveTo(120, 180);
      path.quadTo(150, 120, 180, 180);
      path.closePath();
      shapes.add(path);

      path = new GeneralPath();
      path.moveTo(220, 150);
      path.curveTo(240, 130, 280, 160, 300, 140);
      path.lineTo(300, 180);
      path.quadTo(260, 160, 220, 180);
      path.closePath();
      shapes.add(path);

      path = new GeneralPath();
      path.moveTo(360, 100);
      path.lineTo(360, 200);
      path.lineTo(400, 140);
      path.lineTo(320, 120);
      path.lineTo(400, 180);
      path.lineTo(320, 180);
      path.closePath();
      shapes.add(path);
      
      // 4. show a shape..
      show(shapes.get(pointer));
   }

   void show(java.awt.Shape shape) {
      Graphics2D g2d = j2dTex.begin();
      
      //do whatever want here, e.g. solid fill, strokes, gradient fill
      g2d.setColor(Color.lightGray);
      g2d.fill(shape);
      
      //draw a dashed stroke...
      g2d.setColor(Color.red);
      g2d.setStroke(new BasicStroke(2, BasicStroke.CAP_ROUND,
                              BasicStroke.JOIN_ROUND,
                              10, new float[] { 4, 4 }, 0));
      g2d.draw(shape);
      
      //upload data to GL
      j2dTex.end();
      
      //don't forget to set our texture region up..
      //we use + 1 since Java2D draws outlines on the OUTSIDE
      Rectangle bounds = shape.getBounds();
      sprite.setRegion(bounds.x, bounds.y, bounds.width+1, bounds.height+1);
   }
   
   @Override
   public void dispose() {
      batch.dispose();
      j2dTex.dispose();
   }
   
   
   @Override
   public void render() {      
      Gdx.gl.glClearColor(0, 0, 0, 0);
      Gdx.gl.glClear(GL10.GL_COLOR_BUFFER_BIT);
      
      //show next shape
      if (Gdx.input.isTouched()) {
         pointer++;
         if (pointer>=shapes.size())
            pointer = 0;
         show(shapes.get(pointer));
      }
      
      batch.setProjectionMatrix(camera.combined);
      batch.begin();
      batch.draw(sprite, 10, 10);
      batch.end();
   }

   @Override
   public void resize(int width, int height) {
      camera.setToOrtho(false, width, height);
   }

   @Override
   public void pause() {
   }

   @Override
   public void resume() {
   }
   

   
   public static class Java2DTexture extends Texture {
      
      protected BufferedImage bufferImg;
      protected IntBuffer buffer;
      private final Color BACKGROUND = new Color(0, 0, 0, 0);
      
      public Java2DTexture(int width, int height, Format format) {
         super(width, height, format);
         bufferImg = new BufferedImage(width, height, BufferedImage.TYPE_INT_ARGB);
         buffer = BufferUtils.newIntBuffer(width * height);
      }
      
      public Java2DTexture(int width, int height) {
         this(width, height, Format.RGBA8888);
      }
      
      public Java2DTexture() {
         this(1024, 1024);
      }

      public BufferedImage getBufferedImage() {
         return bufferImg;
      }
      
      public Graphics2D begin() {
         //you could probably cache this instead of requesting it every time
         Graphics2D g2d = (Graphics2D) bufferImg.getGraphics();
         g2d.setRenderingHint(RenderingHints.KEY_ANTIALIASING,
               RenderingHints.VALUE_ANTIALIAS_ON);
         g2d.setBackground(BACKGROUND);
         g2d.clearRect(0, 0, bufferImg.getWidth(), bufferImg.getHeight());
         g2d.setColor(java.awt.Color.white);
         return g2d;
      }
      
      public void end() {
         // now we pass the BufferedImage pixel data to the LibGDX texture...
         int width = bufferImg.getWidth();
         int height = bufferImg.getHeight();
         //you could probably cache this rather than requesting it every upload
         int[] pixels = ((DataBufferInt)bufferImg.getRaster().getDataBuffer())
               .getData();
         this.bind();
         buffer.rewind();
         buffer.put(pixels);
         buffer.flip();
         Gdx.gl.glTexSubImage2D(GL11.GL_TEXTURE_2D, 0, 0, 0, width, height,
               GL12.GL_BGRA, GL12.GL_UNSIGNED_INT_8_8_8_8_REV, buffer);
      }
      
   }
}
```