using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Controls;
using Microsoft.Windows.Storage.Pickers;

namespace TrafficSignRecognitionProject.ViewModels;

public partial class TrainViewModel : ObservableRecipient
{
    [ObservableProperty]
    private PickFolderResult? _chosenFolder;
    public TrainViewModel()
    {
        ChosenFolder = null;
    }

    [RelayCommand]
    private async Task PickFolderAsync(object uielement)
    {
        if (uielement is Button element && element.XamlRoot != null)
        {
            try
            {
                element.IsEnabled = false;

                // Clear previous returned folder name
                var picker = new FolderPicker(element.XamlRoot.ContentIslandEnvironment.AppWindowId);

                picker.CommitButtonText = "Pick Folder";
                picker.SuggestedStartLocation = PickerLocationId.ComputerFolder;
                picker.ViewMode = PickerViewMode.List;

                // Show the picker dialog window
                ChosenFolder = await picker.PickSingleFolderAsync();

                element.IsEnabled = true;
            }
            catch (Exception e)
            {
                System.Diagnostics.Debug.WriteLine($"Error opening picker:{e.Message}");
            }
        }
    }
}