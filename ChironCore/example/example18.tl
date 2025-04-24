:x = 1
:y = :x + 2  
repeat :y [    
  :x = :x * 2  
  :y = :y - 1  
  forward :x
]