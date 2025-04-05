:p=1
assume 5 <= 7
:t=:t*:x

:t=:t*:x

:t=:t*:x

:t=:t*:x

:t=:t*:x


:q=1
assume 4 <= 7
:q=:q*:x

:q=:q*:x

:q=:q*:x

:q=:q*:x


:r=1
assume 7 <= 7
:r=:r*:x

:r=:r*:x

:r=:r*:x

:r=:r*:x

:r=:r*:x

:r=:r*:x

:r=:r*:x


:s=1
:_repeat0 = :o
assume :_repeat0 <= 7 
if (:_repeat0 > 0) [
:s=:s*:x
:o=:o-1

]
if (:_repeat0 > 1) [
:s=:s*:x
:o=:o-1

]
if (:_repeat0 > 2) [
:s=:s*:x
:o=:o-1

]
if (:_repeat0 > 3) [
:s=:s*:x
:o=:o-1

]
if (:_repeat0 > 4) [
:s=:s*:x
:o=:o-1

]
if (:_repeat0 > 5) [
:s=:s*:x
:o=:o-1

]
if (:_repeat0 > 6) [
:s=:s*:x
:o=:o-1

]

:z=2*:p-3*:q+5*:r-7*:s
assert:z>-10000
