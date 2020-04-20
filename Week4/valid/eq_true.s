
	.globl _main
_main:

	mov	$1, %eax
	push	%eax
	mov	$1, %eax
	pop	%ecx
	cmpl	%eax, %ecx
	movl	$0, %eax
	sete	%al
	ret