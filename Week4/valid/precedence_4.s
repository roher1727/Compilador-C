
	.globl _main
_main:

	mov	$2, %eax
	push	%eax
	mov	$2, %eax
	pop	%ecx
	cmpl	%eax, %ecx
	movl	$0, %eax
	sete	%al
	cmpl	$0, %eax
	je	_clause
	movl	$1, %eax
	jmp	_end
_clause:
	mov	$0, %eax
	cmpl	$0, %eax
	movl	$0, %eax
	setne	%al
_end:
	ret