// K = 12
// Width = 16 pixels
// Height = 20 pixels
// Starting address = 16768

(LOOP)
    @KBD
    D=M
    @WHITE
    D;JEQ

    @color
    M=-1
    @DRAW
    0;JMP

(WHITE)
    @color
    M=0

(DRAW)
    @16768
    D=A
    @ptr
    M=D

    @20
    D=A
    @count
    M=D

(ROW)
    @color
    D=M

    @ptr
    A=M
    M=D

    @32
    D=A
    @ptr
    M=D+M

    @count
    MD=M-1
    @ROW
    D;JGT

    @LOOP
    0;JMP
