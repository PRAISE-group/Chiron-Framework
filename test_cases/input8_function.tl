valuefunc sum(:a,:b){
    valuereturn :a +:b
}
voidfunc funcForGoto(:x,:y,:valueToAdd){
       goto(get sum(:x, :valueToAdd), get sum(:y, :valueToAdd))
       voidreturn
}
:x = 0
:y = 0
:valueToAdd = 50

pendown

procedure funcForGoto(:x,:y,:valueToAdd)

penup