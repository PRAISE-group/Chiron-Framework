:mod4 = (:year-1) - ((:year-1)/4)*4
:mod100 = (:year-1) - ((:year-1)/100)*100
:mod400 = (:year-1) - ((:year-1)/400)*400
:isLeap1 = (:mod4+1)/4 - (:mod100+1)/100 + (:mod400+1)/400

:mod4n = :year - (:year/4)*4
:mod100n = :year - (:year/100)*100
:mod400n = :year - (:year/400)*400

if (:mod4n == 0) [
    :isDivby4 = 1
] else [
    :isDivby4 = 0
]
if (:mod100n == 0) [
    :isDivby100 = 1
] else [
    :isDivby100 = 0
]
if (:mod400n == 0)[
    :isDivby400 = 1
] else [
    :isDivby400 = 0
]
if ((:isDivby4 == 1 && :isDivby100 != 1) || (:isDivby400 == 1)) [
    :isLeap2 = 1
] else [
    :isLeap2 = 0
]