You can use the `#version` command as the first line of your shader to specify GLSL version:

```glsl
#version 120

void main() {
    gl_FragColor = vec4(1.0);
}
```

## Versions

<table>
    <tr>
        <td>**OpenGL Version**</td>
        <td>**GLSL Version**</td>
    </tr>
    <tr>
        <td>2.0</td>
        <td>`#version 110`</td>
    </tr>
    <tr>
        <td>2.1</td>
        <td>`#version 120`</td>
    </tr>
    <tr>
        <td>3.0</td>
        <td>`#version 130`</td>
    </tr>
    <tr>
        <td>3.1</td>
        <td>`#version 140`</td>
    </tr>
    <tr>
        <td>3.2</td>
        <td>`#version 150`</td>
    </tr>
</table>