You can use the `#version` command as the first line of your shader to specify GLSL version:

```glsl
#version 120

void main() {
    gl_FragColor = vec4(1.0);
}
```

## GLSL Versions

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

## GLSL ES Versions

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