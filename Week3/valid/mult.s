
	.globl _main
_main:

	mov	$2, %eax
	push	%eax
	mov	$3, %eax
	pop	%ecx
	imul	%ecx, %eax
	ret
