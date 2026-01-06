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
            new()
            {
                SignID = 13,
                Name = "Wrong Way",
                SymbolName="WrongWay"
            },
            new()
            {
                SignID = 14,
                Name = "No Turning Left",
                SymbolName="NoTurnLeft"
            },
            new()
            {
                SignID = 15,
                Name = "No Overtaking",
                SymbolName="NoOvertaking"
            },
            new()
            {
                SignID = 16,
                Name = "No Stopping",
                SymbolName="NoStopping"
            },
            new()
            {
                SignID = 17,
                Name = "One Way Road",
                SymbolName="OneWayRoad"
            },
            new()
            {
                SignID = 18,
                Name = "Other Dangers",
                SymbolName="OtherDangers"
            },
            new()
            {
                SignID = 19,
                Name = "Parking",
                SymbolName="Parking"
            },
            new()
            {
                SignID = 20,
                Name = "Pass on Either Side",
                SymbolName="PassEitherSide"
            },
            new()
            {
                SignID = 21,
                Name = "Pass on Left",
                SymbolName="PassLeft"
            },
            new()
            {
                SignID = 22,
                Name = "Pass on Right",
                SymbolName="PassRight"
            },
            new()
            {
                SignID = 23,
                Name = "Pedestrian Crossing",
                SymbolName="PedestrianCrossing"
            },
            new()
            {
                SignID = 24,
                Name = "Pedestrian Crossing Warning",
                SymbolName="PedestrianCrossingWarning"
            },
            new()
            {
                SignID = 25,
                Name = "Priority Road",
                SymbolName="Priority"
            },
            new()
            {
                SignID = 26,
                Name = "Roadworks",
                SymbolName="Roadworks"
            },
            new()
            {
                SignID = 27,
                Name = "Roundabout",
                SymbolName="Roundabout"
            },
            new()
            {
                SignID = 28,
                Name = "Slippery Road",
                SymbolName="SlipperyRoad"
            },
            new()
            {
                SignID = 29,
                Name = "Speedbump",
                SymbolName="Speedbump"
            },
            new()
            {
                SignID = 30,
                Name = "Stop",
                SymbolName="Stop"
            },
            new()
            {
                SignID = 31,
                Name = "Turn Left after Sign",
                SymbolName="TurnLeftAfter"
            },
            new()
            {
                SignID = 32,
                Name = "Turn Right after Sign",
                SymbolName="TurnRightAfter"
            },
            new()
            {
                SignID = 33,
                Name = "Two Way Traffic",
                SymbolName="TwoWayTraffic"
            },
            new()
            {
                SignID = 34,
                Name = "Yield",
                SymbolName="Yield"
            },
            new()
            {
                SignID = 35,
                Name = "Bicycle Path",
                SymbolName="BicyclePath"
            },
            new()
            {
                SignID = 36,
                Name = "Straight or Left",
                SymbolName="StraightLeft"
            },
            new()
            {
                SignID = 37,
                Name = "Left Curve",
                SymbolName="LeftCurve"
            },
            new()
            {
                SignID = 38,
                Name = "Multiple Curves",
                SymbolName="MultipleCurves"
            }
        };
    }

    public async Task<IEnumerable<Sign>> GetGridDataAsync()
    {
        _allSigns ??= new List<Sign>(AllSigns());

        await Task.CompletedTask;
        return _allSigns;
    }
}
