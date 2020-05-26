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
using System.Linq;


namespace GUI
{
    /// <summary>
    /// Interaction logic for Clients_Info_Win.xaml
    /// </summary>
    public partial class Clients_Info_Win : UserControl
    {
        public delegate void SendCommand_To_Main(string message);
        private string server_message = "";
        public event SendCommand_To_Main Send_Command_Event;
        public Clients_Info_Win()
        {
            InitializeComponent();
        }
        public string Server_Data
        {
            get
            {
                return this.Server_Data;
            }
            set
            {
                this.Server_Data = value;
            }
        }

        private void Connect_Button_Click(object sender, RoutedEventArgs e)
        {
            if (Send_Command_Event != null)
            {
                string m = this.client_number.Text;
                Send_Command_Event(m);// Send The command to the Min 
            }
        }



        
    }
}
