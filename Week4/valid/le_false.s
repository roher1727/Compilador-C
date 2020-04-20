
	.globl _main
_main:

	mov	$1, %eax
	push	%eax
	neg	%eax
	pop	%ecx
	cmpl	%eax, %ecx
	movl	$0, %eax
	setle	%al
	ret