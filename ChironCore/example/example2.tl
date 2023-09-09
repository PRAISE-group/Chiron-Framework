penup
goto (50, 50)
pendown
:two = 200
:one = 100
forward 50
right 90
forward 50
right 90
forward 50
right 90
forward 50
penup

:vara = 20
:varb = 100
:varc = 60
repeat 1 [
	goto (0, 0)
	pendown
	repeat 6 [
		if (:vara != :varb) [
			if ( :vara > :varb) [ right :vara ]
			else [ left :varb ]
		]
		else [
		 if ((:vara <= :varc) || (:varb <= :varc)) [
			:vara = :varc / :vara
			:varb = :varb / :varc
			:varc = :varb
		 ]
		]
		forward :vara
		right :varb
		forward :varc
		left :varc
	]
	left 45
]
penup