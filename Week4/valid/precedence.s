
	.globl _main
_main:

	mov	$1, %eax
	cmpl	$0, %eax
	je	_clause
	movl	$1, %eax
	jmp	_end
_clause:
	cmpl	$0, %eax
	movl	$0, %eax
	setne	%al
_end:
	ret