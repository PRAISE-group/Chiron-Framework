(not (and  ))

=> 
(and  (= s_in 0) (and (>= n1 0) (and (< n_in 100000) (>= k 5)))) 
(= (- (+ s_in n_in) (* (div (+ s_in n_in) 3) 3)) 0)

(=> 
 and (= x (- n_in (* (div n_in 10) 10))) (= s1 (+ s_in x)) (= n1 (div n_in 10)) (= n_out n1) (= s_out s1) (> __rep_counter_1 0) (<= __rep_counter_1 k) (= (- (+ s_in n_in) (* (div (+ s_in n_in) 3) 3)) 0)
 (= (- (+ s_out n_out) (* (div (+ s_out n_out) 3) 3)) 0))

(=> 
 (and (= x (- n_in (* (div n_in 10) 10))) (= s1 (+ s_in x)) (= n1 (div n_in 10)) (= n_out n1) (= s_out s1) (not (and (> __rep_counter_1 0) (<= __rep_counter_1 k) true))) 
 (and (= ans (ite (= (- s_out (* (div s_out 3) 3)) 0) 1 0)) (= (- n_out (* (div n_out 3) 3)) 0))) 


n1 7719
k 0
s_out 0
s1 0
__rep_counter_1 1
s_in 0
n_in 77190
x 0
n_out 7719
ans 2



# AP

# ; Declare variables
# (declare-const a Int)   ; First term of AP
# (declare-const d Int)   ; Common difference
# (declare-const n Int)   ; Number of iterations (n >= 0)
# (declare-const i Int)   ; Loop counter
# (declare-const x Int)   ; Loop variable

# ; Preconditions: Initial values before the loop
# (assert (= i 0))
# (assert (= x a))

# ; Invariant: x = a + i * d (for all valid i)
# (define-fun loop_invariant ((i Int) (x Int)) Bool
#   (= x (+ a (* i d))))

# ; Assert that the invariant holds initially
# (assert (loop_invariant i x))

# ; Universal quantification: Invariant holds for all iterations
# (assert (forall ((j Int) (y Int))
#     (=> (and (>= j 0) (< j n))
#         (loop_invariant (+ j 1) (+ y d)))))

# ; Postcondition: After n iterations, x should be the nth term
# (assert (not (loop_invariant n (+ a (* n d)))))  ; Should be UNSAT if correct

# ; Check correctness
# (check-sat)
# (get-model)




# Div by 3

# ;(set-logic QF_LIA)

# ; Declare variables
# (declare-const k Int)   ; Number of iterations (digits in n)
# (declare-fun n (Int) Int)   ; n(k): The value of n at step k
# (declare-fun n1 (Int) Int)  ; n1(k): Temporary value of n after removing last digit
# (declare-fun s (Int) Int)   ; Sum of extracted digits at step k
# (declare-fun x (Int) Int)   ; Extracted digit at step k
# (declare-const ans Int)     ; Answer variable (1 if divisible by 3, 0 otherwise)

# ; Preconditions: Initial values
# (assert (= k 10))   ; Number of digits must be non-negative
# (assert (< (n 0) 999999999))
# (assert (= (s 0) 0))    ; Sum starts at 0
# (assert (forall ((i Int)) (> (n i) 0)))
# ; Loop invariant: The transformation of n
# (assert (forall ((i Int)) 
#     (=> (and (>= i 0) (< i k)) 
#         (and 
#             (= (n1 i) (div (n (- i 1)) 10))   ; n1(k) = n(k-1) / 10
#             (= (n i) (n1 i))                 ; n(k) = n1(k)
#             (= (x i) (- (n (- i 1)) (* 10 (n1 i))))  ; Extract last digit x(k)
#             (= (s i) (+ (s (- i 1)) (x i)))  ; Sum up digits
#             (= (mod (+ (s i) (n i)) 3) 0)    ; Check divisibility by 3
#         )
#     )
# ))

# ; Assign ans using ite (if-then-else)
# (assert (= ans (ite (= (mod (n 0) 3) 0) 1 0)))

# ; Postcondition: Ensure ans is set correctly
# (assert (or 
#     (and (= ans 1) (= (mod (s k) 3) 0))  ; ans = 1 if sum of digits is div by 3
#     (and (= ans 0) (not (= (mod (s k) 3) 0)))  ; ans = 0 otherwise
# ))

# ; Check satisfiability
# (check-sat)
# (get-model)


# entry[1] has the type
            if entry[1] == "assign":
                # Extract variables from the statement
                vars = extract_variables_assign(stmt)
                rhs_vars = vars[0]
                rexpr = vars[1]
                lhs_vars = vars[2]
                lexpr = vars[3]
            else:
                # Extract variables from the statement
                vars = extract_variables_others(stmt)
                rhs_vars = vars
                rexpr = stmt
                lhs_vars = []
                lexpr = ""
                
            for var in rhs_vars:
                # print(rhs_vars)
                # remove everything after last underscore
                # print(var.split("_"))
                primary_var = "_".join(var.split("_")[0:-1])
                print(primary_var)
                succ_block_id = succ.irID
                new_instrlist.append([f"{primary_var}_{succ_block_id} = {primary_var}_{block_id}", "assign"])
        