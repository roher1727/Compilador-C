
	.globl _main
_main:

	mov	$1, %eax
	push	%eax
	mov	$0, %eax
	pop	%ecx
	cmpl	%eax, %ecx
	movl	$0, %eax
	setg	%al
	ret