using TrafficSignRecognitionProject.Core.Contracts.Services;
using TrafficSignRecognitionProject.Core.Models;

namespace TrafficSignRecognitionProject.Core.Services;

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
                SymbolName="Limit20.jpg"
            },
            new()
            {
                SignID = 2,
                Name = "Speed Limit 30",
                SymbolName="Limit30.jpg"
            },
            new()
            {
                SignID = 3,
                Name = "Speed Limit 50",
                SymbolName="Limit50.png"
            },
            new()
            {
                SignID = 4,
                Name = "Speed Limit 60",
                SymbolName="Limit60.jpg"
            },
            new()
            {
                SignID = 5,
                Name = "Speed Limit 70",
                SymbolName="Limit70.png"
            },
            new()
            {
                SignID = 6,
                Name = "Speed Limit 80",
                SymbolName="Limit80.jpg"
            },
            new()
            {
                SignID = 7,
                Name = "Speed Limit 100",
                SymbolName="Limit100.jpg"
            },
            new()
            {
                SignID = 8,
                Name = "Speed Limit 110",
                SymbolName="Limit110.png"
            },
            new()
            {
                SignID = 9,
                Name = "Speed Limit 120",
                SymbolName="Limit120.jpg"
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
