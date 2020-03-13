
	.globl _main
_main:

	mov	$1, %eax
	push	%eax
	mov	$2, %eax
	pop	%ecx
	addl	%ecx, %eax
	ret