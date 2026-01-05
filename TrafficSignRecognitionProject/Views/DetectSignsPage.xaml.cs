using Microsoft.UI.Xaml.Controls;

using TrafficSignRecognitionProject.ViewModels;

namespace TrafficSignRecognitionProject.Views;

public sealed partial class DetectSignsPage : Page
{
    public DetectSignsViewModel ViewModel
    {
        get;
    }

    public DetectSignsPage()
    {
        ViewModel = App.GetService<DetectSignsViewModel>();
        InitializeComponent();
    }
}
