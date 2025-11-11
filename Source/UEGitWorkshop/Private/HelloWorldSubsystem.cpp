#include "HelloWorldSubsystem.h"
#include "Engine/Engine.h"
#include "UEGitWorkshopLog.h"

void UHelloWorldSubsystem::Initialize(FSubsystemCollectionBase& Collection)
{
    Super::Initialize(Collection);

    UE_LOG(LogUEGitWorkshop, Display, TEXT("Hello Joni!"));

    if (GEngine)
    {
        GEngine->AddOnScreenDebugMessage(
            -1,
            5.0f,
            FColor::Blue,
            TEXT("Hello Joni!")
        );
    }
}
