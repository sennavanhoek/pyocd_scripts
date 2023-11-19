# Playing around with pyOCD

### Script index:

| Script        	  | Description                                                                          	|
|-------------------|------------------------------------------------------------------------------------------|
| usart_over_swd.py | Hooks the 'send_USART_str' function to print the output without actual USART connection.  |
| id_cores.py       | Prints a discription the core(s) e.g. "Cortex-M4 r0p1 with FPU".|

### pyOCD quickstart:
```
$ pip install pyocd
```
Example of installing CMSIS-Pack for a plugged in board.
```
$ pyocd list
  #   Probe/Board	Unique ID              	Target      	 
-----------------------------------------------------------------
  0   STM32 STLink   0667FF565588494867114514   ✖︎ stm32f407vgtx  
  	DISCO-F407VG
 	 
$ pyocd pack install stm32f407vgtx
```
