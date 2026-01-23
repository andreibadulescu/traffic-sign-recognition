using System.Reflection;
using System.Windows.Input;

using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;

using Microsoft.UI.Xaml;

using TrafficSignRecognitionProject.Contracts.Services;
using TrafficSignRecognitionProject.Helpers;

using Windows.ApplicationModel;

namespace TrafficSignRecognitionProject.ViewModels;

public partial class SettingsViewModel : ObservableRecipient
{
    private readonly IThemeSelectorService _themeSelectorService;
    private readonly IModuleInstallerService _moduleInstallerService;

    // TODO: Implement loading status

    [ObservableProperty]
    private ElementTheme _elementTheme;

    [ObservableProperty]
    private string _versionDescription;

    [ObservableProperty]
    private Visibility _moduleInstallVis;

    [ObservableProperty]
    private string _moduleInstallStatus;

    public ICommand SwitchThemeCommand
    {
        get;
    }
    
    public ICommand SwitchVisibilityCommand
    {
        get;
    }

    public SettingsViewModel(IThemeSelectorService themeSelectorService, IModuleInstallerService moduleInstallerService)
    {
        _themeSelectorService = themeSelectorService;
        _elementTheme = _themeSelectorService.Theme;
        _versionDescription = GetVersionDescription();
        _moduleInstallerService = moduleInstallerService;
        _moduleInstallVis = moduleInstallerService.ButtonVisibility;
        _moduleInstallStatus = moduleInstallerService.InstallStatus;

        SwitchThemeCommand = new RelayCommand<ElementTheme>(
            async (param) =>
            {
                if (ElementTheme != param)
                {
                    ElementTheme = param;
                    await _themeSelectorService.SetThemeAsync(param);
                }
            });

        SwitchVisibilityCommand = new RelayCommand<Visibility>(
            async (param) =>
            {
                if (ModuleInstallVis != param)
                {
                    ModuleInstallVis = param;
                    await _moduleInstallerService.SetVisibilityAsync(param);
                    ModuleInstallStatus = _moduleInstallerService.InstallStatus;
                }
            });
    }

    private static string GetVersionDescription()
    {
        Version version;

        if (RuntimeHelper.IsMSIX)
        {
            var packageVersion = Package.Current.Id.Version;

            version = new(packageVersion.Major, packageVersion.Minor, packageVersion.Build, packageVersion.Revision);
        }
        else
        {
            version = Assembly.GetExecutingAssembly().GetName().Version!;
        }

        return $"{"AppDisplayName".GetLocalized()} - {version.Major}.{version.Minor}.{version.Build}.{version.Revision}";
    }
}
