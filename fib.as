/ fibonacci
/ assumes iterations >= 0
/ result in r3

define iterations 13

      ldi r2 #1
      ldi r4 iterations
.loop cmp r4 r0
      bif zero .done
      cpy r1 r2
      cpy r2 r3
      add r3 r1 r2
      dec r4 r4
      jmp .loop
.done hlt

