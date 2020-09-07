xof 0302txt 0064
template Header {
 <3D82AB43-62DA-11cf-AB39-0020AF71E433>
 WORD major;
 WORD minor;
 DWORD flags;
}

template Vector {
 <3D82AB5E-62DA-11cf-AB39-0020AF71E433>
 FLOAT x;
 FLOAT y;
 FLOAT z;
}

template Coords2d {
 <F6F23F44-7686-11cf-8F52-0040333594A3>
 FLOAT u;
 FLOAT v;
}

template Matrix4x4 {
 <F6F23F45-7686-11cf-8F52-0040333594A3>
 array FLOAT matrix[16];
}

template ColorRGBA {
 <35FF44E0-6C7C-11cf-8F52-0040333594A3>
 FLOAT red;
 FLOAT green;
 FLOAT blue;
 FLOAT alpha;
}

template ColorRGB {
 <D3E16E81-7835-11cf-8F52-0040333594A3>
 FLOAT red;
 FLOAT green;
 FLOAT blue;
}

template IndexedColor {
 <1630B820-7842-11cf-8F52-0040333594A3>
 DWORD index;
 ColorRGBA indexColor;
}

template Boolean {
 <4885AE61-78E8-11cf-8F52-0040333594A3>
 WORD truefalse;
}

template Boolean2d {
 <4885AE63-78E8-11cf-8F52-0040333594A3>
 Boolean u;
 Boolean v;
}

template MaterialWrap {
 <4885AE60-78E8-11cf-8F52-0040333594A3>
 Boolean u;
 Boolean v;
}

template TextureFilename {
 <A42790E1-7810-11cf-8F52-0040333594A3>
 STRING filename;
}

template Material {
 <3D82AB4D-62DA-11cf-AB39-0020AF71E433>
 ColorRGBA faceColor;
 FLOAT power;
 ColorRGB specularColor;
 ColorRGB emissiveColor;
 [...]
}

template MeshFace {
 <3D82AB5F-62DA-11cf-AB39-0020AF71E433>
 DWORD nFaceVertexIndices;
 array DWORD faceVertexIndices[nFaceVertexIndices];
}

template MeshFaceWraps {
 <4885AE62-78E8-11cf-8F52-0040333594A3>
 DWORD nFaceWrapValues;
 Boolean2d faceWrapValues;
}

template MeshTextureCoords {
 <F6F23F40-7686-11cf-8F52-0040333594A3>
 DWORD nTextureCoords;
 array Coords2d textureCoords[nTextureCoords];
}

template MeshMaterialList {
 <F6F23F42-7686-11cf-8F52-0040333594A3>
 DWORD nMaterials;
 DWORD nFaceIndexes;
 array DWORD faceIndexes[nFaceIndexes];
 [Material]
}

template MeshNormals {
 <F6F23F43-7686-11cf-8F52-0040333594A3>
 DWORD nNormals;
 array Vector normals[nNormals];
 DWORD nFaceNormals;
 array MeshFace faceNormals[nFaceNormals];
}

template MeshVertexColors {
 <1630B821-7842-11cf-8F52-0040333594A3>
 DWORD nVertexColors;
 array IndexedColor vertexColors[nVertexColors];
}

template Mesh {
 <3D82AB44-62DA-11cf-AB39-0020AF71E433>
 DWORD nVertices;
 array Vector vertices[nVertices];
 DWORD nFaces;
 array MeshFace faces[nFaces];
 [...]
}

Material Material1 {
0.000000;0.000000;0.500000;1.000000;;
20.000000;
1.000000;1.000000;1.000000;;
0.000000;0.000000;0.000000;;
}
Material Material2 {
0.000000;0.000000;1.000000;1.000000;;
20.000000;
1.000000;1.000000;1.000000;;
0.000000;0.000000;0.000000;;
}
Material BlackMaterial {
0.000000;0.000000;0.000000;1.000000;;
0.000000;
0.000000;0.000000;0.000000;;
0.000000;0.000000;0.000000;;
}
Material WhiteMaterial {
1.000000;1.000000;1.000000;1.000000;;
0.000000;
0.000000;0.000000;0.000000;;
0.000000;0.000000;0.000000;;
}

