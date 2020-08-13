# RemoteControl
A cool remote control program that I have created in python and WPF :)
# What it inclues?

The program gives the abillity to control several computers at the same time.

Things that the controlling user can do on each remote computer(one option each time):

A. An option to open a rev shell, which includes:
  1. remote code execution(Including execution of a binary/any file on the victims computer).		
  2. upload files form the control user compuer to the victims computer, or download files.
  3. An option to encrypt/decrypt files using the AES algoritem(With a libary that I have buillt).		
  4. Navigate in the victim's computer using the cd command
			
B. An option to see the victims screen Live

C. A keylogger - that gives the abillety to see what the victims type live, for an ammount of time that the user decides. 

IMPORTANT - A full description about the project(and about its windows) can be found in the "Case.pdf" file. I very recommand you to take a look at it :)


# Requirements
Microsoft Visual Studio 2015 and above (The project was compiled and tested in Visual Studio 2015, but other versions should work as well). 

Both The client and the server have to have Python2 and Python3 installed(I will try to change that in the future to Python3 only :D) 

In the client side, please run the following commands to install the required packages:

	<Python2> -m pip install -r /Project_Client/requirements2.txt
	<Python3> -m pip install -r /Project_Client/requirements3.txt

In the Server side, please run the following commands to install the required packages:

	<Python2> -m pip install -r /Project_Server/requirements2.txt
	<Python3> -m pip install -r /Project_Server/requirements3.txt

# How to Compile The GUI Server

*Note: The project was compiled and tested in Visual Studio 2015, but other versions should work as well.

To compile the GUI sever, please go into Project_Server\Updated_Gui\GUI\ and run the GUI.sln file. After the project was loaded in VS , Press the start button to compile it(you can compile it in Debug mode and Release mode).
 
 Optional: If you want to run the Python Server In the backround, follow this steps:
 
 	A. Go to PythonListener.cs
	B. In the StartPython() function, change the path of the python file in the "pythonProcess.StartInfo.FileName" variable from "\Python37-32\python.exe" to "\Python37-32\pythonw.exe" .
	




