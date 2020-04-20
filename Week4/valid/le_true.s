
	.globl _main
_main:

	mov	$0, %eax
	push	%eax
	mov	$2, %eax
	pop	%ecx
	cmpl	%eax, %ecx
	movl	$0, %eax
	setle	%al
	ret