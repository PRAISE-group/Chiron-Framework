Chiron v5.3

    ░█████╗░██╗░░██╗██╗██████╗░░█████╗░███╗░░██╗
    ██╔══██╗██║░░██║██║██╔══██╗██╔══██╗████╗░██║
    ██║░░╚═╝███████║██║██████╔╝██║░░██║██╔██╗██║
    ██║░░██╗██╔══██║██║██╔══██╗██║░░██║██║╚████║
    ╚█████╔╝██║░░██║██║██║░░██║╚█████╔╝██║░╚███║
    ░╚════╝░╚═╝░░╚═╝╚═╝╚═╝░░╚═╝░╚════╝░╚═╝░░╚══╝
    
assume(1==1)
if (:x > :y)[
    :t = :x
    :x = :y
    :y = :t
] 
if (:y > :z)[
    :t = :y
    :y = :z
    :z = :t
] 
if (:x > :y)[
    :t = :x
    :x = :y
    :y = :t
]
assert((:x <= :y) && (:y <= :z))
Pre-condition:  (= 1 1)
Post-condition:  (and (<= x_18_0 y_18_0) (<= y_18_0 z_18_0))
Code-body:  (and (= x_1_0 x_0_0)(= y_1_0 y_0_0)(= z_1_0 z_0_0)(= y_5_0 y_0_0)(= z_5_0 z_0_0)(= x_5_0 x_0_0)(or (and (> x_0_0 y_0_0) (and (= t_1_1 x_1_0) (= x_1_1 y_1_0) (= y_1_1 t_1_1) (= y_6_0 y_1_1) (= z_6_0 z_1_0) (= x_6_0 x_1_1) )
) (and (not (> x_0_0 y_0_0)) (and (= y_6_0 y_5_0) (= z_6_0 z_5_0) (= x_6_0 x_5_0) )
))(= y_7_0 y_6_0)(= z_7_0 z_6_0)(= x_7_0 x_6_0)(= x_11_0 x_6_0)(= y_11_0 y_6_0)(= z_11_0 z_6_0)(or (and (> y_6_0 z_6_0) (and (= t_7_1 y_7_0) (= y_7_1 z_7_0) (= z_7_1 t_7_1) (= x_12_0 x_7_0) (= y_12_0 y_7_1) (= z_12_0 z_7_1) )
) (and (not (> y_6_0 z_6_0)) (and (= x_12_0 x_11_0) (= y_12_0 y_11_0) (= z_12_0 z_11_0) )
))(= x_13_0 x_12_0)(= y_13_0 y_12_0)(= z_13_0 z_12_0)(= x_17_0 x_12_0)(= y_17_0 y_12_0)(= z_17_0 z_12_0)(or (and (> x_12_0 y_12_0) (and (= t_13_1 x_13_0) (= x_13_1 y_13_0) (= y_13_1 t_13_1) (= x_18_0 x_13_1) (= y_18_0 y_13_1) (= z_18_0 z_13_0) )
) (and (not (> x_12_0 y_12_0)) (and (= x_18_0 x_17_0) (= y_18_0 y_17_0) (= z_18_0 z_17_0) )
))true)

(declare-fun x_12_0 () Int)
(declare-fun x_7_0 () Int)
(declare-fun t_7_1 () Int)
(declare-fun z_1_0 () Int)
(declare-fun x_1_1 () Int)
(declare-fun z_7_0 () Int)
(declare-fun y_1_0 () Int)
(declare-fun x_11_0 () Int)
(declare-fun y_18_0 () Int)
(declare-fun z_13_0 () Int)
(declare-fun y_6_0 () Int)
(declare-fun x_13_1 () Int)
(declare-fun y_5_0 () Int)
(declare-fun x_6_0 () Int)
(declare-fun t_13_1 () Int)
(declare-fun z_7_1 () Int)
(declare-fun z_12_0 () Int)
(declare-fun t_1_1 () Int)
(declare-fun y_0_0 () Int)
(declare-fun z_17_0 () Int)
(declare-fun x_17_0 () Int)
(declare-fun x_0_0 () Int)
(declare-fun x_18_0 () Int)
(declare-fun y_13_1 () Int)
(declare-fun y_17_0 () Int)
(declare-fun y_13_0 () Int)
(declare-fun y_7_1 () Int)
(declare-fun y_11_0 () Int)
(declare-fun x_13_0 () Int)
(declare-fun x_5_0 () Int)
(declare-fun y_7_0 () Int)
(declare-fun z_0_0 () Int)
(declare-fun x_1_0 () Int)
(declare-fun z_11_0 () Int)
(declare-fun y_1_1 () Int)
(declare-fun y_12_0 () Int)
(declare-fun z_18_0 () Int)
(declare-fun z_5_0 () Int)
(declare-fun z_6_0 () Int)
(assert (not (=> (and (= 1 1) (and (= x_1_0 x_0_0)(= y_1_0 y_0_0)(= z_1_0 z_0_0)(= y_5_0 y_0_0)(= z_5_0 z_0_0)(= x_5_0 x_0_0)(or (and (> x_0_0 y_0_0) (and (= t_1_1 x_1_0) (= x_1_1 y_1_0) (= y_1_1 t_1_1) (= y_6_0 y_1_1) (= z_6_0 z_1_0) (= x_6_0 x_1_1) )
) (and (not (> x_0_0 y_0_0)) (and (= y_6_0 y_5_0) (= z_6_0 z_5_0) (= x_6_0 x_5_0) )
))(= y_7_0 y_6_0)(= z_7_0 z_6_0)(= x_7_0 x_6_0)(= x_11_0 x_6_0)(= y_11_0 y_6_0)(= z_11_0 z_6_0)(or (and (> y_6_0 z_6_0) (and (= t_7_1 y_7_0) (= y_7_1 z_7_0) (= z_7_1 t_7_1) (= x_12_0 x_7_0) (= y_12_0 y_7_1) (= z_12_0 z_7_1) )
) (and (not (> y_6_0 z_6_0)) (and (= x_12_0 x_11_0) (= y_12_0 y_11_0) (= z_12_0 z_11_0) )
))(= x_13_0 x_12_0)(= y_13_0 y_12_0)(= z_13_0 z_12_0)(= x_17_0 x_12_0)(= y_17_0 y_12_0)(= z_17_0 z_12_0)(or (and (> x_12_0 y_12_0) (and (= t_13_1 x_13_0) (= x_13_1 y_13_0) (= y_13_1 t_13_1) (= x_18_0 x_13_1) (= y_18_0 y_13_1) (= z_18_0 z_13_0) )
) (and (not (> x_12_0 y_12_0)) (and (= x_18_0 x_17_0) (= y_18_0 y_17_0) (= z_18_0 z_17_0) )
))true)
) (and (<= x_18_0 y_18_0) (<= y_18_0 z_18_0)))))
(check-sat)
(get-model)


======Z3 Output:======
 unsat
(error "line 49 column 10: model is not available")

