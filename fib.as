/ fibonacci
/ assumes iterations >= 0
/ result in r3

define iterations 10

     ldi r2 #1
     ldi r4 iterations
loop sub r4 r4 r0
     bif zero done
     add r1 r2 r0
     add r2 r3 r0
     add r3 r1 r2
     dec r4 r4
     jmp loop
done hlt

/ 0 returns 0
/ 1 returns 