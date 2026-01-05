using TrafficSignRecognitionProject.Core.Contracts.Services;
using TrafficSignRecognitionProject.Core.Models;

namespace TrafficSignRecognitionProject.Core.Services;

// This class holds sample data used by some generated pages to show how they can be used.
// TODO: The following classes have been created to display sample data. Delete these files once your app is using real data.
// 1. Contracts/Services/ISampleDataService.cs
// 2. Services/SampleDataService.cs
// 3. Models/SampleCompany.cs
// 4. Models/SampleOrder.cs
// 5. Models/SampleOrderDetail.cs
public class CatalogueDataService : IDefaultDataService
{
    private List<Sign> _allSigns;

    public CatalogueDataService()
    {
    }

    private static IEnumerable<Sign> AllSigns()
    {
        return new List<Sign>()
        {
            new()
            {
                SignID = 1,
                Name = "Speed Limit 20",
                SymbolName="Limit20"
            },
            new()
            {
                SignID = 2,
                Name = "Speed Limit 30",
                SymbolName="Limit30"
            },
            new()
            {
                SignID = 3,
                Name = "Speed Limit 50",
                SymbolName="Limit50"
            },
            new()
            {
                SignID = 4,
                Name = "Speed Limit 60",
                SymbolName="Limit60"
            },
            new()
            {
                SignID = 5,
                Name = "Speed Limit 70",
                SymbolName="Limit70"
            },
            new()
            {
                SignID = 6,
                Name = "Speed Limit 80",
                SymbolName="Limit80"
            },
            new()
            {
                SignID = 7,
                Name = "Speed Limit 100",
                SymbolName="Limit100"
            },
            new()
            {
                SignID = 8,
                Name = "Speed Limit 110",
                SymbolName="Limit110"
            },
            new()
            {
                SignID = 9,
                Name = "Speed Limit 120",
                SymbolName="Limit120"
            },
            new()
            {
                SignID = 10,
                Name = "Red Semaphore",
                SymbolName="SemaphoreRed"
            },
            new()
            {
                SignID = 11,
                Name = "Green Semaphore",
                SymbolName="SemaphoreGreen"
            },
            new()
            {
                SignID = 12,
                Name = "Arrow Green Semaphore",
                SymbolName="SemaphoreGreenArrow"
            },
        };
    }

    public async Task<IEnumerable<Sign>> GetGridDataAsync()
    {
        _allSigns ??= new List<Sign>(AllSigns());

        await Task.CompletedTask;
        return _allSigns;
    }
}
