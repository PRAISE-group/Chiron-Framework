pendown
assume 3 <= 10
if ((:x>:y)) [
penup
goto (:x, :y)
pendown
assume 4 <= 10
forward:x
left90

forward:x
left90

forward:x
left90

forward:x
left90



] else [
penup
goto (:y, :x)
pendown
assume 5 <= 10
forward:p
left72

forward:p
left72

forward:p
left72

forward:p
left72

forward:p
left72



]
if ((:z>=:p)) [
penup
goto (:p, :x+:z)
pendown
assume 6 <= 10
backward:x
left60

backward:x
left60

backward:x
left60

backward:x
left60

backward:x
left60

backward:x
left60



]
:x=:x+10
:y=:y+10
:z=:z+10

if ((:x>:y)) [
penup
goto (:x, :y)
pendown
assume 4 <= 10
forward:x
left90

forward:x
left90

forward:x
left90

forward:x
left90



] else [
penup
goto (:y, :x)
pendown
assume 5 <= 10
forward:p
left72

forward:p
left72

forward:p
left72

forward:p
left72

forward:p
left72



]
if ((:z>=:p)) [
penup
goto (:p, :x+:z)
pendown
assume 6 <= 10
backward:x
left60

backward:x
left60

backward:x
left60

backward:x
left60

backward:x
left60

backward:x
left60



]
:x=:x+10
:y=:y+10
:z=:z+10

if ((:x>:y)) [
penup
goto (:x, :y)
pendown
assume 4 <= 10
forward:x
left90

forward:x
left90

forward:x
left90

forward:x
left90



] else [
penup
goto (:y, :x)
pendown
assume 5 <= 10
forward:p
left72

forward:p
left72

forward:p
left72

forward:p
left72

forward:p
left72



]
if ((:z>=:p)) [
penup
goto (:p, :x+:z)
pendown
assume 6 <= 10
backward:x
left60

backward:x
left60

backward:x
left60

backward:x
left60

backward:x
left60

backward:x
left60



]
:x=:x+10
:y=:y+10
:z=:z+10


penup

assert (:turtleX > 0)