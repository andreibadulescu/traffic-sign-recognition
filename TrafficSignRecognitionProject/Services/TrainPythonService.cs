using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace TrafficSignRecognitionProject.Services;

public class TrainPythonService
{
    private readonly string _execPath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "Scripts", "Training", "dataset_preparator.py");
    private readonly string _cutterPath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "Scripts", "Training", "video_cutter.py");
    private readonly string _trainPath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "Scripts", "ML", "train.py");

    public async Task<String> RunAsync(string folderPath, bool isContentAnnotated)
    {
        var processConfig = new ProcessStartInfo
        {
            FileName = "python",
            Arguments = $"\"{_execPath}\" \"{folderPath}\"",
            RedirectStandardError = true,
            UseShellExecute = false,
            CreateNoWindow = true
        };

        var cutterConfig = new ProcessStartInfo
        {
            FileName = "python",
            Arguments = $"\"{_cutterPath}\" \"{folderPath}\"",
            RedirectStandardError = true,
            UseShellExecute = false,
            CreateNoWindow = true
        };

        var trainConfig = new ProcessStartInfo
        {
            FileName = "python",
            Arguments = $"\"{_trainPath}\" --data_dir \"{folderPath}\"",
            RedirectStandardOutput = true,
            RedirectStandardError = true,
            UseShellExecute = false,
            CreateNoWindow = true
        };

        await Task.Run(async () =>
        {
            using var process = new Process { StartInfo = cutterConfig };
            process.Start();

            var errorAsync = process.StandardError.ReadToEndAsync();

            await process.WaitForExitAsync();

            var error = await errorAsync;

            if (process.ExitCode != 0)
            {
                throw new Exception($"Cutter failed: {error}");
            }
        });

        if (!isContentAnnotated)
            await Task.Run(async () =>
            {
                using var process = new Process { StartInfo = processConfig };
                process.Start();

                var errorAsync = process.StandardError.ReadToEndAsync();

                await process.WaitForExitAsync();

                var error = await errorAsync;

                if (process.ExitCode != 0)
                {
                    throw new Exception($"Preparator failed: {error}");
                }
            });

        return await Task.Run(async () =>
        {
            using var process = new Process { StartInfo = trainConfig };
            process.Start();

            var outputAsync = process.StandardOutput.ReadToEndAsync();
            var errorAsync = process.StandardError.ReadToEndAsync();

            await process.WaitForExitAsync();

            var output = await outputAsync;
            var error = await errorAsync;

            if (process.ExitCode != 0)
            {
                throw new Exception($"Training Python Model failed: {error}");
            }

            System.Diagnostics.Debug.WriteLine(output);

            return output;
        });
    }

    public TrainPythonService()
    {
    }
}
