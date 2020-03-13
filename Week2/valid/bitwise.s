
	.globl _main
_main:

	cmpl	$0, %eax
	movl	$0, %eax
	sete	%al
	mov	$12, %eax
	ret