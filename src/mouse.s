; AppleMouse II / Apple IIc firmware interface, polled without IRQs.
; Pascal device signatures and entry offsets per Apple Mouse Technical Notes.
.include "zeropage.inc"
.export _native_init, _native_poll, _native_move
.export _mouse_x, _mouse_y, _mouse_button
.segment "BSS"
_mouse_x: .res 2
_mouse_y: .res 2
_mouse_button: .res 1
slot: .res 1
.segment "CODE"
_native_init:
 lda #0
 sta ptr1
 lda #$c1
 sta ptr1+1
scan:
 ldy #$05
 lda (ptr1),y
 cmp #$38
 bne next
 ldy #$07
 lda (ptr1),y
 cmp #$18
 bne next
 ldy #$0b
 lda (ptr1),y
 cmp #1
 bne next
 iny
 lda (ptr1),y
 cmp #$20
 beq found
next:
 inc ptr1+1
 lda ptr1+1
 cmp #$c8
 bne scan
 lda #0
 tax
 rts
found:
 lda ptr1+1
 sta lookup+2
 sta xparam+1
 sta jump+2
 and #15
 sta slot
 asl
 asl
 asl
 asl
 sta yparam+1
 ldx #$19
 jsr firmware
 lda #1
 ldx #$12
 jsr firmware
 ; Clamp X=0..279.
 ldx slot
 lda #0
 sta $0478
 sta $0578
 lda #<279
 sta $04f8
 lda #>279
 sta $05f8
 lda #0
 ldx #$17
 jsr firmware
 ; Clamp Y=0..191.
 ldx slot
 lda #0
 sta $0478
 sta $0578
 sta $05f8
 lda #191
 sta $04f8
 lda #1
 ldx #$17
 jsr firmware
 lda #140
 sta _mouse_x
 lda #80
 sta _mouse_y
 lda #0
 sta _mouse_x+1
 sta _mouse_y+1
 jsr _native_move
 lda #1
 ldx #0
 rts
_native_move:
 ldx slot
 lda _mouse_x
 sta $0478,x
 lda _mouse_x+1
 sta $0578,x
 lda _mouse_y
 sta $04f8,x
 lda _mouse_y+1
 sta $05f8,x
 ldx #$16
 jmp firmware
_native_poll:
 ldx #$14
 jsr firmware
 ldx slot
 lda $0478,x
 sta _mouse_x
 lda $0578,x
 sta _mouse_x+1
 lda $04f8,x
 sta _mouse_y
 lda $05f8,x
 sta _mouse_y+1
 lda $0778,x
 and #$80
 sta _mouse_button
 rts
firmware:
lookup: ldy $ff00,x
 sty jump+1
xparam: ldx #$ff
yparam: ldy #$ff
jump: jmp $ffff
.segment "HGR"
.res $2000
