namespace TrafficSignRecognitionProject.Models;

public class SignDetectionResult
{
    public string Filename
    {
        get; set;
    }

    public string SymbolName
    {
        get; set;
    }

    public override string ToString() => $"{Filename} {SymbolName}";
}