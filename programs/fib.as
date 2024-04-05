/ fibonacci
/ assumes iterations >= 0
/ displays cumulative results on number display

define iterations 13

      ldi r1 #0
      ldi r2 #1
      ldi r4 iterations
      ldi r7 number_display
.loop str r3
      cmp r4 r0
      bif zero .done
      add r1 r1 r2
      add r2 r1 r2
      dec r4 r4
      cmp r4 r0
      bif zero .done
      dec r4 r4
      jmp .loop
.done hlt

