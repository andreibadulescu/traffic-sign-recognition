using Microsoft.UI.Xaml.Controls;

using TrafficSignRecognitionProject.ViewModels;

namespace TrafficSignRecognitionProject.Views;
public sealed partial class SettingsPage : Page
{
    public SettingsViewModel ViewModel
    {
        get;
    }

    public SettingsPage()
    {
        ViewModel = App.GetService<SettingsViewModel>();
        InitializeComponent();
    }
}
