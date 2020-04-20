
	.globl _main
_main:

	mov	$2, %eax
	push	%eax
	mov	$1, %eax
	pop	%ecx
	cmpl	%eax, %ecx
	movl	$0, %eax
	setl	%al
	ret