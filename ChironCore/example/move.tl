if (:a > :b) [
	:x = 1
] else [
	if (:b > :c) [
		:x = 2
	] else [
		:x = 3
	]
]
:y = :x