using System;using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Net.Sockets;
using System.Threading;
using System.Net;
using System.Diagnostics;
using System.Windows.Threading;

namespace GUI
{
    class PythonListener
    {
        private MainWindow mainWin;
        Socket SockListener, clientsock;
        private int GUI_PORT = 4000;//port to connect tu gui
        public PythonListener(MainWindow mainWin)
        {
            this.mainWin = mainWin;
            Thread th = new Thread(new ThreadStart(run));
            th.IsBackground = true;
            th.Start();
            StartPython();
        }
        private void run()
        {
            SockListener = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
            SockListener.Bind(new IPEndPoint(IPAddress.Any, GUI_PORT));
            SockListener.Listen(1);


            clientsock = SockListener.Accept();
            while (true)
            {
                byte[] buffer = new byte[4096];
                int rec = this.clientsock.Receive(buffer);//geting message from client and shows in the window
                string mesfromclient = Encoding.ASCII.GetString(buffer).Substring(0, rec);
                string patt = mesfromclient.Split('$')[1].Substring(0, 4);
                if (patt == "INFO")
                    this.mainWin.Display_On_TextBlock(mesfromclient.Split('$')[1]);
                else
                    Send_Data_To_Client_Window(mesfromclient);



            }

        }

        void Send_Data_To_Client_Window(string mesfromclient)
        {
            Dictionary<string, Client_Control_Window> dic = this.mainWin.Clients_dic;
            string client_num = mesfromclient.Split('$')[0];
            dic[client_num].Msg = mesfromclient.Split('$')[1];

        }

        private void StartPython()
        {//הפעלת פייתון להרצת קובץ 
            Process pythonProcess = new Process();
            pythonProcess.StartInfo.FileName = @"F:\Study\Cyber-Project\Python37-32\python.exe";
            pythonProcess.StartInfo.Arguments = @"F:\Study\Cyber-Project\ssl\server.py";
            pythonProcess.Start();

        }

        public void sendCommand(string cmd)
        {
            byte[] msg = Encoding.ASCII.GetBytes(cmd);
            msg = Encoding.ASCII.GetBytes(cmd);
            this.clientsock.Send(msg);//tacking data from window and sending to client
        }

        public Socket ClientSock
        {
            get { return this.clientsock;}
        }
    }
}

