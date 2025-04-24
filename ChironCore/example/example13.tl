:y = 10
:x = 2
 if (:y < 2) [
  :x = 30
  :y = 0
   left :y
   left :x
 ] else [
    :x = 3
    left :x
   right 50
 ]
 forward :y