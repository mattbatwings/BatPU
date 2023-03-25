define start_x 4
define start_y 4
define x 1
define y 2

        ldi r7 screen_opcode
        ldi r6 plot_pixel
        str r6

        ldi r1 start_x
        ldi r2 start_y

.loop   ldi r7 input
        lod r3

.pleft  ldi r4 p_left
        and r5 r4 r3
        bif zero .pright
        dec x x
        jmp .draw
.pright ldi r4 p_right
        and r5 r4 r3
        bif zero .pup
        inc x x
        jmp .draw
.pup    ldi r4 p_up
        and r5 r4 r3
        bif zero .pdown
        inc y y
        jmp .draw
.pdown  ldi r4 p_down
        and r5 r4 r3
        bif zero .draw
        dec y y

.draw   ldi r7 screen_x
        str x
        ldi r7 screen_y
        str y
        jmp .loop

