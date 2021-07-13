3 timesRepeat: [ Transcript show: 'Hello' ; cr ].

Date today + 12 days.

Point linesOfCode.

Smalltalk allClasses size.

Smalltalk allClasses; inject: 0 into: [ :sum :each | sum + each linesOfCode ].

VGTigerDemo runDemo.

SystemNavigation new; browseAllSelect:
       [:m| m primitive isZero; and: [m pragmas notEmpty]].