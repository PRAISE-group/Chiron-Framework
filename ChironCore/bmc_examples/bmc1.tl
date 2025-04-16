// inputs: :x, :y, :z

:t = :x + 2*:y + 3*:z + :x * :w * :u
:z = :x + :w


assert (:x + 100 < :y) && (:x + 200 > :y) && !(:x >= 0) && (:x * :y < -:x) && (:t > 0)
