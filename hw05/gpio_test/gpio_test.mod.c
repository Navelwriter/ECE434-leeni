#include <linux/module.h>
#define INCLUDE_VERMAGIC
#include <linux/build-salt.h>
#include <linux/vermagic.h>
#include <linux/compiler.h>

BUILD_SALT;

MODULE_INFO(vermagic, VERMAGIC_STRING);
MODULE_INFO(name, KBUILD_MODNAME);

__visible struct module __this_module
__section(".gnu.linkonce.this_module") = {
	.name = KBUILD_MODNAME,
	.init = init_module,
#ifdef CONFIG_MODULE_UNLOAD
	.exit = cleanup_module,
#endif
	.arch = MODULE_ARCH_INIT,
};

#ifdef CONFIG_RETPOLINE
MODULE_INFO(retpoline, "Y");
#endif

static const struct modversion_info ____versions[]
__used __section("__versions") = {
	{ 0xf05d40e2, "module_layout" },
	{ 0xfe990052, "gpio_free" },
	{ 0xc1514a3b, "free_irq" },
	{ 0xa8fedea6, "gpiod_unexport" },
	{ 0x92d5838e, "request_threaded_irq" },
	{ 0x582ae8f3, "gpiod_to_irq" },
	{ 0xffc6c2f3, "gpiod_set_debounce" },
	{ 0x3bfd45d3, "gpiod_direction_input" },
	{ 0xfeca4e1d, "gpiod_export" },
	{ 0xb88c333, "gpiod_direction_output_raw" },
	{ 0x47229b5c, "gpio_request" },
	{ 0xefd6cf06, "__aeabi_unwind_cpp_pr0" },
	{ 0xc5850110, "printk" },
	{ 0x9894082, "gpiod_get_raw_value" },
	{ 0xbe13c4e3, "gpiod_set_raw_value" },
	{ 0xc435f86e, "gpio_to_desc" },
};

MODULE_INFO(depends, "");


MODULE_INFO(srcversion, "E5A3B8529DB4CFA97141B71");
