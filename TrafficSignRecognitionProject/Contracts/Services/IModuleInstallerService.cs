using Microsoft.UI.Xaml;

namespace TrafficSignRecognitionProject.Contracts.Services;

public interface IModuleInstallerService
{
    Visibility ButtonVisibility
    {
        get;
    }

    string InstallStatus
    {
        get;
    }

    Task InitializeAsync();

    Task SetVisibilityAsync(Visibility showButton);
}
