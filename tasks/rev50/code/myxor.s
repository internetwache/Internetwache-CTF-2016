.data
flag: .asciiz "IW{M1P5_!S_FUN}\n"

.text
.globl main
main:
    la $t0, flag        # Load address of flag to $t0
    move $t1, $0        # Initialize loop counter with 0

    for:
        sgt $t2, $t1, 15 # If i > 15 goto print
        beq $t2, 1, exit #Print string when done

        add $t2, $t0, $t1   #Offset is address + counter
        lb $a0, ($t2)       #Load byte
        xor $a0, $a0, $t1    #XOR with ith position
        sb $a0, 0($t2)  #Save back

        add $t1, $t1, 1  # i++
        j for            # Jump back to for


exit:
    move $a0, $t0       # Move string address to $a0
    jal printstring     # Print string
    li $v0, 10          # Exit code
    syscall             # Exit programm

printstring:
    li  $v0, 4  #
    syscall     # Print null-terminated string
    jr  $ra     #