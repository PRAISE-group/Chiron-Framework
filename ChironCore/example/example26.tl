
:base = 100
:offset = 20
:depth = 3
:step = 0
:dir = 1
:shape = 1
:accel = 2
:decay = 1
:counter = 0
:limit = 7
:alternate = 0
:geofactor = 3/2

pendown
repeat 4 [  
  
  if (:shape * :dir > :limit) [
    :shape = 1
    :dir = :dir * -1
    :alternate = :alternate + 1
  ] else [
    :shape = :shape + :accel
    :accel = :accel + :decay
  ]

 
  if (:alternate < 3) [
    repeat :shape [
      forward :base
      right (360 / :shape)
      :step = :step + 1
      
      
      repeat 2 [
        if (:step > 5) [
          penup
          goto (:base * :geofactor, :base / :geofactor)
          pendown
          :geofactor = :geofactor + (2/10)
          
        
          repeat 3 [
            left 120
            forward (:base - :offset)
            :offset = :offset + 5
            if (:offset > 40) [
              :offset = 20
              right 60
              forward (:base / 2)
            ]
          ]
        ] else [
          backward (:base / 2)
          left 45
          :counter = :counter + 1
        ]
      ]
    ]
  ] else [
    
    :spiralsteps = 10
    :spiralangle = 15
    :spiralgrowth = (6/5)
    
    repeat 3 [
      forward :spiralsteps
      right :spiralangle
      :spirasteps = :spirasteps * :spiralgrowth
      :spiraangle = :spiraangle + 2
      
    
      if (:spirasteps > 50) [
        penup
        goto (:spirasteps, :spiraangle)
        pendown
        repeat 2 [
          left 90
          forward (:spiralsteps / 2)
          :spiralgrowth = :spiralgrowth - (1/10)
        ]
      ]
    ]
  ]

  
  :temp = :base
  :base = :base + (:counter * 2)
  :counter = :temp - (:offset / 2)
  :limit = :limit + (:shape * :dir)
  

  if (:base > 200) [
    :base = 50
    :dir = :dir * -1
    repeat 2 [
      right 180
      forward 30
      :geofactor = :geofactor - (1/2)
    ]
  ] else [
    left 45
    forward (:base * (7/10))
  ]
  
 
  penup
  goto (0, 0)
  pendown
  :depth = :depth - 1
]
penup