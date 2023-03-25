/ bouncing ball

define start_x 1
define start_y 3
define start_vx 1
define start_vy 1

define low_val 0
define high_val 7

define x 1
define y 2
define vx 3
define vy 4
define low 0
define high 5

        ldi r1 start_x
        ldi r2 start_y
        ldi r3 start_vx
        ldi r4 start_vy
        ldi r5 high_val

        ldi r7 screen_opcode
        str r0

.loop   cmp x low
        bif zero .flipx
        cmp x high
        bif zero .flipx
        jmp .skipx
.flipx  not vx vx
        inc vx vx
.skipx  cmp y low
        bif zero .flipy
        cmp y high
        bif zero .flipy
        jmp .skipy
.flipy  not vy vy
        inc vy vy
.skipy  add x x vx
        add y y vy
        ldi r7 screen_opcode
        ldi r6 delete_pixel
        str r6
        ldi r7 screen_x
        str r1
        ldi r7 screen_y
        str r2
        ldi r7 screen_opcode
        ldi r6 plot_pixel
        str r6
        jmp .loop