// inputs: :x, :y, :z

:t = :x + 2*:y 


assert (:x + 100 < :y) && (:x + 200 > :y) && !(:x >= 0) && (:x * :y < -:x) && (:t > 0)