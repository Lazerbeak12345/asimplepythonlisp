(define pie 3)             ; defines pie to be 3
 
(define (piece str)        ; defines piece as a function
  (substring str 0 pie))   ;  of one argument

pie

(print
  (piece "key lime"))

