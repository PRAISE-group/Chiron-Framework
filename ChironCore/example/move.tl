:x = 10
:x = :x + 2
if (:x > 2) [
	:x = 4
] else [
	:x = 3
]
:y = :x + 2
:x = :x + 1
:x = :x + 5

repeat :x [
if (:y > 0) [
:x = :x + :y + :z
]
if (:y < 0) [
:x = :w + :lam
]
]
