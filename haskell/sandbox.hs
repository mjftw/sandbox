doubleMe x = x*2

doubleUs x y = doubleMe x + doubleMe y

doubleLessThan x thresh = if x < thresh
                            then doubleMe x
                            else x

-- Horribly inefficient implementation
fibonacci n = if (n <= 2)
                then 1
                else fibonacci (n-1) + fibonacci (n-2)

tensUpTo x = [0,10..x]

-- inefficient multiply
multipleOf n x = [0,x..] !! n

-- computationally POOR
{-
Python equivalent:
    def firstNFibonacci(n):
        return [fibonacci(x) for x in range(1, n)]
-}
firstNFibonacci n = [fibonacci x | x <- [1..n]]

-- computationally POOR
{-
Python equivalent:
    def firstNFibonacciOver(n, max):
        return [fibonacci(x) for x in range(1, n) if x > max]
-}
firstNFibonacciOver n max = [fibonacci x | x <- [1..n], x > max]

-- FizzBuzz implementation - create a list of n FizzBuzz values
strDefault str val = if str == "" then val else str
strValIfDivBy x y value = if (x `mod` y) == 0 then value else ""
fizzBuzz n = [strDefault ((strValIfDivBy x 3 "Fizz") ++ (strValIfDivBy x 5 "Buzz")) (show x) | x <- [1..n]]

allUpperLowerCombos = [x:y:[] | x <- ['a'..'z'], y <- ['A'..'Z']]

length' xs = sum [1 | _ <- xs]

-- Some matrix maths
-- v = [x1, x2, x3]

dot :: [Int] -> [Int] -> Int
dot v1 v2 = sum [v1n + v2n | v1n <- v1, v2n <- v2]

-- calculate Pi using Leibniz formula
piN n = 4 * (1 - (sum [1/x | x <- [3, 7..n]]) + (sum [1/x | x <- [5, 9..n]]))

fibonacci' :: Int -> Int
fibonacci' 1 = 1
fibonacci' 2 = 1
fibonacci' n = fibonacci (n-2) + fibonacci (n-1)

-- Much more efficient but uglier version
_fibonacci_helper'' :: Int -> Int -> Int -> Int -> Int
_fibonacci_helper'' n idx prev curr
    | idx >= n = curr
    | otherwise = _fibonacci_helper'' n (idx+1) curr (prev+curr)

fibonacci'' :: Int -> Int
fibonacci'' n
    | n <=2 = 1
    | otherwise = _fibonacci_helper'' n 1 1 1