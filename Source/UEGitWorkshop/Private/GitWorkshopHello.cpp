#include "GitWorkshopHello.h"
#include "Engine/Engine.h"
#include "UEGitWorkshopLog.h"

// Optional: use a dedicated log category instead of LogTemp
// UE_DEFINE_LOG_CATEGORY_STATIC(LogGitWorkshop, Log, All);

AGitWorkshopHello::AGitWorkshopHello()
{
    PrimaryActorTick.bCanEverTick = false;
}

void AGitWorkshopHello::BeginPlay()
{
    Super::BeginPlay();

    //UE_LOG(LogGitWorkshop, Warning, TEXT("Hello World!"));
    UE_LOG(LogUEGitWorkshop, Warning, TEXT("Hello World!"));

    if (GEngine)
    {
        GEngine->AddOnScreenDebugMessage(
            -1,         // key (unique or replace last)
            5.0f,       // time on screen
            FColor::Yellow,
            TEXT("Hello World!")
        );
    }
}