Header {
 1;
 0;
 1;
}

Mesh cobrafs {
68;
 32.0; 0.0; 76.0;,
 -32.0; 0.0; 76.0;,
 0.0; 26.0; 24.0;,
 -120.0; -3.04; -8.0;,
 120.0; -3.04; -8.0;,
 -88.0; 16.0; -40.0;,
 88.0; 16.0; -40.0;,
 128.0; -8.0; -40.0;,
 -128.0; -8.0; -40.0;,
 0.0; 26.0; -40.0;,
 -32.0; -24.0; -40.0;,
 32.0; -24.0; -40.0;,
 -36.0; 8.0; -40.08;,
 -8.0; 12.0; -40.08;,
 8.0; 12.0; -40.08;,
 36.0; 8.0; -40.08;,
 36.0; -12.0; -40.08;,
 8.0; -16.0; -40.08;,
 -8.0; -16.0; -40.08;,
 -36.0; -12.0; -40.08;,
 -1.6; -1.6; 76.0;,
 -1.6; -1.6; 90.0;,
 -80.0; -6.0; -40.08;,
 -80.0; 6.0; -40.08;,
 -88.0; 0.0; -40.08;,
 80.0; 6.0; -40.08;,
 88.0; 0.0; -40.08;,
 80.0; -6.0; -40.08;,
 1.6; -1.6; 76.0;,
 1.6; -1.6; 90.0;,
 1.6; 1.6; 76.0;,
 1.6; 1.6; 90.0;,
 -1.6; 1.6; 76.0;,
 -1.6; 1.6; 90.0;,
 32.0; 0.0; 76.0;,
 -32.0; 0.0; 76.0;,
 0.0; 26.0; 24.0;,
 32.0; 0.0; 76.0;,
 32.0; -24.0; -40.0;,
 128.0; -8.0; -40.0;,
 120.0; -3.04; -8.0;,
 -32.0; 0.0; 76.0;,
 -120.0; -3.04; -8.0;,
 -128.0; -8.0; -40.0;,
 -32.0; -24.0; -40.0;,
 32.0; 0.0; 76.0;,
 -32.0; 0.0; 76.0;,
 -32.0; -24.0; -40.0;,
 32.0; -24.0; -40.0;,
 -88.0; 16.0; -40.0;,
 0.0; 26.0; 24.0;,
 0.0; 26.0; -40.0;,
 0.0; 26.0; 24.0;,
 88.0; 16.0; -40.0;,
 0.0; 26.0; -40.0;,
 88.0; 16.0; -40.0;,
 0.0; 26.0; 24.0;,
 32.0; 0.0; 76.0;,
 120.0; -3.04; -8.0;,
 88.0; 16.0; -40.0;,
 -32.0; 0.0; 76.0;,
 -88.0; 16.0; -40.0;,
 -88.0; 16.0; -40.0;,
 -120.0; -3.04; -8.0;,
 -88.0; 16.0; -40.0;,
 -128.0; -8.0; -40.0;,
 128.0; -8.0; -40.0;,
 88.0; 16.0; -40.0;;

 22;
 3;36,35,34;,
 4;45,46,47,48;,
 3;55,56,57;,
 3;0,58,59;,
 4;37,38,39,40;,
 3;60,2,61;,
 3;62,63,1;,
 4;41,42,43,44;,
 3;49,50,51;,
 3;52,53,54;,
 3;64,65,3;,
 3;66,67,4;,
 7;9,6,7,11,10,8,5;,
 4;14,15,16,17;,
 4;12,13,18,19;,
 3;25,26,27;,
 3;24,23,22;,
 4;21,29,28,20;,
 4;31,29,28,30;,
 4;32,30,31,33;,
 4;21,33,32,20;,
 4;20,33,31,29;;

MeshMaterialList {
 4; 
 22;
 1, 
 1, 
 0,
 0,
 0,
 0,
 0,
 0,
 1,
 1,
 1,
 1,
 0,
 2,
 2,
 2,
 2,
 3,
 3,
 3,
 3,
 3;;
{Material1} 
{Material2}
{BlackMaterial}
{WhiteMaterial}
}
}
