# OctoPrint Malyan Connection Fix Plugin

Due to some weird issue with some Malyan/Monoprice printers, the initial connection to the printer via the 
Connect button may fail. Only the second connection succeeds. 

This plugin is supposed to fix this by invoking a specific serial port opening sequence that has been found
to solve this problem. Note that due to the nature of this sequence this fix can't work for OctoPrint installations
on Windows and is therefore not supported for that OS. 

Printer models known to be affected by this and confirmed as issues resolved with this fix:

  * Turnigy Fabrikator II Mini (Malyan M100)
  * Monoprice Select Mini (Malyan M200)
  * Monoprice Mini Delta (Malyan ?)

For more details please refer to [this ticket on the OctoPrint issue tracker](https://github.com/foosel/OctoPrint/issues/2271).

## Setup

Install via the bundled [Plugin Manager](https://github.com/foosel/OctoPrint/wiki/Plugin:-Plugin-Manager)
or manually using this URL:

    https://github.com/OctoPrint/OctoPrint-MalyanConnectionFix/archive/master.zip
