using UnrealBuildTool;

public class UEGitWorkshopTarget : TargetRules
{
    public UEGitWorkshopTarget(TargetInfo Target) : base(Target)
    {
        Type = TargetType.Game;
        DefaultBuildSettings = BuildSettingsVersion.V5;
        IncludeOrderVersion = EngineIncludeOrderVersion.Unreal5_6; // was Unreal5_3
        ExtraModuleNames.Add("UEGitWorkshop");
    }
}
