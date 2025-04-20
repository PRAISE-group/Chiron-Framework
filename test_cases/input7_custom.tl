:counter = 10
:step = 2
:threshold = 5

repeat 3 [  
    :counter = :counter - :step
    if :counter > :threshold [  
        :step = :step + 1  
    ]
]

if :counter < :threshold [  
    :counter = :counter + 5  
]

:result = :counter * 2 + 3
