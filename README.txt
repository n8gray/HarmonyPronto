harmony_pronto.py
=================

This script will upload Phillips Pronto codes to your Logitech Harmony account.

You can find the latest version at:

https://github.com/n8gray/HarmonyPronto


Dependencies
============

You'll need libconcord from the Concordance project.  You'll also need the 
python bindings for that library, included in the project as a separate install.

http://phildev.net/concordance/index.shtml
http://sourceforge.net/projects/concordance/

Note that you can use harmony_pronto.py even if your remote is not supported by
concordance!  You don't even have to connect your remote to use it.


Usage
=====

Using a web browser, go to Logitech's Harmony configuration website, currently located at:

http://members.harmonyremote.com/EasyZapper/UserHome.asp

Log in to your account, pick the device you want to upload codes for, and click More Options.  Next click "Learn infrared commands."  Select some commands to learn and click "Learn Selected Commands."  Alternately, scroll down to the "Learn a New Command" area, type in a new command name, and click "Learn New Command."

Your browser should now download a file, for example "LearnIr.EZTut".  This is the file you're going to pass to harmony_pronto.py.  For example:

% harmony_pronto.py ~/Downloads/harmony_pronto.py

You'll be prompted to paste in your Pronto codes one at a time and they will be uploaded to Logitech's website.  After that you can configure them for use in buttons and sequences just like any other command.


Author
======

harmony_pronto.py was written by Nathan Gray, based in large part on code from congruity.py by Stephen Warren:

http://sourceforge.net/projects/congruity/

