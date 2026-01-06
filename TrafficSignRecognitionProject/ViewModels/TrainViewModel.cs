using System.Collections.ObjectModel;
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Controls;
using Microsoft.Windows.Storage.Pickers;
using TrafficSignRecognitionProject.Core.Models;
using TrafficSignRecognitionProject.Services;
using Windows.Foundation.Metadata;

namespace TrafficSignRecognitionProject.ViewModels;

public partial class TrainViewModel : ObservableRecipient
{
    private readonly TrainPythonService _service;

    [ObservableProperty]
    private bool _isProcessing;

    [ObservableProperty]
    private Visibility _showProcessingIcon;

    [ObservableProperty]
    private string _exitMessage;

    [ObservableProperty]
    private Visibility _showExitMessage;

    [ObservableProperty]
    private PickFolderResult? _chosenFolder;
    
    public TrainViewModel()
    {
        ChosenFolder = null;
        ExitMessage = String.Empty;
        IsProcessing = false;
        _service = new TrainPythonService();
        ShowExitMessage = Visibility.Collapsed;
        ShowProcessingIcon = Visibility.Collapsed;
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
                await TrainSignsAsync();

                element.IsEnabled = true;
            }
            catch (Exception e)
            {
                System.Diagnostics.Debug.WriteLine($"Error opening picker: {e.Message}");
            }
        }
    }

    [RelayCommand]
    private async Task TrainSignsAsync()
    {
        if (ChosenFolder == null)
        {
            return;
        }

        var folderPath = ChosenFolder.Path;

        try
        {
            IsProcessing = true;
            ShowProcessingIcon = Visibility.Visible;
            ShowExitMessage = Visibility.Visible;
            ExitMessage = "Processing...\nDo not change tabs.";


            // TODO: Modify true to reflect user choice!
            await _service.RunAsync(folderPath, true);

            ShowExitMessage = Visibility.Collapsed;
            ExitMessage = "Success!\nModel has been trained successfully.";
        }
        catch (Exception e)
        {
            ExitMessage = $"Error while processing: {e.Message}";
        }
        finally
        {
            ShowProcessingIcon = Visibility.Collapsed;
            IsProcessing = false;
        }
    }
}