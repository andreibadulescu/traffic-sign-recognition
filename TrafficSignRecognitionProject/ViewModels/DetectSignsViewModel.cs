using System.Collections.ObjectModel;
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Controls;
using Microsoft.Windows.Storage.Pickers;
using TrafficSignRecognitionProject.Core.Models;
using TrafficSignRecognitionProject.Models;
using TrafficSignRecognitionProject.Services;
using Windows.Devices.Sms;

namespace TrafficSignRecognitionProject.ViewModels;

public partial class DetectSignsViewModel : ObservableRecipient
{
    private readonly DetectionPythonService _service;

    [ObservableProperty]
    private bool _isProcessing;

    [ObservableProperty]
    private Visibility _showProcessingIcon;

    [ObservableProperty]
    private string _exitMessage;

    [ObservableProperty]
    private Visibility _showExitMessage;

    [ObservableProperty]
    private string _processingResult;

    [ObservableProperty]
    private Visibility _showResults;

    [ObservableProperty]
    private Visibility _showDialogue;

    [ObservableProperty]
    private PickFolderResult? _chosenFolder;

    public ObservableCollection<SignDetectionResult> detectedSigns { get; } = new();
    
    public DetectSignsViewModel()
    {
        ChosenFolder = null;
        _service = new DetectionPythonService();
        ExitMessage = String.Empty;
        IsProcessing = false;
        ProcessingResult = String.Empty;
        ShowExitMessage = Visibility.Collapsed;
        ShowResults = Visibility.Collapsed;
        ShowDialogue = Visibility.Visible;
        ShowProcessingIcon = Visibility.Collapsed;
    }

    [RelayCommand]
    public async Task PickFolderAsync(object uielement)
    {
        if (uielement is Button element && element.XamlRoot != null)
        {
            try
            {
                element.IsEnabled = false;
                ShowResults = Visibility.Collapsed;

                // Clear previous returned folder name
                var picker = new FolderPicker(element.XamlRoot.ContentIslandEnvironment.AppWindowId);

                picker.CommitButtonText = "Pick Folder";
                picker.SuggestedStartLocation = PickerLocationId.ComputerFolder;
                picker.ViewMode = PickerViewMode.List;

                // Show the picker dialog window
                ChosenFolder = await picker.PickSingleFolderAsync();
                await DetectSignsAsync();

                element.IsEnabled = true;
            }
            catch (Exception e)
            {
                System.Diagnostics.Debug.WriteLine($"Error opening picker: {e.Message}");
            }
        }
    }

    [RelayCommand]
    private async Task DetectSignsAsync()
    {
        if (ChosenFolder == null)
        {
            return;
        }

        var folderPath = ChosenFolder.Path;

        try
        {
            ShowExitMessage = Visibility.Visible;
            detectedSigns.Clear();
            IsProcessing = true;
            ShowProcessingIcon = Visibility.Visible;
            ExitMessage = "Processing...\nDo not change tabs.";

            ProcessingResult = await _service.RunAsync(folderPath);
            ParseResults();
            ShowExitMessage = Visibility.Collapsed;
            ShowDialogue = Visibility.Collapsed;
            ShowResults = Visibility.Visible;
            ExitMessage = "Success!";
        }
        catch (Exception e)
        {
            ExitMessage = $"Error while processing: {e.Message}";
        }
        finally
        {
            IsProcessing = false;
            ShowProcessingIcon = Visibility.Collapsed;
        }
    }

    private void ParseResults()
    {
        if (String.IsNullOrWhiteSpace(ProcessingResult)) return;

        var lines = ProcessingResult.Split('\n', StringSplitOptions.RemoveEmptyEntries);

        foreach(var line in lines)
        {
            var tokens = line.Split(' ');

            if (tokens.Length == 2)
            {
                detectedSigns.Add(new SignDetectionResult
                {
                    Filename = tokens[0],
                    SymbolName = tokens[1]
                });
            }
            else
            {
                throw new Exception("ParseResults: Too many tokens for a result entry!");
            }
        }
    }

    [RelayCommand]
    public void ResetView()
    {
        ShowResults = Visibility.Collapsed;
        ShowDialogue = Visibility.Visible;
        ExitMessage = String.Empty;
    }
}
