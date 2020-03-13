
	.globl _main
_main:

	mov	$3, %eax
	neg	%eax
	cmpl	$0, %eax
	movl	$0, %eax
	sete	%al
	ret