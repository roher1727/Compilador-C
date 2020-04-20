
	.globl _main
_main:

	mov	$2, %eax
	push	%eax
	pop	%ecx
	cmpl	%eax, %ecx
	movl	$0, %eax
	sete	%al
	ret