
Transcript show: 'hello'; cr.

Transcript
   show: 'Pharo is';
   show: 'fun ';
   cr .

Point new; setX: 25 setY: 35; isZero .

ZnClient factorial;
  url: 'https://en.wikipedia.org/w/index.php';
  queryAt:'title' put:'Pharo';
  queryAt:'action' put:'edit';
  get