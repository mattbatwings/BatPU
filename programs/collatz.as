/ collatz conjecture
/ displays 1 on number display once it reached 1

define start 15

      ldi r1 start
      ldi r2 #1
      ldi r7 number_display
.loop str r1
      cmp r1 r2
      bif zero .done / if r1 == 1, stop
      and r3 r1 r2
      cmp r3 r0
      bif zero .even
      / make r1 = 3n+1
      cpy r3 r1
      lsh r3 r3
      inc r3 r3
      add r1 r1 r3
      jmp .loop
.even rsh r1 r1
      jmp .loop
.done hlt