#include "HelloWorldSubsystem.h"
#include "Engine/Engine.h"
#include "UEGitWorkshopLog.h"

void UHelloWorldSubsystem::Initialize(FSubsystemCollectionBase& Collection)
{
    Super::Initialize(Collection);

    if (UWorld* World = GetWorld())
    {
        if (World->IsGameWorld() && GEngine)
        {
            constexpr const TCHAR* HelloText = TEXT("Hello Joni");

            UE_LOG(LogUEGitWorkshop, Display, TEXT("%s"), HelloText);

            // Use a stable key so subsequent runs replace instead of stacking
            const int32 MessageKey = 1;
            GEngine->AddOnScreenDebugMessage(
                MessageKey,
                5.0f,
                FColor::Red,
                HelloText
            );
        }
    }
}
