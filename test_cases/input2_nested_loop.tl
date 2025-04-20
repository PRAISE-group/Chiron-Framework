:x = 4
:y = 5
if :x < :y [
  :x = :x + 3
]
else [
    :x = :x + 2
]

repeat 2 [
    repeat 4 [
	    :y = :y + 3
    ]
]
