using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Net.Sockets;
using System.Net.NetworkInformation;
using System.Threading;
using System.Net;



namespace GUI
{
     class Client_Python_Listener
    {
        private int port;
        Socket clientsock;



        public Client_Python_Listener(Socket clientsock)
        {
            this.clientsock = clientsock;
        }
       

        public void sendCommand(string cmd)
        {
            cmd = cmd + String.Concat(Enumerable.Repeat('*', (1024 - cmd.Length)));
            byte[] msg = Encoding.ASCII.GetBytes(cmd);
            msg = Encoding.ASCII.GetBytes(cmd);
            this.clientsock.Send(msg);//tacking data from window and sending to client
        }

    }
}
