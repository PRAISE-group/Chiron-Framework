:x = 20 
:y = 100
:z = 60
repeat 6 [
if (:x != :y) [
if ( :x > :y) [ right :x ]
else [ left :y ]
] else [
if((:x <= :z) || (:y <= :z))[
:x = :z / :x
:z = :y / :z
 ]]
 forward :x right :y
 forward :z left :z
 ]
 goto (:x, :y)