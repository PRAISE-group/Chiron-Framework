import z3

# Create a solver instance
s = z3.Solver()

# Declare integer variables
a = z3.Int('a')  # First term
d = z3.Int('d')  # Common difference
n = z3.Int('n')  # Term index (should be >= 1)
T_n = z3.Int('T_n')  # The nth term

# Declare a function f(n) representing the nth term of AP
f = z3.Function('f', z3.IntSort(), z3.IntSort())

# Define the nth term function using universal quantification
s.add(z3.ForAll(n, z3.Implies(n >= 1, f(n) == a + (n - 1) * d)))

# Assert that the computed nth term is correct
s.add(T_n == f(n))

# Check satisfiability
print(s.check())

# Get and print the model
print(s.model())




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
