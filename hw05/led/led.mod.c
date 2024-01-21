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
	{ 0xce5798e1, "param_ops_uint" },
	{ 0xfe990052, "gpio_free" },
	{ 0xa8fedea6, "gpiod_unexport" },
	{ 0x1804d458, "kthread_stop" },
	{ 0xeeaaf8d, "wake_up_process" },
	{ 0xe34fe8e5, "kthread_create_on_node" },
	{ 0xfeca4e1d, "gpiod_export" },
	{ 0xb88c333, "gpiod_direction_output_raw" },
	{ 0x47229b5c, "gpio_request" },
	{ 0x56c87b84, "kobject_put" },
	{ 0xee3dcb64, "sysfs_create_group" },
	{ 0x868f8b1f, "kobject_create_and_add" },
	{ 0x7f8ce477, "kernel_kobj" },
	{ 0x8f678b07, "__stack_chk_guard" },
	{ 0x86332725, "__stack_chk_fail" },
	{ 0xbcab6ee6, "sscanf" },
	{ 0x84b183ae, "strncmp" },
	{ 0xf9a482f9, "msleep" },
	{ 0xb3f7646e, "kthread_should_stop" },
	{ 0xc5850110, "printk" },
	{ 0xbe13c4e3, "gpiod_set_raw_value" },
	{ 0xc435f86e, "gpio_to_desc" },
	{ 0x3c3ff9fd, "sprintf" },
	{ 0xefd6cf06, "__aeabi_unwind_cpp_pr0" },
};

MODULE_INFO(depends, "");


MODULE_INFO(srcversion, "008A068FEA9AF109F4152F6");
