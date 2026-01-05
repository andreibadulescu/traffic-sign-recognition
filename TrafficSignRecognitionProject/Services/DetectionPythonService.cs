using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace TrafficSignRecognitionProject.Services;

public class DetectionPythonService
{
    private readonly string _execPath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "Assets", "Scripts", "Testing", "run_inference.py");
    private readonly string _extractorPath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "Assets", "Scripts", "Testing", "frame_extractor.py");

    public async Task<String> RunAsync(string folderPath)
    {
        var processConfig = new ProcessStartInfo
        {
            FileName = "python",
            Arguments = $"\"{_execPath}\" \"{folderPath}\"",
            RedirectStandardOutput = true,
            RedirectStandardError = true,
            UseShellExecute = false,
            CreateNoWindow = true
        };

        var frameExtractorConfig = new ProcessStartInfo
        {
            FileName = "python",
            Arguments = $"\"{_extractorPath}\" \"{folderPath}\"",
            RedirectStandardError = true,
            UseShellExecute = false,
            CreateNoWindow = true
        };

        await Task.Run(async () =>
        {
            using var process = new Process { StartInfo = frameExtractorConfig };
            process.Start();

            var errorAsync = process.StandardError.ReadToEndAsync();

            await process.WaitForExitAsync();

            var error = await errorAsync;

            if (process.ExitCode != 0)
            {
                throw new Exception($"Frame extractor failed: {error}");
            }
        });

        return await Task.Run(async () =>
        {
            using var process = new Process { StartInfo = processConfig };
            process.Start();

            var outputAsync = process.StandardOutput.ReadToEndAsync();
            var errorAsync = process.StandardError.ReadToEndAsync();

            await process.WaitForExitAsync();

            var output = await outputAsync;
            var error = await errorAsync;

            if (process.ExitCode != 0)
            {
                throw new Exception($"Python script failed: {error}");
            }

            return output;
        });
    }

    public DetectionPythonService()
    {
    }
}
