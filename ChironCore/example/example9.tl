:x = 0
:a = 1
:b = 1
if (:a==1) [
  :x = 1
] 
if (:b==1) [
  :x = 2
] else [
  :x = 3
  :a = 0
]
forward :x