# Software for Smalltalk source code analysis


About
====

The project consists of three parts: 
- Smalltalk parser
- Language server
- Client

The main task was to find all references to a particular message in Pharo programming language. The service is integrated into the Visual Code editor.

Communication between Language Server and Client follows [Language Server Protocol](https://github.com/Microsoft/language-server-protocol/blob/main/versions/protocol-1-x.md). 

The Pharo grammar and parser are written using [textX](http://textx.github.io/textX/3.0/) python library. Check parse tree visualizations inside the parser/images folder.

Architecture components
====
![alt text](https://github.com/specnazm/smalltalk-parser/blob/main/components.png?raw=true)

