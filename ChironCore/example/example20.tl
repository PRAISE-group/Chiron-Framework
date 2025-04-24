:global1 = 10
repeat 2 [
  :global1 = 20 
  if (:global1 > 15) [
    :local = :global1
    :global1 = :local + 5  
  ]
]
forward :global1