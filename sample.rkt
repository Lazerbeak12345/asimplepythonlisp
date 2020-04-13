#lang racket
(define (bake flavor)
  (printf "preheating oven...\n")
  (string-append flavor " pie"))
 
(bake "apple")

