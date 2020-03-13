
	.globl _main
_main:

	mov	$1, %eax
	cmpl	$0, %eax
	je	_clause2
	movl	$1, %eax
	jmp	_end
_clause2:
	cmpl	$0, %eax
	movl	$0, %eax
	setne	%al
_end:
	ret
