/**
 * @file   gpio_test.c
 * @author Derek Molloy
 * @date   19 April 2015
 * @brief  A kernel module for controlling a GPIO LED/button pair. The device mounts devices via
 * sysfs /sys/class/gpio/gpio115 and gpio49. Therefore, this test LKM circuit assumes that an LED
 * is attached to GPIO 49 which is on P9_23 and the button is attached to GPIO 115 on P9_27. There
 * is no requirement for a custom overlay, as the pins are in their default mux mode states.
 * @see http://www.derekmolloy.ie/
*/

#include <linux/init.h>
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/gpio.h>                 // Required for the GPIO functions
#include <linux/interrupt.h>            // Required for the IRQ code

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Derek Molloy");
MODULE_DESCRIPTION("A Button/LED test driver for the BBB");
MODULE_VERSION("0.1");
#define gpioLED 51
#define gpioLED1 60
#define gpioLED2 50

#define gpioButton 48
#define gpioButton1 47
#define gpioButton2 65
//static unsigned int gpioLED = 51;       ///< hard coding the LED gpio for this example to P9_16 (GPIO51)
//static unsigned int gpioButton = 48;   ///< hard coding the button gpio for this example to P9_15 (GPIO48)
static unsigned int numberPresses = 0;  ///< For information, store the number of button presses

//static unsigned int gpioLED1 = 60;       ///< hard coding the LED gpio for this example to P9_12 (GPIO60)
//static unsigned int gpioButton1 = 47;   ///< hard coding the button gpio for this example to P8_15 (GPIO47)
                                    ///
//static unsigned int gpioLED2 = 50;       ///< hard coding the LED gpio for this example to P9_14 (GPIO50)
//static unsigned int gpioButton2 = 65;   ///< hard coding the button gpio for this example to P8_18 (GPIO65)
/// Function prototype for the custom IRQ handler function -- see below for the implementation
static irq_handler_t  ebbgpio_irq_handler(unsigned int irq, void *dev_id, struct pt_regs *regs);

unsigned int LEDarr[3] = {gpioLED,gpioLED1,gpioLED2};
unsigned int BUTTarr[3] = {gpioButton, gpioButton1, gpioButton2};
unsigned int IRQarr[3];
bool ledStatus[3] = {false, false, false};
int i;
/** @brief The LKM initialization function
 *  The static keyword restricts the visibility of the function to within this C file. The __init
 *  macro means that for a built-in driver (not a LKM) the function is only used at initialization
 *  time and that it can be discarded and its memory freed up after that point. In this example this
 *  function sets up the GPIOs and the IRQ
 *  @return returns 0 if successful
 */
static int __init ebbgpio_init(void){
   int result = 0;
   printk(KERN_INFO "GPIO_TEST: Initializing the GPIO_TEST LKM\n");
   //LEDarr[0] = gpioLED;
   //LEDarr[1] = gpioLED1;
   //LEDarr[0] = gpioLED2;

   //BUTTarr[0] = gpioButton;
   //BUTTarr[1] = gpioButton1;
   //BUTTarr[2] = gpioButton2;
   // Is the GPIO a valid GPIO number (e.g., the BBB has 4x32 but not all available)
   for (i = 0; i < 3; i++)
   {
       if (!gpio_is_valid(LEDarr[i])){
          printk(KERN_INFO "GPIO_TEST: invalid LED GPIO %d\n",LEDarr[i]);
          return -ENODEV;
       }
       if (!gpio_is_valid(BUTTarr[i])){
          printk(KERN_INFO "GPIO_TEST: invalid LED GPIO %d\n",BUTTarr[i]);
          return -ENODEV;
       }
       // Going to set up the LED. It is a GPIO in output mode and will be on by default
       ledStatus[i] = true;
       gpio_request(LEDarr[i], "sysfs");          // gpioLED is hardcoded to 49, request it
       gpio_direction_output(LEDarr[i],ledStatus[i]);   // Set the gpio to be in output mode and on
    // gpio_set_value(gpioLED, ledOn);          // Not required as set by line above (here for reference)
       gpio_export(LEDarr[i], false);             // Causes gpio49 to appear in /sys/class/gpio
                                    // the bool argument prevents the direction from being changed
       gpio_request(BUTTarr[i], "sysfs");       // Set up the gpioButton
       gpio_direction_input(BUTTarr[i]);        // Set the button GPIO to be an input
       gpio_set_debounce(BUTTarr[i], 200);      // Debounce the button with a delay of 200ms
       gpio_export(BUTTarr[i], false);          // Causes gpio115 to appear in /sys/class/gpio
                                    // the bool argument prevents the direction from being changed
       // Perform a quick test to see that the button is working as expected on LKM load
       printk(KERN_INFO "GPIO_TEST: The button %d state is currently: %d\n", i, gpio_get_value(BUTTarr[i]));

       // GPIO numbers and IRQ numbers are not the same! This function performs the mapping for us
       IRQarr[i] = gpio_to_irq(BUTTarr[i]);
       printk(KERN_INFO "GPIO_TEST: The button %d is mapped to IRQ: %d\n",BUTTarr[i], IRQarr[i]);

       // This next call requests an interrupt line
       result = request_irq(IRQarr[i],             // The interrupt number requested
                            (irq_handler_t) ebbgpio_irq_handler, // The pointer to the handler function below
                            IRQF_TRIGGER_RISING,   // Interrupt on rising edge (button press, not release)
                            "ebb_gpio_handler",    // Used in /proc/interrupts to identify the owner
                            NULL);                 // The *dev_id for shared interrupt lines, NULL is okay

       printk(KERN_INFO "GPIO_TEST: The interrupt request %d result is: %d\n",i, result);
    }
   return result;
}

