﻿#pragma checksum "..\..\Client_Control_Window.xaml" "{ff1816ec-aa5e-4d10-87f7-6f4963833460}" "D1E73BE941746E602A60D205A9F52898DB28A6FD"
//------------------------------------------------------------------------------
// <auto-generated>
//     This code was generated by a tool.
//     Runtime Version:4.0.30319.42000
//
//     Changes to this file may cause incorrect behavior and will be lost if
//     the code is regenerated.
// </auto-generated>
//------------------------------------------------------------------------------

using GUI;
using System;
using System.Diagnostics;
using System.Windows;
using System.Windows.Automation;
using System.Windows.Controls;
using System.Windows.Controls.Primitives;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Ink;
using System.Windows.Input;
using System.Windows.Markup;
using System.Windows.Media;
using System.Windows.Media.Animation;
using System.Windows.Media.Effects;
using System.Windows.Media.Imaging;
using System.Windows.Media.Media3D;
using System.Windows.Media.TextFormatting;
using System.Windows.Navigation;
using System.Windows.Shapes;
using System.Windows.Shell;


namespace GUI {
    
    
    /// <summary>
    /// Client_Control_Window
    /// </summary>
    public partial class Client_Control_Window : System.Windows.Window, System.Windows.Markup.IComponentConnector {
        
        
        #line 12 "..\..\Client_Control_Window.xaml"
        [System.Diagnostics.CodeAnalysis.SuppressMessageAttribute("Microsoft.Performance", "CA1823:AvoidUnusedPrivateFields")]
        internal System.Windows.Controls.Image image;
        
        #line default
        #line hidden
        
        
        #line 13 "..\..\Client_Control_Window.xaml"
        [System.Diagnostics.CodeAnalysis.SuppressMessageAttribute("Microsoft.Performance", "CA1823:AvoidUnusedPrivateFields")]
        internal System.Windows.Controls.Label lb1;
        
        #line default
        #line hidden
        
        
        #line 14 "..\..\Client_Control_Window.xaml"
        [System.Diagnostics.CodeAnalysis.SuppressMessageAttribute("Microsoft.Performance", "CA1823:AvoidUnusedPrivateFields")]
        internal System.Windows.Controls.Label client_info;
        
        #line default
        #line hidden
        
        
        #line 15 "..\..\Client_Control_Window.xaml"
        [System.Diagnostics.CodeAnalysis.SuppressMessageAttribute("Microsoft.Performance", "CA1823:AvoidUnusedPrivateFields")]
        internal System.Windows.Controls.Button Shell_But;
        
        #line default
        #line hidden
        
        private bool _contentLoaded;
        
        /// <summary>
        /// InitializeComponent
        /// </summary>
        [System.Diagnostics.DebuggerNonUserCodeAttribute()]
        [System.CodeDom.Compiler.GeneratedCodeAttribute("PresentationBuildTasks", "4.0.0.0")]
        public void InitializeComponent() {
            if (_contentLoaded) {
                return;
            }
            _contentLoaded = true;
            System.Uri resourceLocater = new System.Uri("/GUI;component/client_control_window.xaml", System.UriKind.Relative);
            
            #line 1 "..\..\Client_Control_Window.xaml"
            System.Windows.Application.LoadComponent(this, resourceLocater);
            
            #line default
            #line hidden
        }
        
        [System.Diagnostics.DebuggerNonUserCodeAttribute()]
        [System.CodeDom.Compiler.GeneratedCodeAttribute("PresentationBuildTasks", "4.0.0.0")]
        [System.ComponentModel.EditorBrowsableAttribute(System.ComponentModel.EditorBrowsableState.Never)]
        [System.Diagnostics.CodeAnalysis.SuppressMessageAttribute("Microsoft.Design", "CA1033:InterfaceMethodsShouldBeCallableByChildTypes")]
        [System.Diagnostics.CodeAnalysis.SuppressMessageAttribute("Microsoft.Maintainability", "CA1502:AvoidExcessiveComplexity")]
        [System.Diagnostics.CodeAnalysis.SuppressMessageAttribute("Microsoft.Performance", "CA1800:DoNotCastUnnecessarily")]
        void System.Windows.Markup.IComponentConnector.Connect(int connectionId, object target) {
            switch (connectionId)
            {
            case 1:
            this.image = ((System.Windows.Controls.Image)(target));
            return;
            case 2:
            this.lb1 = ((System.Windows.Controls.Label)(target));
            return;
            case 3:
            this.client_info = ((System.Windows.Controls.Label)(target));
            return;
            case 4:
            this.Shell_But = ((System.Windows.Controls.Button)(target));
            
            #line 15 "..\..\Client_Control_Window.xaml"
            this.Shell_But.Click += new System.Windows.RoutedEventHandler(this.Shell_But_Click);
            
            #line default
            #line hidden
            return;
            case 5:
            
            #line 16 "..\..\Client_Control_Window.xaml"
            ((System.Windows.Controls.Button)(target)).Click += new System.Windows.RoutedEventHandler(this.Live_Screen_But_Click);
            
            #line default
            #line hidden
            return;
            case 6:
            
            #line 17 "..\..\Client_Control_Window.xaml"
            ((System.Windows.Controls.Button)(target)).Click += new System.Windows.RoutedEventHandler(this.Keylogger_But_Click);
            
            #line default
            #line hidden
            return;
            }
            this._contentLoaded = true;
        }
    }
}
