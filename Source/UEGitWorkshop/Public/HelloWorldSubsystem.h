#pragma once

#include "CoreMinimal.h"
#include "TimerManager.h"
#include "Subsystems/GameInstanceSubsystem.h"
#include "HelloWorldSubsystem.generated.h"

UCLASS()
class UEGITWORKSHOP_API UHelloWorldSubsystem : public UGameInstanceSubsystem
{
    GENERATED_BODY()

public:
    virtual void Initialize(FSubsystemCollectionBase& Collection) override;
    virtual void Deinitialize() override;

private:
    void RemoveHelloMessage();

    TSharedPtr<class SWidget> HelloMessageWidget;
    FTimerHandle HelloMessageTimerHandle;
};
