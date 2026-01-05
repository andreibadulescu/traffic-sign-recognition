using TrafficSignRecognitionProject.Core.Models;

namespace TrafficSignRecognitionProject.Core.Contracts.Services;

public interface IDefaultDataService
{
    Task<IEnumerable<Sign>> GetGridDataAsync();
}
