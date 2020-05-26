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
using System.Windows.Navigation;
using System.Windows.Shapes;
using System.Net.Sockets;
using System.Threading;
using System.Runtime.InteropServices;

namespace GUI
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    /// 
    public partial class MainWindow : Window
    {
        Clients_Info_Win c;
        PythonListener p;
        public int client_num;
        public string ipv4;
        List <Client_Control_Window> clients_windows_list;
        List<Thread> msg_box_thread_lst;
        //Imports for closing messagebox
        [DllImport("user32.dll", EntryPoint = "FindWindow", SetLastError = true)]
        static extern IntPtr FindWindowByCaption(IntPtr ZeroOnly, string lpWindowName);
        [DllImport("user32.Dll")]
        static extern int PostMessage(IntPtr hWnd, UInt32 msg, int wParam, int lParam);
        const UInt32 WM_CLOSE = 0x0010;
        public MainWindow()
        {
            InitializeComponent();
            this.client_num = 0;
            this.ipv4 = Get_Local_Ip();
            this.c = new Clients_Info_Win();
            this.canvas.Children.Add(this.c);
            this.c.Send_Command_Event += new Clients_Info_Win.SendCommand_To_Main(Get_Command);
            this.clients_windows_list = new List<Client_Control_Window>(); 
            this.p = new PythonListener(this);
            this.Closing += Window_Closing;
            this.msg_box_thread_lst = new List<Thread>();
            // we need another list of client number and id's
            //this.client_ids = new List<string>();

        }
    

        public string Get_Local_Ip()
        {
            string myHost = System.Net.Dns.GetHostName();
            string myIP = null;

            for (int i = 0; i <= System.Net.Dns.GetHostEntry(myHost).AddressList.Length - 1; i++)
            {
                if (System.Net.Dns.GetHostEntry(myHost).AddressList[i].IsIPv6LinkLocal == false)
                {
                    myIP = System.Net.Dns.GetHostEntry(myHost).AddressList[i].ToString();
                }
            }
           return myIP;
        }


        private void Window_Closing(object sender, System.ComponentModel.CancelEventArgs e)
        {
            int count = 0;
            string message = "Are you sure that you would like to close the form?";
            string caption = "Program Closing";
            MessageBoxResult result = MessageBox.Show(message, caption, MessageBoxButton.YesNo);
            if (result == MessageBoxResult.Yes)
            {
                this.p.sendCommand("Exit");
                this.p.StopEvent = true;
                this.p.ClientSock.Close();
                CloseMessageBox();
                for (int i = 0; i < this.clients_windows_list.Count; i++)
                {
                    this.clients_windows_list[i].Exit_Flag = true;
                    this.clients_windows_list[i].Close();
                }
            }
            else
                e.Cancel = true;

        }

        void CloseMessageBox()
        {
            IntPtr hWnd = FindWindowByCaption(IntPtr.Zero, "Client Disconnected");
            while (hWnd != IntPtr.Zero)
            {
                PostMessage(hWnd, WM_CLOSE, 0, 0);
                hWnd = FindWindowByCaption(IntPtr.Zero, "Client Disconnected");
            }
            foreach (Thread t in this.msg_box_thread_lst)
            {
                if (t.IsAlive)
                    t.Abort();
            }
        }

        void Get_Command(string cmd)
        {
            bool flag = Check_Choise(cmd);
            if (flag)
            {
                Show_Control_Win(cmd);
            }
            else
                Display_An_Error();
    
        }


        //public void Add_To_Id_List(string id)
        //{
        //    this.client_ids.Add(id);
        //}


        string Remove_Client_From_List(string id_to_remove)
        {
            string ip = "";
            for (int i=0; i< this.clients_windows_list.Count; i++)
            {
                if(this.clients_windows_list[i].Client_ID == id_to_remove)
                {
                    ip = this.clients_windows_list[i].Client_data.Split(' ')[3];
                    this.clients_windows_list[i].Disconnected_Flag = true;
                    this.clients_windows_list[i].Close(); // close his window
                    this.clients_windows_list[i] = null;                    
                    this.clients_windows_list.RemoveAt(i);
                    break;
                }
            }
            return ip;

        }
       

        public void Remove_Disconnected_Client(string id_to_remove)
        {
            string ip = "";
            Dispatcher.Invoke((Action)(() =>
            {
                //this.client_ids.Remove(id_to_remove);
                ip = Remove_Client_From_List(id_to_remove);         
                string ordered_avilible_clients = "";
                int count = 1;
            foreach (Client_Control_Window w in this.clients_windows_list)
                {                   
                    ordered_avilible_clients += "\n" + count + ") " + w.Client_data;
                    count++;            
                }
                this.c.Clients_Data.Text = ordered_avilible_clients;
                

            }));
            this.client_num--;
            var thread = new Thread(
             () =>
             {
                 MessageBox.Show("The client with the following IP:  " + ip + " has been disconnected. his control window has been closed", "Client Disconnected");
             });
            thread.Start();
            this.msg_box_thread_lst.Add(thread);
           
        }


        public int Get_Client_Win_By_Id(string id)
        {

            for (int i = 0; i < this.clients_windows_list.Count; i++)
            {
                if (this.clients_windows_list[i].Client_ID == id)
                    return i;
            }
            return -1;
        }

        void Show_Control_Win(string cmd)
        {

            int pos = (Int32.Parse(cmd) - 1);
            try
            {

                if (this.clients_windows_list[pos] != null)
                {
                    if (!this.clients_windows_list[pos].Isopen)
                    {
                        this.clients_windows_list[pos].Isopen = true;
                        this.clients_windows_list[pos].Show();
                        this.c.alert.Content = "";
                    }
                    else
                        MessageBox.Show("The window is already open", "Alert");
                }
            }
            catch
            {
                Display_An_Error();
            }

           
            

        }




        public void Add_Control_Window(string id, string info)
        {
            Dispatcher.BeginInvoke((Action)(() =>
            {
            Client_Control_Window c1 = new Client_Control_Window(info, id, this.p.ClientSock, this.ipv4);
            this.clients_windows_list.Add(c1);
            }));
        }

        void C1_Send_Command_Event(string cmd)
        {
            this.p.sendCommand(cmd);
        }

        bool Check_Choise(string m)
        {

            int x;
            try
            {
                x = Int32.Parse(m);
            }
            catch(FormatException e)
            {
                return false;
            }

            if (m == "" ||  Int32.Parse(m) < 0 || Int32.Parse(m) > this.client_num || Int32.Parse(m) == 0)
            {
                return false;
            }
            else
                return true;
            
        }


        private void Display_An_Error()
        {
            Dispatcher.BeginInvoke((Action)(() =>
            {
                this.c.alert.Content= "Invalid client number";
            }));
        }




        public void Display_On_TextBlock(string mess)
            {
                Dispatcher.BeginInvoke((Action)(() =>
                {
                    string temp = this.c.Clients_Data.Text;
                    temp += "\n" + (this.client_num + 1) + ") " + mess;
                    this.c.Clients_Data.Text = temp;
                    this.client_num++;
                }));
            }

        public List<Client_Control_Window> Clients_List
        {
            get { return this.clients_windows_list; }
        }



  
      
    }
}
