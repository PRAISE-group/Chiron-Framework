 :x = 20
 :y = 10
 :a = 10
 :b = 3
 forward :x + :a
 if (:y > :x) [
  :x = 30
  :y = 0
   left :y
 ] else [
  :x = 25
   right 50
 ]
 forward :x+:a+:b
 forward :y