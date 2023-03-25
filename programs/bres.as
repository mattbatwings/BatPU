/ brezzy
/ assumes x2 > x1 and y2 > y1

define x1 0
define y1 1
define x2 6
define y2 5

define dx 3
define a 4
define inter 5
define b 6

/ initial load
        ldi r1 x1
        ldi r2 y1
        ldi r3 x2
        ldi r4 y2
        
        ldi r7 screen_x
        str r1
        ldi r7 screen_y
        str r2

/ r3 = dx, r4 = dy

        sub r3 r3 r1
        sub r4 r4 r2

/ if dy > dx, swap and set r5 = interchange

        cmp r3 r4
        bif msb .inter1
        jmp .inter0
.inter1 cpy r5 r4
        cpy r4 r3
        cpy r3 r5
        ldi inter #1
        jmp .skip
.inter0 ldi inter #0

/ r4 = a, mem[1] = e, r6 = b

.skip   lsh r4 r4     / r4 = 2dy = a
        sub r6 r4 r3  / r6 = 2dy - dx = e
        ldi r7 #1
        str r6 
        sub r6 r6 r3  / r6 = e - dx = b

/ plot pixel first at .loop then check for branch
/ begin pixel loop

        / write pixel 
.loop   ldi r7 #2
        str r1 / put away x
        ldi r7 screen_opcode
        ldi r1 plot_pixel
        str r1
        str r0
        
        / while dx > 0
        cmp dx r0
        bif zero .done
        dec dx dx

        / error branch
        ldi r7 #1
        lod r1
        cmp r1 r0
        bif msb .nerr

        / error >= 0
.perr   add r1 r1 b
        str r1

        ldi r7 screen_y
        inc r2 r2
        str r2
        jmp .x++

        / error < 0
.nerr   add r1 r1 a
        str r1
        cmp inter r0
        bif zero .noint
        
        ldi r7 screen_y
        inc r2 r2
        str r2
        jmp .rep

.noint  jmp .x++

.x++    ldi r7 #2
        lod r1 / get x back
        inc r1 r1
        ldi r7 screen_x
        str r1
        jmp .loop

.rep    ldi r7 #2
        lod r1 / get x back 
        jmp .loop
.done   hlt



