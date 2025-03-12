penup
goto (50,50)
pendown
:angle = 45
if (:angle < 90) [
   right :angle
   forward 100
] else [
   left :angle
   backward 50
]
penup