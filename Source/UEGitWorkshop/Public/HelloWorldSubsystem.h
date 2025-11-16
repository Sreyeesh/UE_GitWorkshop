#pragma once

#include "CoreMinimal.h"
#include "TimerManager.h"
#include "Subsystems/GameInstanceSubsystem.h"

class UWorld;

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
    void HandleWorldInitialized(UWorld& World);
    void HandleWorldBeginPlay();
    void ShowHelloMessage(UWorld& World);
    void ClearWorldBindings();

    FDelegateHandle PostWorldInitHandle;
    FDelegateHandle WorldBeginPlayHandle;
    TWeakObjectPtr<UWorld> PendingHelloWorld;
    TSharedPtr<class SWidget> HelloMessageWidget;
    FTimerHandle HelloMessageTimerHandle;
    TWeakObjectPtr<UWorld> MessageWorld;
};
