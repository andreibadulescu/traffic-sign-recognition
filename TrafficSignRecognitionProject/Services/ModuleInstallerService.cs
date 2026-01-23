using System.Diagnostics;
using System.Xml.Linq;
using Microsoft.UI.Xaml;

using TrafficSignRecognitionProject.Contracts.Services;
using TrafficSignRecognitionProject.Helpers;

namespace TrafficSignRecognitionProject.Services;

public class ModuleInstallerService : IModuleInstallerService
{
    private const string SettingsKey = "AppBackgroundInstalledModules";
    private readonly string _requirementsPath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "requirements.txt");

    public Visibility ButtonVisibility { get; set; } = Visibility.Visible;
    public string InstallStatus { get; set; } = "Required Python modules may not be installed.";
    private readonly string ModulesInstalledMessage = "Required Python modules are already installed.";

    private readonly ILocalSettingsService _localSettingsService;

    public ModuleInstallerService(ILocalSettingsService localSettingsService)
    {
        _localSettingsService = localSettingsService;
    }

    public async Task InitializeAsync()
    {
        ButtonVisibility = await LoadVisibilityFromSettingsAsync();
        await Task.CompletedTask;
    }

    public async Task SetVisibilityAsync(Visibility visibility)
    {
        try
        {
            await SetRequestedVisibilityAsync();
        }
        catch (Exception e)
        {
            System.Diagnostics.Debug.WriteLine($"Error while trying to install modules: {e.Message}");
        }
        await SaveVisibilityInSettingsAsync(visibility);
    }

    public async Task SetRequestedVisibilityAsync()
    {
        // TODO: Complete App call to "python -m pip install -r requirements.txt"
        var installerConfig = new ProcessStartInfo
        {
            FileName = "python",
            Arguments = $"-m pip install -r \"{_requirementsPath}\"",
            RedirectStandardOutput = true,
            RedirectStandardError = true,
            UseShellExecute = false,
            CreateNoWindow = true
        };

        await Task.Run(async () =>
        {
            using var process = new Process { StartInfo = installerConfig };
            process.Start();

            var outputAsync = process.StandardOutput.ReadToEndAsync();
            var errorAsync = process.StandardError.ReadToEndAsync();

            await process.WaitForExitAsync();

            var output = await outputAsync;
            var error = await errorAsync;

            if (process.ExitCode != 0)
            {
                throw new Exception($"Module installer failed: {error}");
            }
        });

        if (ButtonVisibility == Visibility.Collapsed)
            InstallStatus = ModulesInstalledMessage;

        await Task.CompletedTask;
    }

    private async Task<Visibility> LoadVisibilityFromSettingsAsync()
    {
        var visibilityName = await _localSettingsService.ReadSettingAsync<string>(SettingsKey);

        if (Enum.TryParse(visibilityName, out Visibility cacheVisibility))
        {
            if (cacheVisibility == Visibility.Collapsed)
                InstallStatus = ModulesInstalledMessage;

            return cacheVisibility;
        }

        return Visibility.Visible;
    }

    private async Task SaveVisibilityInSettingsAsync(Visibility visibility)
    {
        await _localSettingsService.SaveSettingAsync(SettingsKey, visibility.ToString());
    }
}
