using System.Collections.ObjectModel;
using System.Windows.Input;

using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;

using TrafficSignRecognitionProject.Contracts.Services;
using TrafficSignRecognitionProject.Contracts.ViewModels;
using TrafficSignRecognitionProject.Core.Contracts.Services;
using TrafficSignRecognitionProject.Core.Models;

namespace TrafficSignRecognitionProject.ViewModels;

public partial class SupportedSignsViewModel : ObservableRecipient, INavigationAware
{
    private readonly INavigationService _navigationService;
    private readonly IDefaultDataService _sampleDataService;

    public ObservableCollection<Sign> Source { get; } = new ObservableCollection<Sign>();

    public SupportedSignsViewModel(INavigationService navigationService, IDefaultDataService sampleDataService)
    {
        _navigationService = navigationService;
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
