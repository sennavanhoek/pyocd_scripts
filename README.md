# Playing around with pyOCD

pyOCD installation:
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


## Script index:

| Script        	  | Description                                                                          	|
|-------------------|------------------------------------------------------------------------------------------|
| usart_over_swd.py | Hooks the 'send_USART_str' function to print the output without actual USART connection.  |
| id_cores.py       | Prints the core type, revision/patch and if an FPU is available e.g. "Cortex-M4 r0p1 with FPU".|
