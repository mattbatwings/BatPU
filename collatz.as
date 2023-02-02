/ collatz conjecture
/ r1 should end in 1

define start 23

      ldi r1 start
      ldi r2 #1
.loop cmp r1 r2 /print r1
      bif zero .done
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