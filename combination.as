/ combination program
/ computes n choose r
/ assumes n >= r
/ result in r5

define n 3
define r 3

     ldi r1 #1
     str r1

     ldi r1 n 
     ldi r2 r

     cmp r1 r2
     bif zero eq

     sub r1 r1 r2 
     cpy r3 r1
     inc r2 r2

lout cmp r2 r0
     bif zero dout
     ldi r7 #0
     cpy r1 r3
lin  cmp r1 r0
     bif zero din
     
     lod r4
     inc r7 r7
     lod r5
     add r5 r5 r4
     str r5

     dec r1 r1
     jmp lin   
din  dec r2 r2
     jmp lout
eq   ldi r5 #1
dout hlt