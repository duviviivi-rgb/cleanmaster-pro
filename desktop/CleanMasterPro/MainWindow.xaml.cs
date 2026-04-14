using System;
using System.Windows;
using CleanMasterPro.Services;

namespace CleanMasterPro
{
    public partial class MainWindow : Window
    {
        private ApiServer apiServer;

        public MainWindow()
        {
            InitializeComponent();
            StartApiServer();
        }

        private void StartApiServer()
        {
            try
            {
                apiServer = new ApiServer(5000);
                apiServer.Start();
                Console.WriteLine("API服务器已启动");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"启动API服务器失败: {ex.Message}");
            }
        }

        protected override void OnClosed(EventArgs e)
        {
            base.OnClosed(e);
            apiServer?.Stop();
            Console.WriteLine("API服务器已停止");
        }
    }
}