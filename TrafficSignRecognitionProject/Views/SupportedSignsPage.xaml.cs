using Microsoft.UI.Xaml.Controls;

using TrafficSignRecognitionProject.ViewModels;

namespace TrafficSignRecognitionProject.Views;

public sealed partial class SupportedSignsPage : Page
{
    public SupportedSignsViewModel ViewModel
    {
        get;
    }

    public SupportedSignsPage()
    {
        ViewModel = App.GetService<SupportedSignsViewModel>();
        InitializeComponent();
    }
}
