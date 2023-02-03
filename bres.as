/ brezzy
/ assumes x2 > x1 and y2 > y1

define x1 6
define y1 9
define x2 17
define y2 31

/ allocation
/ r1 - x
/ r2 - y
/ r3 - dx
/ r4 - a
/ r5 - b
/ r6 - e
/ ram[0] = interchange

/ initial load

        ldi r1 x1
        ldi r2 y1
        ldi r3 x2
        ldi r4 y2 

/ r3 = dx, r4 = dy

        sub r3 r3 r1
        sub r4 r4 r2

/ if dy > dx

        cmp r3 r4
        bif carry .inter / branch if dy > dx
        jmp .skip
.inter  cpy r5 r4
        cpy r4 r3
        cpy r3 r5
        ldi r5 #1
        ldi r7 #0
        str r5

/ r4 = a, r6 = e, r5 = b, dx++ for the do while

.skip   lsh r4 r4
        sub r6 r4 r3
        lsh r5 r3
        sub r5 r4 r5

/ main loop

.loop   ldi r7 #62
        str r1
        dec r7 r7
        str r2
        dec r7 r7
        ldi r1 #2
        str r1 / write pixel
        str r0 / reset to noop
        ldi r7 #62
        lod r1
        cmp r3 r0 / while dx > 0
        bif zero .done
        cmp r6 r0
        bif carry .nerr / branch if 0 > error
        inc r1 r1
        inc r2 r2
        add r6 r6 r5
        jmp .rep
.nerr   add r6 r6 r4
        ldi r7 #0
        lod r1
        cmp r1 r0
        ldi r7 #62
        lod r1
        bif zero .noint
        inc r2 r2
        jmp .rep
.noint  inc r1 r1
.rep    dec r3 r3
        jmp .loop
.done   hlt



