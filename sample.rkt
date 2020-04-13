#lang racket
(define (bake flavor)
  (printf "preheating oven...\n")
  (string-append flavor " pie"))

;(print
;	(bake "apple"))

;(define (nobake flavor)
;  string-append flavor "jello") 
;
;;(nobake "green")
;
;(define (halfbake flavor
;                  (string-append flavor " creme brulee")))
(bake "apple")

