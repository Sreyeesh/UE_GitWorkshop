using UnrealBuildTool;

public class UEGitWorkshopEditorTarget : TargetRules
{
    public UEGitWorkshopEditorTarget(TargetInfo Target) : base(Target)
    {
        Type = TargetType.Editor;
        DefaultBuildSettings = BuildSettingsVersion.V5;
        IncludeOrderVersion = EngineIncludeOrderVersion.Unreal5_6; // was Unreal5_3
        ExtraModuleNames.Add("UEGitWorkshop");
    }
}
