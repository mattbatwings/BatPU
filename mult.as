/ multiplication
/ computes a * b
/ result in r3

define a 14
define b 12

      ldi r1 a
      ldi r2 b
      ldi r4 #8
      ldi r5 #1
      ldi r7 #63
.loop cmp r4 r0
      bif zero .done
      and r0 r1 r5
      bif zero .skip
      add r3 r3 r2
.skip rsh r1 r1
      lsh r2 r2
      dec r4 r4
      jmp .loop
.done str r3
      hlt