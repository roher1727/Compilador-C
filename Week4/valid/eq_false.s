
write_a_c_compiler/stage_4/valid/eq_false.c
	.globl _main
	_main:
	ret{-}
	push	%rax
{}
	pop	%rbx
	cmp	%rax, %rbx
	mov	$0, %rax
	sete	%al	mov	$1 %eax	mov	$2 %eax