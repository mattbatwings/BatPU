/ multiplication
/ computes a * b
/ displays result on number display

define a 14
define b 7

      ldi r1 a
      ldi r2 b
      ldi r3 #0
      ldi r4 #8
      ldi r5 #1
.loop cmp r4 r0
      bif zero .done
      and r0 r1 r5
      bif zero .skip
      add r3 r3 r2
.skip rsh r1 r1
      lsh r2 r2
      dec r4 r4
      jmp .loop
.done ldi r7 number_display
      str r3
      hlt