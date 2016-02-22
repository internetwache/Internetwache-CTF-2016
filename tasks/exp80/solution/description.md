exploit80: Remote Printer
============
Printer are very very important for offices. Especially for remote printing. My boss told me to build a tool for that task. 

Compilation:
gcc -m32 -fno-stack-protector RemotePrinter.c -o RemotePrinter -z execstack
strip RemotePrinter