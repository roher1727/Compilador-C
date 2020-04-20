
	.globl _main
_main:

	neg	%eax
	push	%eax
	neg	%eax
	pop	%ecx
	cmpl	%eax, %ecx
	movl	$0, %eax
	setne	%al
	ret