/ fibonacci
/ assumes iterations >= 0
/ displays cumulative results on number display

define iterations 13

      ldi r2 #1
      ldi r4 iterations
      ldi r7 number_display
.loop str r3
      cmp r4 r0
      bif zero .done
      cpy r1 r2
      cpy r2 r3
      add r3 r1 r2
      dec r4 r4
      jmp .loop
.done hlt

