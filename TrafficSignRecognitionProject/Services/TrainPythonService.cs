using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace TrafficSignRecognitionProject.Services;

public class TrainPythonService
{
    // TODO: CHANGE PATH TO TRAINING PIPELINE
    private readonly string _execPath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "Scripts", "path_here.py");

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

    public TrainPythonService()
    {
    }
}
