namespace TrafficSignRecognitionProject.Core.Models;

public class Sign
{
    public long SignID
    {
        get; set;
    }

    public string Name
    {
        get; set;
    }

    public string SymbolName
    {
        get; set;
    }

    public override string ToString() => $"{Name} {SymbolName}";
}
