You can use the `#version` command as the first line of your shader to specify GLSL version:

```glsl
#version 120

void main() {
    gl_FragColor = vec4(1.0);
}
```

GLSL versions are released alongside GL versions. See the following charts to decide which version you would like to target.

### GLSL Versions

<table>
    <tr>
        <td><b>OpenGL Version</b></td>
        <td><b>GLSL Version</b></td>
    </tr>
    <tr>
        <td>2.0</td>
        <td>110</td>
    </tr>
    <tr>
        <td>2.1</td>
        <td>120</td>
    </tr>
    <tr>
        <td>3.0</td>
        <td>130</td>
    </tr>
    <tr>
        <td>3.1</td>
        <td>140</td>
    </tr>
    <tr>
        <td>3.2</td>
        <td>150</td>
    </tr>
    <tr>
        <td>3.3</td>
        <td>330</td>
    </tr>
    <tr>
        <td>4.0</td>
        <td>400</td>
    </tr>
    <tr>
        <td>4.1</td>
        <td>410</td>
    </tr>
    <tr>
        <td>4.2</td>
        <td>420</td>
    </tr>
    <tr>
        <td>4.3</td>
        <td>430</td>
    </tr>
</table>

### GLSL ES Versions (Android, iOS, WebGL)

OpenGL ES has its own Shading Language, and the versioning starts fresh. It is based on OpenGL Shading Language version 1.10.

<table>
    <tr>
        <td><b>OpenGL ES Version</b></td>
        <td><b>GLSL ES Version</b></td>
    </tr>
    <tr>
        <td>2.0</td>
        <td>100</td>
    </tr>
    <tr>
        <td>3.0</td>
        <td>300</td>
    </tr>
</table>

So, for example, if a feature is available in GLSL 120, it probably won't be available in GLSL ES 100 unless the ES compiler specifically allows it.

## Arrays

Arrays are declared like so:
```glsl
float a[5];
```

#GLSL 120

Some major additions to GLSL 120. Note that most of these will not work on GLSL ES.

- You can initialize arrays within a shader, like so:
```glsl
float a[5] = float[5](3.4, 4.2, 5.0, 5.2, 1.1);
float b[5] = float[](3.4, 4.2, 5.0, 5.2, 1.1);
```
However, the above is not supported on Mac OSX Snow Leopard, even with GLSL 120. [(1)](http://openradar.appspot.com/6121615) 
- You can initialize uniforms in a shader, and the value will be set at link time:
```glsl
uniform float val = 1.0;
```
- You can use built-ins like `sin()` when setting a `const` value
- Integers are implicitly converted to floats when necessary, for example:
```glsl
float f = 1.0; <-- valid
float g = 1; <-- only supported in GLSL 120
vec2 v = vec2(1, 2.0); <-- only supported in GLSL 120
```
- You can use `f` to define a float: `float f = 2.5f;`