
	.globl _main
_main:

	mov	$1, %eax
	neg	%eax
	mov	$2, %eax
	sub	%ecx, %eax
	ret
