using System.Collections.ObjectModel;

using CommunityToolkit.Mvvm.ComponentModel;

using TrafficSignRecognitionProject.Contracts.ViewModels;
using TrafficSignRecognitionProject.Core.Contracts.Services;
using TrafficSignRecognitionProject.Core.Models;

namespace TrafficSignRecognitionProject.ViewModels;

public partial class DetectSignsViewModel : ObservableRecipient, INavigationAware
{
    private readonly IDefaultDataService _sampleDataService;

    public ObservableCollection<Sign> Source { get; } = new ObservableCollection<Sign>();

    public DetectSignsViewModel(IDefaultDataService sampleDataService)
    {
        _sampleDataService = sampleDataService;
    }

    public async void OnNavigatedTo(object parameter)
    {
        Source.Clear();

        var data = await _sampleDataService.GetGridDataAsync();

        foreach (var item in data)
        {
            Source.Add(item);
        }
    }

    public void OnNavigatedFrom()
    {
    }
}
