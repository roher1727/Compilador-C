
	.globl _main
_main:

	mov	$1, %eax
	cmpl	$0, %eax
	je	_clause2
	jmp	_end
_clause2:
	neg	%eax
	cmpl	$0, %eax
	movl	$0, %eax
	setne	%al
_end:
	ret