/** @brief The LKM cleanup function
 *  Similar to the initialization function, it is static. The __exit macro notifies that if this
 *  code is used for a built-in driver (not a LKM) that this function is not required. Used to release the
 *  GPIOs and display cleanup messages.
 */
static void __exit ebbgpio_exit(void){
    for (i = 0; i < 3; i++)
    {
        printk(KERN_INFO "GPIO_TEST: The button %d state is currently: %d\n",BUTTarr[i], gpio_get_value(BUTTarr[i]));
        gpio_set_value(LEDarr[i], 0);              // Turn the LED off, makes it clear the device was unloaded
        gpio_unexport(LEDarr[i]);                  // Unexport the LED GPIO
        free_irq(IRQarr[i], NULL);               // Free the IRQ number, no *dev_id required in this case
        gpio_unexport(BUTTarr[i]);               // Unexport the Button GPIO
        gpio_free(LEDarr[i]);                      // Free the LED GPIO
        gpio_free(BUTTarr[i]);                   // Free the Button GPIO
    }
    printk(KERN_INFO "GPIO_TEST: Goodbye from the LKM!\n");
    printk(KERN_INFO "GPIO_TEST: The button was pressed %d times\n", numberPresses);
}

/** @brief The GPIO IRQ Handler function
 *  This function is a custom interrupt handler that is attached to the GPIO above. The same interrupt
 *  handler cannot be invoked concurrently as the interrupt line is masked out until the function is complete.
 *  This function is static as it should not be invoked directly from outside of this file.
 *  @param irq    the IRQ number that is associated with the GPIO -- useful for logging.
 *  @param dev_id the *dev_id that is provided -- can be used to identify which device caused the interrupt
 *  Not used in this example as NULL is passed.
 *  @param regs   h/w specific register values -- only really ever used for debugging.
 *  return returns IRQ_HANDLED if successful -- should return IRQ_NONE otherwise.
 */
static irq_handler_t ebbgpio_irq_handler(unsigned int irq, void *dev_id, struct pt_regs *regs){
  printk(KERN_INFO "GPIO_TEST: Interrupt called by %d\n",irq);
  for (i = 0; i < 3; i++)
  { 
      printk(KERN_INFO "GPIO_TEST: Interrupt! (button %d state is %d)\n",i, gpio_get_value(BUTTarr[i]));
      if(irq == IRQarr[i])
      {
        ledStatus[i] = !(ledStatus[i]);      // Invert the LED state on each button presyy
        gpio_set_value(LEDarr[i], ledStatus[i]);          // Set the physical LED accordingly
        //printk(KERN_INFO "GPIO_TEST: Interrupt! (button %d state is %d)\n",i, gpio_get_value(BUTTarr[i]));
      }
  }

   numberPresses++;                         // Global counter, will be outputted when the module is unloaded
   return (irq_handler_t) IRQ_HANDLED;      // Announce that the IRQ has been handled correctly
}

/// This next calls are  mandatory -- they identify the initialization function
/// and the cleanup function (as above).
module_init(ebbgpio_init);
module_exit(ebbgpio_exit);
