.data
flag: .asciiz "IW{M1P5_!S_FUN}\n"

.text
.globl main
main:
    la $t0, flag        
    move $t1, $0        

    for:
        sgt $t2, $t1, 15 
        beq $t2, 1, exit 

        add $t2, $t0, $t1   
        lb $a0, ($t2)       
        xor $a0, $a0, $t1    
        sb $a0, 0($t2)  

        add $t1, $t1, 1  
        j for            


exit:
    move $a0, $t0       
    jal printstring     
    li $v0, 10          
    syscall             

printstring:
    li  $v0, 4  
    syscall     
    jr  $ra     