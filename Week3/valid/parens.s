
	.globl _main
_main:

	mov	$3, %eax
	push	%eax
	mov	$4, %eax
	pop	%ecx
	addl	%ecx, %eax
	mov	$2, %eax
	push	%eax
	pop	%ecx
	imul	%ecx, %eax
	ret
