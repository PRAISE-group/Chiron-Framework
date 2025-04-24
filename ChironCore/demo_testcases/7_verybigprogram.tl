:basesize = 150
:sides = 6
:factor = 8/10
:angle = 60
:depth = 3
:maxdepth = 4
:shift = 30
:counter = 0
:maxcounter = 20
:direction = 1
:spiralsize = 5
:spiralangle = 15
:spiralgrowth = 108/100
:branchfactor = 7/10
:rotationstep = 72
:flowerpoints = 8
:flowersize = 120
:stars = 2
:starsize = 100
:starpoints = 7
:starangle = 144
:polygons = 4
:polygonsize = 80
:spiraliterations = 40
:spiralmultiple = 3
:floweriteration = 1
:specialeffect = 1
:shapefactor = 2/3

pendown

repeat 5 [
  :currentsize = :basesize
  :currentsides = :sides
  :currentdepth = 0
  
  repeat :currentsides [
    forward :currentsize
    right (360 / :currentsides)
    
    if (:currentdepth < :maxdepth) [
      :currentdepth = :currentdepth + 1
      :branchsize = :currentsize * :branchfactor
      :branchsides = :currentsides - 1
      
      if (:branchsides < 3) [
        :branchsides = 3
      ]
      
      repeat :branchsides [
        forward :branchsize
        right (360 / :branchsides)
        repeat 1[
            forward 1
        ]
      ]
      
      :currentdepth = :currentdepth - 1
    ]
  ]
  
  if (:specialeffect > 0) [
    :spiralrad = :spiralsize
    
    repeat 20 [
      forward :spiralrad
      right :spiralangle
      :spiralrad = :spiralrad * :spiralgrowth
    ]
    
    :specialeffect = 0
  ] else [
    :specialeffect = 1
  ]
  
  :counter = :counter + 1
  
  if (:counter >= :maxcounter) [
    :counter = 0
    :direction = :direction * -1
  ]
  
  :basesize = :basesize * :factor
  :sides = :sides + :direction
  
  if (:sides > 8) [
    :sides = 3
  ]
  
  if (:sides < 3) [
    :sides = 8
  ]
  
  penup
  goto (0, 0)
  pendown
  right :rotationstep
]

if (:floweriteration > 0) [
  repeat :flowerpoints [
    forward :flowersize
    backward :flowersize
    right (360 / :flowerpoints)
  ]
]

:currentstars = :stars

repeat :stars [
  :currentstarsize = :starsize
  
  repeat :starpoints [
    forward :currentstarsize
    right :starangle
  ]
  
  :starsize = :starsize * :shapefactor
]

:currentspiral = :spiralmultiple
:spiralrad = :spiralsize
:spiralstep = :spiralangle

repeat :spiraliterations [
  forward :spiralrad
  right :spiralstep
  :spiralrad = :spiralrad * :spiralgrowth
  
  if (:spiralrad > 200) [
    :currentspiral = :currentspiral - 1
    
    if (:currentspiral > 0) [
      penup
      goto (0, 0)
      pendown
      right 90
      :spiralrad = :spiralsize
    ] else [
      :spiralgrowth = 100/100
    ]
  ]
]

:currentpolygons = :polygons
:currentpolygonsize = :polygonsize
:polygonsides = 3

repeat :polygons [
  repeat :polygonsides [
    forward :currentpolygonsize
    right (360 / :polygonsides)
  ]
  
  :currentpolygonsize = :currentpolygonsize * :shapefactor
  :polygonsides = :polygonsides + 1
]

penup